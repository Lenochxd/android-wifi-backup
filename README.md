# Android Wi-Fi Restorer
A simple Android app to restore Wi-Fi networks from a rooted android device.

> [!IMPORTANT]  
> Your phone has to be rooted to extract the Wi-Fi networks. The app will generate a QR code for each network, which can be scanned on a non-rooted phone to restore the networks.

# Usage
> [!TIP]
> If your new phone is rooted, you can use the `adb` command to restore the networks directly from the `WifiConfigStore.xml` file:
> ```bash
> adb shell su -c "cat /data/misc/apexdata/com.android.wifi/WifiConfigStore.xml" > WifiConfigStore.xml
> adb push WifiConfigStore.xml /data/misc/apexdata/com.android.wifi/WifiConfigStore.xml
> ```

If your new phone is not rooted, you can use the webapp to generate QR codes for each network, which is the whole purpose of this repo. The steps are as follows:
1. root your phone
2. install adb on your computer
3. run `adb shell su -c "cat /data/misc/apexdata/com.android.wifi/WifiConfigStore.xml" > WifiConfigStore.xml`
4. open the webapp in your browser (`pip install -r requirements.txt` and then `python3 app.py`)
5. upload the `WifiConfigStore.xml` file
6. have fun scanning all the QR codes you want on your new (non-rooted) phone
