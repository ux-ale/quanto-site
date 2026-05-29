# Quanto Creator Download Page — Deploy Guide

## What this is

A landing page at `quanto.app/download` that:

- Reads `?ref=sarah` (or any word) from the URL — defaults to `direct`
- On **iOS/Android**: auto-redirects to the correct store after logging the click
- On **Android**: passes the ref through Play's `referrer` param so it survives install and shows in Play Console → User Acquisition → UTM tags
- On **desktop**: shows both store buttons + a QR code of the current URL (preserves `?ref=`)
- Logs every click (ref + device + timestamp) to a Google Sheet via `sendBeacon`

---

## 1. Google Sheet setup

Create a Google Sheet called **"Quanto Creator Tracking"**.

### Tab 1: `Clicks`

Add these headers in **row 1**:

| A | B | C | D |
|---|---|---|---|
| Timestamp | Ref | Device | User Agent |

Data rows are appended automatically by the Apps Script.

### Tab 2: `Dashboard`

This tab auto-summarizes clicks per creator. Set up:

| Col | Header (row 1) | Formula (row 2, drag down as needed) |
|-----|----------------|--------------------------------------|
| A | Ref | `=SORT(UNIQUE(Clicks!B2:B))` |
| B | iOS Clicks | `=COUNTIFS(Clicks!B:B, A2, Clicks!C:C, "ios")` |
| C | Android Clicks | `=COUNTIFS(Clicks!B:B, A2, Clicks!C:C, "android")` |
| D | Desktop Clicks | `=COUNTIFS(Clicks!B:B, A2, Clicks!C:C, "desktop")` |
| E | Total Clicks | `=SUM(B2:D2)` |
| F | Android Installs | *(paste manually from Play Console)* |

**Why no iOS installs column?**
Apple doesn't expose per-referrer install attribution in App Store Connect without a paid MMP (like AppsFlyer/Adjust). That's intentional — you track iOS *clicks* here and total iOS installs in App Store Connect separately.

**Android installs**: Go to Play Console → Statistics → filter by UTM Campaign = the creator's ref name. Paste the install count into column F periodically.

---

## 2. Apps Script deployment

1. Open the Google Sheet → **Extensions → Apps Script**
2. Replace `Code.gs` contents with `apps-script.js` from this folder
3. Click **Deploy → New deployment**
4. Choose type: **Web app**
5. Settings:
   - Description: `Quanto click logger`
   - Execute as: **Me** (your account)
   - Who has access: **Anyone**
6. Click **Deploy** and authorize when prompted
7. Copy the **Web app URL** (looks like `https://script.google.com/macros/s/AKfyc.../exec`)

---

## 3. Wire the endpoint into the page

Open `download/index.html` and find this line:

```js
var LOG_ENDPOINT = 'YOUR_APPS_SCRIPT_WEB_APP_URL';
```

Replace `YOUR_APPS_SCRIPT_WEB_APP_URL` with the URL from step 2.

---

## 4. Host on quanto.app/download

### Option A: Static hosting (Vercel / Netlify / Cloudflare Pages)

Drop the `download/` folder contents into your hosting root so that `quanto.app/download/index.html` resolves. Most hosts support a rewrite rule to serve `/download` → `/download/index.html`.

### Option B: Firebase Hosting (if you already use Firebase)

Add to `firebase.json`:

```json
{
  "hosting": {
    "rewrites": [
      { "source": "/download", "destination": "/download/index.html" }
    ]
  }
}
```

### Files to deploy

```
download/
  index.html           ← the page
  quanto-app-icon.png   ← app icon (referenced by the page)
```

---

## 5. Creator links

Give each creator a personalized link. The `ref` param is freeform — no registration needed:

| Creator | Link |
|---------|------|
| Sarah | `https://quanto.app/download?ref=sarah` |
| Mark | `https://quanto.app/download?ref=mark` |
| TikTok bio | `https://quanto.app/download?ref=tiktok` |
| Instagram story | `https://quanto.app/download?ref=ig-story` |
| Direct / organic | `https://quanto.app/download` (ref defaults to `direct`) |

---

## 6. How the Play referrer works

When an Android user clicks the download link, the URL becomes:

```
https://play.google.com/store/apps/details?id=app.quanto.quanto&referrer=utm_source%3Dquanto_download%26utm_medium%3Dcreator%26utm_campaign%3Dsarah
```

After install, Play Console reports these UTM params under **Statistics → User acquisition**. Filter by `utm_campaign` to see installs per creator.

---

## Dashboard model summary

| Metric | Source | Per-creator? |
|--------|--------|-------------|
| iOS clicks | Google Sheet (auto) | Yes |
| Android clicks | Google Sheet (auto) | Yes |
| Desktop clicks | Google Sheet (auto) | Yes |
| Android installs | Play Console (manual paste) | Yes |
| iOS installs | App Store Connect (total only) | No — intentional |
