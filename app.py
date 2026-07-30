import xmltodict
import wifi_qrcode_generator.generator
from io import BytesIO
from flask import Flask, render_template, request, send_file
from xml.parsers.expat import ExpatError

app = Flask(__name__)


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _normalize_network(network):
    wifi_configuration = network.get("WifiConfiguration", {})
    attributes = _as_list(wifi_configuration.get("string"))

    wifi_configuration["string"] = attributes

    ssid = ""
    password = ""
    authentication_type = "nopass"
    is_passwordless = True

    for attribute in attributes:
        attribute_name = attribute.get("@name")
        attribute_value = attribute.get("#text", "")

        if attribute_name == "SSID":
            ssid = attribute_value
        elif attribute_name == "PreSharedKey":
            password = attribute_value
            is_passwordless = False
        elif attribute_name == "ConfigKey":
            authentication_type = attribute_value.split('"')[-1].replace("NONE", "nopass")

    return {
        "WifiConfiguration": wifi_configuration,
        "ssid": ssid,
        "password": password,
        "authentication_type": authentication_type,
        "is_passwordless": is_passwordless,
    }


def _extract_networks(xml_bytes):
    data_dict = xmltodict.parse(xml_bytes)
    raw_networks = data_dict.get("WifiConfigStoreData", {}).get("NetworkList", {}).get("Network", [])
    return [_normalize_network(network) for network in _as_list(raw_networks)]


def serve_pil_image(pil_img):
    # https://stackoverflow.com/a/51986716/17100464
    # https://stackoverflow.com/a/10170635/17100464
    img_io = BytesIO()
    pil_img.save(img_io, "JPEG", quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")


@app.route("/generate_qr_code", methods=["GET"])
def qr_code():
    ssid = request.args.get("ssid")
    authentication_type = str(request.args.get("authentication_type"))
    password = request.args.get("password")

    if "WPA" in authentication_type:
        authentication_type = "WPA"
    elif "WEP" in authentication_type:
        authentication_type = "WEP"
    else:
        authentication_type = "nopass"
        password = None

    qr_code = wifi_qrcode_generator.generator.wifi_qrcode(
        ssid=ssid,
        hidden=False,
        authentication_type=authentication_type,
        password=password,
    )
    print(
        f"Generated QR code for SSID: {ssid}, Authentication Type: {authentication_type}, Password: {password}"
    )
    return serve_pil_image(qr_code.make_image())


@app.route("/", methods=["GET", "POST"])
def index():
    networks = []
    error = None

    if request.method == "POST":
        uploaded_file = request.files.get("wifi_config_file")

        if not uploaded_file or not uploaded_file.filename:
            error = "Please choose a WifiConfigStore.xml file to upload."
        else:
            try:
                networks = _extract_networks(uploaded_file.read())
            except (ExpatError, TypeError, ValueError):
                error = "Unable to parse the uploaded XML file."

    return render_template("index.html", networks=networks, error=error)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000,
    )
