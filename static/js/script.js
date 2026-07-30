function togglePasswordless() {
  const checkbox = document.getElementById("show_passwordless");
  const passwordlessNetworks = document.querySelectorAll(".passwordless");

  passwordlessNetworks.forEach((network) => {
    network.style.display = checkbox.checked ? "block" : "none";
  });
}

function selectAll() {
  const checkboxes = document.querySelectorAll(".network-checkbox");
  checkboxes.forEach((checkbox) => {
    checkbox.checked = true;
  });
}

function deselectAll() {
  const checkboxes = document.querySelectorAll(".network-checkbox");
  checkboxes.forEach((checkbox) => {
    checkbox.checked = false;
  });
}

function generateQRCodes() {
  const selectedNetworks = document.querySelectorAll(
    ".network-checkbox:checked",
  );
  selectedNetworks.forEach((network) => {
    const ssid = network.getAttribute("data-ssid");
    const authenticationType = network.getAttribute("data-authentication-type");
    const password = network.getAttribute("data-password");
    const qrCodeUrl = `/generate_qr_code?ssid=${encodeURIComponent(ssid)}&authentication_type=${encodeURIComponent(authenticationType)}&password=${encodeURIComponent(password)}`;
    const qrCodeImage = document.createElement("img");
    qrCodeImage.src = qrCodeUrl;
    if (network.parentElement.querySelector("img")) {
      network.parentElement.querySelector("img").remove();
    }
    network.parentElement.appendChild(qrCodeImage);
  });
}
