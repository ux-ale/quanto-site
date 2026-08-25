import json

SRC = 'quanto-aso-all-locales.json'
OUT = 'index.html'

data = json.load(open(SRC))
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
    --warn:   #e5a13a;
    --danger: #ff6b5e;
    --text-1: #ffffff;
    --text-2: rgba(255,255,255,0.55);
    --text-3: rgba(255,255,255,0.30);
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

  .wrap { max-width: 780px; margin: 0 auto; padding: 0 24px 64px; }

  /* ─── HERO ─── */
  .hero { padding: 56px 0 28px; }

  .hero-icon {
    width: 56px; height: 56px; border-radius: 14px; overflow: hidden;
    margin: 0 0 22px; box-shadow: 0 16px 48px rgba(0,0,0,0.4);
  }
  .hero-icon img { width: 100%; height: 100%; display: block; }

  .hero h1 {
    font-size: clamp(30px, 5.5vw, 42px); font-weight: 700;
    line-height: 1.05; letter-spacing: -0.03em; margin-bottom: 14px;
  }
  .hero h1 .teal { color: var(--brand); }

  .hero p { font-size: 14.5px; font-weight: 300; color: var(--text-2); max-width: 520px; }

  .hero-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }

  .pill {
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.02em;
    padding: 5px 11px; border-radius: 100px;
    background: var(--sem-8); border: 1px solid var(--border); color: var(--text-2);
  }
  .pill.teal { background: rgba(12,187,161,0.12); border-color: rgba(12,187,161,0.35); color: var(--brand); }
  .pill.warn { background: rgba(229,161,58,0.12); border-color: rgba(229,161,58,0.35); color: var(--warn); }

  /* ─── OVERALL PROGRESS ─── */
  .overall {
    border: 1px solid var(--border); border-radius: 14px; background: var(--sem-5);
    padding: 16px 18px; margin-bottom: 26px;
  }
  .overall-top {
    display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 10px;
  }
  .overall-label { font-size: 12.5px; font-weight: 600; color: var(--text-1); }
  .overall-count { font-size: 12px; font-weight: 400; color: var(--text-3); font-variant-numeric: tabular-nums; }
  .bar { height: 5px; border-radius: 100px; background: rgba(255,255,255,0.07); overflow: hidden; }
  .bar span { display: block; height: 100%; background: var(--brand); border-radius: 100px; transition: width 0.25s ease; }

  /* ─── LOCALE NAV ─── */
  .locale-nav {
    position: sticky; top: 0; z-index: 30;
    margin: 0 -24px 26px; padding: 0 24px;
    background: rgba(12,15,17,0.85);
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border);
  }
  .locale-nav ul { list-style: none; display: flex; gap: 6px; overflow-x: auto; padding: 11px 0; scrollbar-width: none; }
  .locale-nav ul::-webkit-scrollbar { display: none; }

  .locale-nav button {
    display: flex; align-items: center; gap: 7px; flex-shrink: 0; white-space: nowrap;
    padding: 7px 13px; border-radius: 100px; cursor: pointer;
    background: var(--sem-8); border: 1px solid var(--border);
    color: var(--text-2); font-family: 'Sora', sans-serif; font-size: 12.5px; font-weight: 400;
    transition: background 0.15s, border-color 0.15s, color 0.15s;
    -webkit-tap-highlight-color: transparent;
  }
  .locale-nav button:hover { color: var(--text-1); border-color: var(--sem-15); }
  .locale-nav button .code { font-weight: 600; font-size: 12px; letter-spacing: 0.02em; }
  .locale-nav button .tick { width: 6px; height: 6px; border-radius: 50%; background: var(--text-3); flex-shrink: 0; }
  .locale-nav button.complete .tick { background: var(--brand); }
  .locale-nav button.active { background: rgba(12,187,161,0.14); border-color: var(--brand); color: var(--text-1); }

  /* ─── LOCALE HEADER ─── */
  .locale-head { margin-bottom: 26px; }
  .locale-head h2 { font-size: 26px; font-weight: 700; letter-spacing: -0.02em; line-height: 1.15; }
  .asc-line {
    display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px;
    font-size: 13px; font-weight: 300; color: var(--text-2); margin-top: 8px;
  }
  .asc-line b { font-weight: 600; color: var(--brand); }
  .locale-head .note { font-size: 13px; font-weight: 300; color: var(--text-3); margin-top: 6px; }
  .locale-head .pills { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }

  /* ─── SECTIONS ─── */
  .section { margin-top: 34px; }
  .section-title {
    display: flex; align-items: baseline; gap: 10px;
    font-size: 12px; font-weight: 600; letter-spacing: 0.10em; text-transform: uppercase;
    color: var(--text-3); padding-bottom: 12px; border-bottom: 1px solid var(--border); margin-bottom: 16px;
  }
  .section-title .n { font-size: 11px; font-weight: 400; letter-spacing: 0; text-transform: none; }

  /* ─── FIELD ─── */
  .field {
    border: 1px solid var(--border); border-left: 2px solid transparent;
    border-radius: 12px; background: var(--sem-5); padding: 14px 16px; margin-bottom: 12px;
    transition: border-color 0.2s, opacity 0.2s;
  }
  .field.is-done { border-left-color: var(--brand); opacity: 0.62; }

  .field-top { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }
  .field-label { font-size: 13px; font-weight: 600; color: var(--text-1); margin-right: auto; }

  .badge {
    font-size: 10px; font-weight: 600; letter-spacing: 0.03em;
    padding: 3px 8px; border-radius: 100px; white-space: nowrap;
    background: var(--sem-8); border: 1px solid var(--border); color: var(--text-3);
  }
  .badge.idx { background: rgba(12,187,161,0.10); border-color: rgba(12,187,161,0.30); color: var(--brand); }
  .badge.ver { background: rgba(229,161,58,0.10); border-color: rgba(229,161,58,0.30); color: var(--warn); }

  .count {
    font-size: 11.5px; font-weight: 600; font-variant-numeric: tabular-nums;
    color: var(--text-3); white-space: nowrap;
  }
  .count.near { color: var(--warn); }
  .count.max  { color: var(--brand); }
  .count.over { color: var(--danger); }

  .field-val {
    width: 100%; text-align: left; display: block; cursor: pointer;
    font-family: 'Sora', sans-serif; font-size: 13px; font-weight: 300; line-height: 1.65;
    color: var(--text-1); white-space: pre-wrap; word-break: break-word;
    background: rgba(0,0,0,0.22); border: 1px solid var(--border); border-radius: 9px;
    padding: 12px 14px; transition: border-color 0.15s, background 0.15s;
    -webkit-tap-highlight-color: transparent;
  }
  .field-val:hover { border-color: var(--sem-15); }
  .field-val.kw { color: var(--brand); font-size: 12.5px; line-height: 1.7; }

  .field-val.clamped {
    max-height: 190px; overflow: hidden;
    -webkit-mask-image: linear-gradient(180deg, #000 120px, transparent 100%);
            mask-image: linear-gradient(180deg, #000 120px, transparent 100%);
  }

  .field-foot { display: flex; align-items: center; gap: 10px; margin-top: 10px; }

  .linkbtn {
    background: none; border: none; padding: 0; cursor: pointer;
    font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 400; color: var(--text-3);
    text-decoration: underline; text-underline-offset: 3px;
  }
  .linkbtn:hover { color: var(--text-2); }

  .done-btn {
    margin-left: auto; display: inline-flex; align-items: center; gap: 7px; cursor: pointer;
    font-family: 'Sora', sans-serif; font-size: 12px; font-weight: 400; color: var(--text-3);
    background: var(--sem-5); border: 1px solid var(--border); border-radius: 100px; padding: 5px 12px;
    transition: all 0.15s; -webkit-tap-highlight-color: transparent;
  }
  .done-btn:hover { color: var(--text-2); border-color: var(--sem-15); }
  .done-btn .box {
    width: 13px; height: 13px; border-radius: 4px; flex-shrink: 0;
    border: 1.5px solid var(--sem-15); display: grid; place-items: center;
  }
  .done-btn .box svg { width: 9px; height: 9px; opacity: 0; }
  .field.is-done .done-btn { color: var(--brand); border-color: rgba(12,187,161,0.35); background: rgba(12,187,161,0.10); }
  .field.is-done .done-btn .box { background: var(--brand); border-color: var(--brand); }
  .field.is-done .done-btn .box svg { opacity: 1; color: #07211d; }

  /* ─── FOOTER ─── */
  footer {
    margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--border);
    display: flex; flex-wrap: wrap; align-items: center; gap: 14px;
    font-size: 11px; font-weight: 300; color: var(--text-3);
  }
  footer .spacer { margin-left: auto; }

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

  @media (max-width: 560px) {
    .wrap { padding: 0 16px 48px; }
    .locale-nav { margin: 0 -16px 22px; padding: 0 16px; }
    .hero { padding: 40px 0 22px; }
    .field { padding: 13px 14px; }
  }
</style>
</head>
<body>

<div class="wrap">

  <header class="hero">
    <div class="hero-icon"><img src="quanto-icon-192.png" alt="Quanto" width="56" height="56" decoding="async" fetchpriority="high"></div>
    <h1>Store <span class="teal">Localization</span></h1>
    <p>Every App Store Connect and Google Play field, per locale. Tap any value to copy it, and tick it off as you paste. Character counts are live against each store limit.</p>
    <div class="hero-meta" id="hero-meta"></div>
  </header>

  <div class="overall">
    <div class="overall-top">
      <span class="overall-label">Pasted into the stores</span>
      <span class="overall-count" id="overall-count"></span>
    </div>
    <div class="bar"><span id="overall-bar" style="width:0%"></span></div>
  </div>

  <nav class="locale-nav"><ul id="locale-nav"></ul></nav>

  <div id="panel"></div>

  <footer>
    <span id="foot-note"></span>
    <button class="linkbtn spacer" id="reset-locale">Reset this locale</button>
    <button class="linkbtn" id="reset-all">Reset all</button>
  </footer>

</div>

<div class="toast" id="toast">Copied to clipboard</div>

<script>
const DATA = '''

TAIL = ''';

const FIELDS = DATA.fields;
const LOCALES = DATA.locales;
const STORE_LABEL = { ios: 'App Store Connect', play: 'Google Play Console' };
const KEY = 'quanto-aso-progress-v1';

/* ─── PROGRESS STATE ─── */
let progress = {};
try { progress = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { progress = {}; }

function saveProgress() {
  try { localStorage.setItem(KEY, JSON.stringify(progress)); } catch (e) {}
}
function isDone(code, key) { return !!(progress[code] && progress[code][key]); }
function setDone(code, key, on) {
  if (!progress[code]) progress[code] = {};
  if (on) progress[code][key] = true; else delete progress[code][key];
  if (!Object.keys(progress[code]).length) delete progress[code];
  saveProgress();
}

/* fields that actually exist for a locale (only EN carries kw_gb) */
function fieldsFor(loc) { return FIELDS.filter(f => loc.values[f.key]); }
function doneCount(loc) { return fieldsFor(loc).filter(f => isDone(loc.code, f.key)).length; }

/* ─── RENDER ─── */
let current = LOCALES[0].code;
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

const TICK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';

function countClass(n, limit) {
  if (n > limit) return 'over';
  if (n === limit) return 'max';
  if (n >= limit * 0.9) return 'near';
  return '';
}

function renderHeroMeta() {
  const totalFields = LOCALES.reduce((a, l) => a + fieldsFor(l).length, 0);
  document.getElementById('hero-meta').innerHTML =
    '<span class="pill teal">' + LOCALES.length + ' locales</span>' +
    '<span class="pill">' + totalFields + ' fields</span>' +
    '<span class="pill">Generated ' + esc(DATA.generated) + '</span>';
  document.getElementById('foot-note').textContent =
    DATA.app + ' store metadata — generated ' + DATA.generated + '. Progress is saved in this browser only.';
}

function renderNav() {
  document.getElementById('locale-nav').innerHTML = LOCALES.map(l => {
    const total = fieldsFor(l).length, done = doneCount(l);
    return '<li><button data-locale="' + l.code + '"' +
      ' class="' + (l.code === current ? 'active ' : '') + (done === total ? 'complete' : '') + '">' +
      '<span class="tick"></span><span class="code">' + esc(l.code) + '</span>' +
      '<span>' + done + '/' + total + '</span></button></li>';
  }).join('');
}

function renderOverall() {
  const total = LOCALES.reduce((a, l) => a + fieldsFor(l).length, 0);
  const done  = LOCALES.reduce((a, l) => a + doneCount(l), 0);
  document.getElementById('overall-count').textContent = done + ' / ' + total + ' fields';
  document.getElementById('overall-bar').style.width = (total ? (done / total) * 100 : 0) + '%';
}

function fieldHTML(loc, f) {
  const val = loc.values[f.key];
  const n = val.length;
  const long = n > 400;
  const isKw = f.key.indexOf('kw_') === 0;
  return '' +
    '<div class="field' + (isDone(loc.code, f.key) ? ' is-done' : '') + '" data-key="' + f.key + '">' +
      '<div class="field-top">' +
        '<span class="field-label">' + esc(f.label) + '</span>' +
        (f.indexed ? '<span class="badge idx">indexed</span>' : '') +
        (f.needsNewVersion ? '<span class="badge ver">needs new version</span>' : '') +
        '<span class="count ' + countClass(n, f.limit) + '">' + n + ' / ' + f.limit + '</span>' +
      '</div>' +
      '<button class="field-val' + (isKw ? ' kw' : '') + (long ? ' clamped' : '') + '" data-copy>' + esc(val) + '</button>' +
      '<div class="field-foot">' +
        (long ? '<button class="linkbtn" data-expand>Show full text</button>' : '') +
        '<button class="done-btn" data-done><span class="box">' + TICK + '</span><span>Pasted</span></button>' +
      '</div>' +
    '</div>';
}

function renderPanel() {
  const loc = LOCALES.find(l => l.code === current);
  const fields = fieldsFor(loc);
  const groups = [
    { store: 'ios',  title: 'App Store Connect' },
    { store: 'play', title: 'Google Play Console' }
  ];

  let html =
    '<div class="locale-head">' +
      '<h2>' + esc(loc.language) + '</h2>' +
      '<div class="asc-line">Select <b>' + esc(loc.appStoreLocale) + '</b> in App Store Connect</div>' +
      (loc.note ? '<div class="note">' + esc(loc.note) + '</div>' : '') +
      '<div class="pills">' +
        (loc.status === 'final'
          ? '<span class="pill teal">Final</span>'
          : '<span class="pill warn">Draft — needs native review</span>') +
        '<span class="pill">' + doneCount(loc) + ' / ' + fields.length + ' pasted</span>' +
      '</div>' +
    '</div>';

  groups.forEach(g => {
    const list = fields.filter(f => f.store === g.store);
    if (!list.length) return;
    html += '<section class="section">' +
      '<h3 class="section-title">' + g.title + '<span class="n">' + list.length + ' fields</span></h3>' +
      list.map(f => fieldHTML(loc, f)).join('') +
      '</section>';
  });

  document.getElementById('panel').innerHTML = html;
}

function renderAll() { renderNav(); renderOverall(); renderPanel(); }

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
document.getElementById('locale-nav').addEventListener('click', e => {
  const b = e.target.closest('[data-locale]');
  if (!b) return;
  current = b.getAttribute('data-locale');
  renderAll();
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

document.getElementById('panel').addEventListener('click', async e => {
  const field = e.target.closest('.field');
  if (!field) return;
  const key = field.getAttribute('data-key');
  const loc = LOCALES.find(l => l.code === current);

  if (e.target.closest('[data-expand]')) {
    const val = field.querySelector('.field-val');
    const btn = e.target.closest('[data-expand]');
    const clamped = val.classList.toggle('clamped');
    btn.textContent = clamped ? 'Show full text' : 'Show less';
    return;
  }

  if (e.target.closest('[data-done]')) {
    const on = !isDone(loc.code, key);
    setDone(loc.code, key, on);
    field.classList.toggle('is-done', on);
    renderNav(); renderOverall();
    const head = document.querySelector('.locale-head .pills .pill:last-child');
    if (head) head.textContent = doneCount(loc) + ' / ' + fieldsFor(loc).length + ' pasted';
    return;
  }

  if (e.target.closest('[data-copy]')) {
    const ok = await copyText(loc.values[key]);
    if (!ok) { showToast('Press and hold to copy'); return; }
    const label = FIELDS.find(f => f.key === key).label;
    showToast('Copied ' + label);
    if (!isDone(loc.code, key)) {
      setDone(loc.code, key, true);
      field.classList.add('is-done');
      renderNav(); renderOverall();
      const head = document.querySelector('.locale-head .pills .pill:last-child');
      if (head) head.textContent = doneCount(loc) + ' / ' + fieldsFor(loc).length + ' pasted';
    }
  }
});

document.getElementById('reset-locale').addEventListener('click', () => {
  delete progress[current];
  saveProgress();
  renderAll();
  showToast('Reset ' + current);
});

document.getElementById('reset-all').addEventListener('click', () => {
  progress = {};
  saveProgress();
  renderAll();
  showToast('Reset all locales');
});

renderHeroMeta();
renderAll();
</script>

</body>
</html>
'''

open(OUT, 'w').write(HEAD + payload + TAIL)
print('wrote', OUT)
