// ═══════════════════════════════════════════════════════════════════
// Google Apps Script — Quanto Download Click Logger
// ═══════════════════════════════════════════════════════════════════
//
// SETUP:
// 1. Create a new Google Sheet called "Quanto Creator Tracking"
// 2. Rename the first tab to "Clicks"
// 3. Add headers in row 1: Timestamp | Ref | Device | User Agent
// 4. Create a second tab called "Dashboard" (see below for formulas)
// 5. Open Extensions → Apps Script
// 6. Paste this entire file into Code.gs
// 7. Deploy → New deployment → Web app
//    - Execute as: Me
//    - Who has access: Anyone
// 8. Copy the web app URL and paste it into download/index.html
//    replacing YOUR_APPS_SCRIPT_WEB_APP_URL
//
// ═══════════════════════════════════════════════════════════════════

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Clicks');
    if (!sheet) {
      sheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Clicks');
      sheet.appendRow(['Timestamp', 'Ref', 'Device', 'User Agent']);
    }

    sheet.appendRow([
      data.timestamp || new Date().toISOString(),
      data.ref || 'direct',
      data.device || 'unknown',
      (data.ua || '').substring(0, 300)
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok', message: 'Quanto click logger is running.' }))
    .setMimeType(ContentService.MimeType.JSON);
}
