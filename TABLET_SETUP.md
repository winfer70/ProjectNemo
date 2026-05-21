# Tablet Kiosk Setup — Samsung Galaxy Tab A11+

## Goal
Convert the Tab A11+ into a permanently-on, auto-recovering aquarium dashboard kiosk.

## Hardware
- Samsung Galaxy Tab A11+ (SM-X210, Android 14)
- USB-C cable + charger (leave plugged in permanently)
- Optional: wall mount bracket near aquarium

---

## Step 1: Connect to LAN WiFi
Settings → Connections → WiFi → connect to home network.
Assign a static IP in your router (DHCP reservation by MAC) so the URL never changes.

## Step 2: Enable Developer Options + disable battery optimisation
1. Settings → About Tablet → tap "Build Number" 7 times
2. Settings → Developer Options:
   - Stay Awake: ON (screen stays on while charging)
   - USB Debugging: ON (optional, for adb access)
3. Settings → Battery → "Optimize battery usage" → find Fully Kiosk → Don't optimize

## Step 3: Install Fully Kiosk Browser
- Download from: https://www.fully-kiosk.com/en/#download
- Or search "Fully Kiosk Browser" on Google Play

## Step 4: Configure Fully Kiosk Browser
Open Fully Kiosk → Settings (gear icon, long-press bottom bar):

### Start URL
```
http://[LAN_IP_OF_SWISS_KNIFE]:3000
```
(e.g. http://192.168.1.100:3000)

### Web Content Settings
- Start URL on Boot: ON
- Reload on Error: ON (reload after 10s if page fails)
- Reload after Inactivity: 0 (never auto-reload if working)

### Kiosk Mode
- Enable Kiosk Mode: ON
- Allow Home Button: OFF
- Allow Volume Buttons: OFF
- Allow Power Button: OFF (prevents accidental shutdown)

### Screen & Display
- Keep Screen On: ON
- Prevent Sleep: ON
- Screen Brightness: 40-60% (conserves display, readable)
- Motion Detection Wake: ON (screen wakes when you appREDACTED-HOST)
- Motion Sensitivity: Medium
- Screen Off Timer: 120 seconds of no motion → dim to 10%

### Anti Burn-In
- Screen Saver: ON (activates after 5 min of no motion)
- Screen Saver Type: Black Screen (or subtle animation)
- Dim Screen: ON
- Move Screensaver: ON (prevents static pixel burn-in on OLED)

### Remote Admin (optional, recommended)
- Enable Remote Administration: ON
- Set admin password
- Access via http://[tablet_ip]:2323 from browser to remotely view/control

## Step 5: Set Fully Kiosk as Device Owner (optional, stronger lockdown)
Only needed if you want to prevent any app exit. Run from adb:
```bash
adb shell dpm set-device-owner de.ozerov.fully/.FullyDeviceAdminReceiver
```

## Step 6: Battery management for long-term kiosk
The Tab A11+ will be plugged in permanently. To extend battery lifespan:
- In Fully Kiosk → Settings → Advanced Web Settings → Battery Saver: ON
- Use a smart plug (Tapo P110!) on the charger and schedule it off 01:00–06:00
  (charges to ~80% then rests — better than 100% 24/7)
- OR: Settings → Battery → set max charge level if Samsung DeX supports it

## Step 7: Test crash recovery
1. Open Fully Kiosk with the Nemo URL loaded
2. Force-close the nemo-ui container on REDACTED-HOST
3. Tab should show an error/retry page
4. Restart the container → Tab should auto-reload within ~30 seconds

## Accessing from S11 Ultra and Phone
No setup needed — open the LAN URL in any browser:
```
http://[LAN_IP]:3000              (LAN only)
https://nemo.[your-domain].com    (public, HTTP Basic Auth)
```
The dashboard is fully responsive — 3-column on tablet, 1-column on phone.

## PWA shortcut on phone (optional)
Open the dashboard in Chrome → 3-dot menu → "Add to Home Screen".
Creates an app-like shortcut with full-screen mode.
