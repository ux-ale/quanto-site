import json

SRC = 'quanto-aso-all-locales.json'
OUT = 'index.html'

data = json.load(open(SRC))

# Display order, flag and chip label per locale (chip labels as specified).
LOCALE_META = [
    ("EN",     "\U0001F1EC\U0001F1E7", "English"),
    ("DE",     "\U0001F1E9\U0001F1EA", "German"),
    ("FR",     "\U0001F1EB\U0001F1F7", "French"),
    ("ES-ES",  "\U0001F1EA\U0001F1F8", "Spanish"),
    ("ES-419", "\U0001F310",           "Latam"),
    ("IT",     "\U0001F1EE\U0001F1F9", "Italian"),
    ("PT-BR",  "\U0001F1E7\U0001F1F7", "Portuguese (Brazil)"),
    ("TR",     "\U0001F1F9\U0001F1F7", "Turkish"),
    ("ID",     "\U0001F1EE\U0001F1E9", "Indonesian"),
    ("MS",     "\U0001F1F2\U0001F1FE", "Malay"),
    ("JA",     "\U0001F1EF\U0001F1F5", "Japanese"),
    ("KO",     "\U0001F1F0\U0001F1F7", "Korean"),
    ("NL",     "\U0001F1F3\U0001F1F1", "Dutch"),
    ("PL",     "\U0001F1F5\U0001F1F1", "Polish"),
]

# Short ASO note shown beside each field label.
HINTS = {
    "ios_name":  "Highest-weighted field. Needs a new version to change",
    "ios_sub":   "Second-highest. No word repeated from the name",
    "kw_us":     "Hidden from users. Comma-separated, no spaces, no repeats",
    "kw_gb":     "Separate keyword index for the U.K. storefront",
    "promo":     "Not indexed. Can be changed without a new version",
    "ios_desc":  "Not indexed on the App Store. Written for conversion",
    "iap_group": "Indexed. Shown on the subscription sheet",
    "iap_m":     "Indexed. Shown at checkout",
    "iap_y":     "Indexed. Shown at checkout",
    "iap_l":     "Indexed. Shown at checkout",
    "play_title":"Indexed. Highest weight on Google Play",
    "play_short":"Indexed. Shown under the title",
    "play_full": "Indexed on Google Play, unlike the App Store",
}

known = {c for c, _, _ in LOCALE_META}
missing = [l['code'] for l in data['locales'] if l['code'] not in known]
assert not missing, f"locale missing from LOCALE_META: {missing}"
assert set(HINTS) == {f['key'] for f in data['fields']}, "HINTS keys must match fields"

order = {c: i for i, (c, _, _) in enumerate(LOCALE_META)}
data['locales'].sort(key=lambda l: order[l['code']])
for l in data['locales']:
    _, flag, label = next(m for m in LOCALE_META if m[0] == l['code'])
    l['flag'] = flag
    l['chip'] = label
for f in data['fields']:
    f['hint'] = HINTS[f['key']]

payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quanto — Store Localization</title>
<meta name="description" content="App Store and Google Play metadata for every Quanto locale, ready to copy.">
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="quanto-icon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="quanto-icon-180.png">
<meta name="apple-mobile-web-app-title" content="Localization">
<meta name="theme-color" content="#0C0F11">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0C0F11;
    --sem-5:  rgba(255,255,255,0.05);
    --sem-8:  rgba(255,255,255,0.08);
    --sem-15: rgba(255,255,255,0.15);
    --border: rgba(255,255,255,0.08);
    --brand:  #0cbba1;
    --warn:   #f0920e;
    --danger: #ff6b5e;
    --text-1: #ffffff;
    --text-2: rgba(255,255,255,0.55);
    --text-3: rgba(255,255,255,0.30);
    --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  }

  html, body { margin: 0; min-height: 100%; background: #0C0F11; overscroll-behavior: none; }
  html { scroll-behavior: smooth; }

  body::before {
    content: ""; position: fixed; inset: 0; z-index: -1;
    background: linear-gradient(180deg, #283339 0%, #0C0F11 100%);
    pointer-events: none;
  }

  body {
    font-family: 'Sora', sans-serif;
    background: transparent;
    color: var(--text-1);
    -webkit-font-smoothing: antialiased;
    line-height: 1.6;
    min-height: 100vh;
  }

  .wrap { max-width: 940px; margin: 0 auto; padding: 0 28px 72px; }

  /* ─── HERO ─── */
  .hero { padding: 56px 0 26px; }

  .hero-icon {
    width: 52px; height: 52px; border-radius: 13px; overflow: hidden;
    margin: 0 0 20px; box-shadow: 0 16px 48px rgba(0,0,0,0.4);
  }
  .hero-icon img { width: 100%; height: 100%; display: block; }

  .hero h1 {
    font-size: clamp(30px, 5.5vw, 42px); font-weight: 700;
    line-height: 1.05; letter-spacing: -0.03em;
  }
  .hero h1 .teal { color: var(--brand); }

  /* ─── LOCALE CHIPS ─── */
  .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 44px; }

  .chips button {
    display: inline-flex; align-items: center; gap: 8px; cursor: pointer;
    padding: 8px 15px; border-radius: 100px;
    background: var(--sem-5); border: 1px solid var(--border);
    color: var(--text-2); font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 400;
    transition: background 0.15s, border-color 0.15s, color 0.15s;
    -webkit-tap-highlight-color: transparent;
  }
  .chips button .flag { font-size: 14px; line-height: 1; }
  .chips button:hover { color: var(--text-1); border-color: var(--sem-15); }
  .chips button.active {
    background: rgba(12,187,161,0.14); border-color: var(--brand);
    color: var(--text-1); font-weight: 600;
  }

  /* ─── LOCALE HEADER ─── */
  .locale-head {
    display: flex; align-items: flex-start; gap: 20px; flex-wrap: wrap;
    padding-bottom: 22px; border-bottom: 1px solid var(--border); margin-bottom: 32px;
  }
  .locale-head .who { margin-right: auto; }
  .locale-head h2 { font-size: 30px; font-weight: 700; letter-spacing: -0.025em; line-height: 1.15; }
  .locale-head .sub {
    font-size: 14px; font-weight: 300; color: var(--text-2); margin-top: 6px;
  }
  .locale-head .sub b { font-weight: 600; color: var(--text-1); }
  .locale-head .sub .final { color: var(--brand); font-weight: 600; }
  .locale-head .sub .draft { color: var(--warn); font-weight: 600; }

  .seg {
    display: inline-flex; gap: 3px; padding: 3px; flex-shrink: 0;
    background: var(--sem-5); border: 1px solid var(--border); border-radius: 11px;
  }
  .seg button {
    padding: 8px 16px; border-radius: 8px; cursor: pointer; border: none; background: none;
    font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600; color: var(--text-3);
    transition: background 0.15s, color 0.15s; -webkit-tap-highlight-color: transparent;
  }
  .seg button:hover { color: var(--text-2); }
  .seg button.on { background: rgba(255,255,255,0.10); color: var(--text-1); }

  /* ─── SECTION ─── */
  .section-title {
    display: flex; align-items: center; gap: 16px; margin-bottom: 14px;
    font-size: 11.5px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--text-3);
  }
  .section-title::after { content: ""; flex: 1; height: 1px; background: var(--border); }

  /* ─── FIELD ─── */
  .field {
    border: 1px solid var(--border); border-left: 2px solid transparent;
    border-radius: 12px; background: rgba(255,255,255,0.03);
    margin-bottom: 12px; overflow: hidden;
    transition: border-color 0.2s;
  }
  .field.is-copied { border-left-color: var(--brand); }

  .field-head { display: flex; align-items: center; gap: 14px; padding: 14px 18px; }

  .field-label { font-size: 15px; font-weight: 600; white-space: nowrap; }
  .field-hint {
    font-size: 12.5px; font-weight: 300; color: var(--text-3);
    margin-right: auto; line-height: 1.4;
  }

  .meter { width: 96px; height: 4px; border-radius: 100px; background: rgba(255,255,255,0.10); flex-shrink: 0; }
  .meter span { display: block; height: 100%; border-radius: 100px; background: var(--brand); }
  .meter.near span, .meter.max span { background: var(--warn); }
  .meter.over span { background: var(--danger); }

  .count {
    font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums;
    color: var(--text-2); white-space: nowrap; flex-shrink: 0;
  }
  .count.near, .count.max { color: var(--warn); }
  .count.over { color: var(--danger); }

  .copy-btn {
    flex-shrink: 0; cursor: pointer; padding: 7px 18px; border-radius: 100px;
    background: var(--sem-5); border: 1px solid var(--sem-15); color: var(--text-1);
    font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 600;
    transition: background 0.15s, border-color 0.15s; -webkit-tap-highlight-color: transparent;
  }
  .copy-btn:hover { background: var(--sem-8); border-color: rgba(255,255,255,0.28); }
  .copy-btn:active { background: rgba(255,255,255,0.02); }

  .field-body {
    border-top: 1px solid var(--border); background: rgba(0,0,0,0.20);
    padding: 16px 18px;
    font-family: var(--mono); font-size: 13px; line-height: 1.7;
    color: var(--text-1); white-space: pre-wrap; word-break: break-word;
  }
  .field-body.kw { color: var(--brand); }

  .field-body.clamped {
    max-height: 200px; overflow: hidden;
    -webkit-mask-image: linear-gradient(180deg, #000 130px, transparent 100%);
            mask-image: linear-gradient(180deg, #000 130px, transparent 100%);
  }

  .expand {
    display: block; width: 100%; text-align: left; cursor: pointer;
    background: rgba(0,0,0,0.20); border: none; border-top: 1px solid var(--border);
    padding: 10px 18px; font-family: 'Sora', sans-serif; font-size: 12px;
    font-weight: 400; color: var(--text-3);
  }
  .expand:hover { color: var(--text-2); }

  /* ─── FOOTER ─── */
  footer {
    margin-top: 44px; padding-top: 22px; border-top: 1px solid var(--border);
    display: flex; flex-wrap: wrap; align-items: center; gap: 14px;
    font-size: 11px; font-weight: 300; color: var(--text-3);
  }
  .linkbtn {
    margin-left: auto; background: none; border: none; padding: 0; cursor: pointer;
    font-family: 'Sora', sans-serif; font-size: 11px; font-weight: 400; color: var(--text-3);
    text-decoration: underline; text-underline-offset: 3px;
  }
  .linkbtn:hover { color: var(--text-2); }

  /* ─── TOAST ─── */
  .toast {
    position: fixed; bottom: 28px; left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: var(--brand); color: #07211d;
    font-size: 13px; font-weight: 600; padding: 11px 20px; border-radius: 100px;
    box-shadow: 0 8px 28px rgba(0,0,0,0.45);
    opacity: 0; pointer-events: none;
    transition: opacity 0.22s, transform 0.22s; z-index: 100;
  }
  .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }

  @media (max-width: 720px) {
    .wrap { padding: 0 18px 56px; }
    .hero { padding: 40px 0 20px; }
    .chips { margin-bottom: 32px; }
    .field-head { flex-wrap: wrap; gap: 10px 12px; padding: 14px 15px; }
    .field-label { width: 100%; }
    .field-hint { width: 100%; margin-right: 0; order: 3; }
    .meter { order: 1; }
    .count { order: 1; margin-right: auto; }
    .copy-btn { order: 2; }
    .field-body { padding: 14px 15px; }
    .locale-head { gap: 16px; }
    .seg { width: 100%; }
    .seg button { flex: 1; }
  }
</style>
</head>
<body>

<div class="wrap">

  <header class="hero">
    <div class="hero-icon"><img src="quanto-icon-192.png" alt="Quanto" width="52" height="52" decoding="async" fetchpriority="high"></div>
    <h1>Store <span class="teal">Localization</span></h1>
  </header>

  <nav class="chips" id="chips"></nav>

  <div id="panel"></div>

  <footer>
    <span id="foot-note"></span>
    <button class="linkbtn" id="reset-all">Reset copied markers</button>
  </footer>

</div>

<div class="toast" id="toast">Copied to clipboard</div>

<script>
const DATA = '''

TAIL = ''';

const FIELDS = DATA.fields;
const LOCALES = DATA.locales;
const KEY = 'quanto-aso-progress-v1';

let current = LOCALES[0].code;
let store = 'ios';

/* ─── COPIED MARKERS ─── */
let progress = {};
try { progress = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { progress = {}; }
function saveProgress() { try { localStorage.setItem(KEY, JSON.stringify(progress)); } catch (e) {} }
function isCopied(code, key) { return !!(progress[code] && progress[code][key]); }
function markCopied(code, key) {
  if (!progress[code]) progress[code] = {};
  progress[code][key] = true;
  saveProgress();
}

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const fieldsFor = (loc, st) => FIELDS.filter(f => f.store === st && loc.values[f.key]);

function level(n, limit) {
  if (n > limit) return 'over';
  if (n === limit) return 'max';
  if (n >= limit * 0.9) return 'near';
  return '';
}

function renderChips() {
  document.getElementById('chips').innerHTML = LOCALES.map(l =>
    '<button data-locale="' + l.code + '" class="' + (l.code === current ? 'active' : '') + '">' +
      '<span class="flag">' + l.flag + '</span><span>' + esc(l.chip) + '</span>' +
    '</button>').join('');
}

function fieldHTML(loc, f) {
  const val = loc.values[f.key];
  const n = val.length;
  const lv = level(n, f.limit);
  const pct = Math.min(100, (n / f.limit) * 100);
  const long = n > 400;
  const isKw = f.key.indexOf('kw_') === 0;
  return '' +
    '<div class="field' + (isCopied(loc.code, f.key) ? ' is-copied' : '') + '" data-key="' + f.key + '">' +
      '<div class="field-head">' +
        '<span class="field-label">' + esc(f.label) + '</span>' +
        '<span class="field-hint">' + esc(f.hint) + '</span>' +
        '<span class="meter ' + lv + '"><span style="width:' + pct + '%"></span></span>' +
        '<span class="count ' + lv + '">' + n + '/' + f.limit + '</span>' +
        '<button class="copy-btn" data-copy>Copy</button>' +
      '</div>' +
      '<div class="field-body' + (isKw ? ' kw' : '') + (long ? ' clamped' : '') + '">' + esc(val) + '</div>' +
      (long ? '<button class="expand" data-expand>Show full text</button>' : '') +
    '</div>';
}

function renderPanel() {
  const loc = LOCALES.find(l => l.code === current);
  const list = fieldsFor(loc, store);
  const statusHTML = loc.status === 'final'
    ? '<span class="final">Live</span>'
    : '<span class="draft">Draft — needs native review</span>';
  // EN's note is just "Live", which the status already says
  const note = (loc.note && !/^live$/i.test(loc.note.trim())) ? loc.note : '';

  document.getElementById('panel').innerHTML =
    '<div class="locale-head">' +
      '<div class="who">' +
        '<h2>' + l_flag(loc) + esc(loc.language) + '</h2>' +
        '<div class="sub">App Store locale <b>' + esc(loc.appStoreLocale) + '</b> · ' + statusHTML +
          (note ? ' · ' + esc(note) : '') + '</div>' +
      '</div>' +
      '<div class="seg">' +
        '<button data-store="ios" class="' + (store === 'ios' ? 'on' : '') + '">App Store</button>' +
        '<button data-store="play" class="' + (store === 'play' ? 'on' : '') + '">Google Play</button>' +
      '</div>' +
    '</div>' +
    '<h3 class="section-title">' + (store === 'ios' ? 'App Store Connect' : 'Google Play Console') + '</h3>' +
    list.map(f => fieldHTML(loc, f)).join('');
}

function l_flag(loc) { return '<span style="margin-right:10px">' + loc.flag + '</span>'; }

function renderAll() { renderChips(); renderPanel(); }

/* ─── TOAST ─── */
const toast = document.getElementById('toast');
let toastTimer;
function showToast(msg) {
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 1600);
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (e) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (_) {}
    document.body.removeChild(ta);
    return ok;
  }
}

/* ─── EVENTS ─── */
document.getElementById('chips').addEventListener('click', e => {
  const b = e.target.closest('[data-locale]');
  if (!b) return;
  current = b.getAttribute('data-locale');
  renderAll();
});

document.getElementById('panel').addEventListener('click', async e => {
  const seg = e.target.closest('[data-store]');
  if (seg) { store = seg.getAttribute('data-store'); renderPanel(); return; }

  const field = e.target.closest('.field');
  if (!field) return;
  const key = field.getAttribute('data-key');
  const loc = LOCALES.find(l => l.code === current);

  if (e.target.closest('[data-expand]')) {
    const body = field.querySelector('.field-body');
    const btn = e.target.closest('[data-expand]');
    btn.textContent = body.classList.toggle('clamped') ? 'Show full text' : 'Show less';
    return;
  }

  if (e.target.closest('[data-copy]')) {
    const ok = await copyText(loc.values[key]);
    if (!ok) { showToast('Press and hold to copy'); return; }
    showToast('Copied ' + FIELDS.find(f => f.key === key).label);
    markCopied(loc.code, key);
    field.classList.add('is-copied');
  }
});

document.getElementById('reset-all').addEventListener('click', () => {
  progress = {};
  saveProgress();
  renderPanel();
  showToast('Cleared copied markers');
});

document.getElementById('foot-note').textContent =
  DATA.app + ' store metadata — ' + LOCALES.length + ' locales, generated ' + DATA.generated +
  '. Copied markers are saved in this browser only.';
renderAll();
</script>

</body>
</html>
'''

open(OUT, 'w').write(HEAD + payload + TAIL)
print('wrote', OUT)
