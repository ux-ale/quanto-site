#!/usr/bin/env python3
"""
Builds quanto.app/privacy-policy/ and quanto.app/terms-of-use/ from the JSON
sources in legal-src/content/.

Each page is a single self-contained HTML file: English is rendered statically
into the document (so it works without JS and is what crawlers read), and every
translation is embedded as pre-rendered HTML that the language switcher swaps in.

Usage:  python3 legal-src/build.py
"""

import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONTENT = ROOT / "legal-src" / "content"

# Order matters: this is the order of the language menu.
LANGS = [
    ("en", "English",          "English"),
    ("de", "German",           "Deutsch"),
    ("fr", "French",           "Français"),
    ("es", "Spanish",          "Español"),
    ("it", "Italian",          "Italiano"),
    ("pt", "Portuguese (BR)",  "Português"),
    ("tr", "Turkish",          "Türkçe"),
    ("id", "Indonesian",       "Bahasa Indonesia"),
    ("ms", "Malay",            "Bahasa Melayu"),
    ("ja", "Japanese",         "日本語"),
    ("ko", "Korean",           "한국어"),
    ("nl", "Dutch",            "Nederlands"),
    ("pl", "Polish",           "Polski"),
]
LANG_CODES = [c for c, _, _ in LANGS]

DOCS = {
    "privacy": {"slug": "privacy-policy", "other": "terms",   "ui_title": "privacyTitle"},
    "terms":   {"slug": "terms-of-use",   "other": "privacy", "ui_title": "termsTitle"},
}

SITE = "https://quanto.app"


# ---------------------------------------------------------------- inline text

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")

NBSP = "\u00a0"

# French typography wants an unbreakable space before : ; ! ? and % and inside
# guillemets. The content files are written with ordinary spaces; this puts the
# right character in so the punctuation never wraps to the next line.
FR_TYPO = [
    (" :", NBSP + ":"),
    (" ;", NBSP + ";"),
    (" !", NBSP + "!"),
    (" ?", NBSP + "?"),
    (" %", NBSP + "%"),
    ("\u00ab ", "\u00ab" + NBSP),
    (" \u00bb", NBSP + "\u00bb"),
]

_typo = None  # set per language by build()


def typo(text):
    if _typo == "fr":
        for a, b in FR_TYPO:
            text = text.replace(a, b)
    return text


def inline(text):
    """Escape, then apply the tiny subset of markdown the content files use."""
    out = html.escape(typo(text), quote=False)
    out = LINK_RE.sub(
        lambda m: '<a href="%s">%s</a>' % (html.escape(m.group(2), quote=True), m.group(1)),
        out,
    )
    out = BOLD_RE.sub(r"<strong>\1</strong>", out)
    return out


# ------------------------------------------------------------------ rendering

def render_blocks(blocks):
    parts = []
    for b in blocks:
        t = b["t"]
        if t == "p":
            parts.append("<p>%s</p>" % inline(b["x"]))
        elif t == "h3":
            parts.append("<h3>%s</h3>" % inline(b["x"]))
        elif t == "ul":
            items = "".join("<li>%s</li>" % inline(i) for i in b["items"])
            parts.append("<ul>%s</ul>" % items)
        elif t == "dl":
            rows = "".join(
                "<div class=\"fact\"><dt>%s</dt><dd>%s</dd></div>" % (inline(k), inline(v))
                for k, v in b["items"]
            )
            parts.append("<dl class=\"facts\">%s</dl>" % rows)
        else:
            raise ValueError("unknown block type: %r" % t)
    return "".join(parts)


def render_article(doc):
    out = []
    for i, sec in enumerate(doc["sections"], start=1):
        out.append(
            '<section class="sec" id="s%d">'
            '<h2><span class="sec-n" aria-hidden="true">%d</span>'
            '<span class="sec-t">%s</span></h2>'
            "%s</section>"
            % (i, i, inline(sec["heading"]), render_blocks(sec["blocks"]))
        )
    return "".join(out)


def render_toc(doc):
    items = "".join(
        '<li><a href="#s%d"><span class="toc-n">%d</span>%s</a></li>'
        % (i, i, inline(sec["heading"]))
        for i, sec in enumerate(doc["sections"], start=1)
    )
    return "<ol class=\"toc-list\">%s</ol>" % items


# -------------------------------------------------------------------- assets

CSS = r"""
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --bg:#0C0F11;
  --sem-5:rgba(255,255,255,0.05);
  --sem-8:rgba(255,255,255,0.08);
  --sem-15:rgba(255,255,255,0.15);
  --border:rgba(255,255,255,0.08);
  --border-strong:rgba(255,255,255,0.15);
  --brand:#0cbba1;
  --text-1:#ffffff;
  --text-2:rgba(255,255,255,0.72);
  --text-3:rgba(255,255,255,0.45);
  --text-4:rgba(255,255,255,0.30);
  --head-h:60px;
}

html,body{margin:0;min-height:100%;background:var(--bg);overscroll-behavior:none}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}

body::before{
  content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(180deg,#283339 0%,#0C0F11 55%);
}

body{
  font-family:'Sora',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  color:var(--text-1);font-weight:300;line-height:1.7;
  -webkit-font-smoothing:antialiased;
  background:transparent;
}

a{color:inherit}
a:focus-visible,button:focus-visible{outline:2px solid var(--brand);outline-offset:3px;border-radius:6px}

/* ---------------------------------------------------------------- header */

.head{
  position:sticky;top:0;z-index:50;height:var(--head-h);
  display:flex;align-items:center;gap:16px;
  padding:0 20px;border-bottom:1px solid var(--border);
  background:rgba(12,15,17,0.72);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
}
.head-in{
  width:100%;max-width:1040px;margin:0 auto;
  display:flex;align-items:center;justify-content:space-between;gap:16px;
}
.brand{display:inline-flex;align-items:center;gap:10px;text-decoration:none}
.brand img{width:28px;height:28px;border-radius:7px;display:block}
.brand span{font-size:15px;font-weight:600;letter-spacing:-0.01em}

/* ------------------------------------------------------- language switch */

.lang{position:relative}
.lang-btn{
  display:inline-flex;align-items:center;gap:8px;cursor:pointer;
  font-family:inherit;font-size:13px;font-weight:400;color:var(--text-1);
  background:var(--sem-5);border:1px solid var(--border);border-radius:100px;
  padding:7px 12px 7px 11px;transition:background .2s ease,border-color .2s ease;
}
.lang-btn:hover{background:var(--sem-8);border-color:var(--border-strong)}
.lang-btn svg{flex:none}
.lang-btn .chev{transition:transform .2s ease;opacity:.5}
.lang[data-open="true"] .lang-btn .chev{transform:rotate(180deg)}

.lang-menu{
  position:absolute;top:calc(100% + 8px);right:0;z-index:60;
  min-width:210px;max-height:min(78vh,560px);overflow-y:auto;overscroll-behavior:contain;
  padding:6px;border-radius:16px;
  background:#1e252b;border:1px solid var(--border-strong);
  box-shadow:0 24px 60px rgba(0,0,0,0.55);
  display:none;
}
.lang[data-open="true"] .lang-menu{display:block}
.lang-menu button{
  display:flex;align-items:center;justify-content:space-between;gap:12px;
  width:100%;cursor:pointer;text-align:left;
  font-family:inherit;font-size:14px;font-weight:400;color:var(--text-2);
  background:none;border:0;border-radius:10px;padding:9px 12px;
}
.lang-menu button:hover{background:var(--sem-8);color:var(--text-1)}
.lang-menu button[aria-current="true"]{color:var(--brand);font-weight:600}
.lang-menu button[aria-current="true"]::after{content:"";width:6px;height:6px;border-radius:50%;background:var(--brand);flex:none}

/* ------------------------------------------------------------------ page */

.wrap{max-width:1040px;margin:0 auto;padding:0 20px}

.doc-head{padding:56px 0 40px;border-bottom:1px solid var(--border)}
.eyebrow{
  font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;
  color:var(--brand);margin-bottom:14px;
}
h1{font-size:40px;font-weight:700;line-height:1.15;letter-spacing:-0.025em}
.updated{
  display:inline-block;margin-top:16px;padding:5px 12px;border-radius:100px;
  background:var(--sem-5);border:1px solid var(--border);
  font-size:12px;font-weight:400;color:var(--text-3);
}
.updated:empty{display:none}
.intro{margin-top:20px;max-width:62ch;font-size:16px;color:var(--text-2)}

.cols{display:grid;grid-template-columns:1fr;gap:0;padding:40px 0 72px}

/* ------------------------------------------------------------------- toc */

.toc{margin-bottom:36px}
.toc-head{
  display:flex;align-items:center;justify-content:space-between;gap:12px;width:100%;
  font-family:inherit;font-size:12px;font-weight:600;letter-spacing:0.08em;
  text-transform:uppercase;color:var(--text-3);
  background:var(--sem-5);border:1px solid var(--border);border-radius:12px;
  padding:12px 14px;cursor:pointer;
}
.toc-head .chev{transition:transform .2s ease;opacity:.6}
.toc[data-open="true"] .toc-head .chev{transform:rotate(180deg)}
.toc-list{list-style:none;display:none;margin-top:10px}
.toc[data-open="true"] .toc-list{display:block}
.toc-list a{
  display:flex;gap:10px;text-decoration:none;color:var(--text-3);
  font-size:13px;line-height:1.5;padding:8px 12px;border-radius:10px;
}
.toc-list a:hover{color:var(--text-1);background:var(--sem-5)}
.toc-list a.on{color:var(--brand);background:var(--sem-8)}
.toc-n{color:var(--text-4);font-variant-numeric:tabular-nums;flex:none;min-width:14px}
.toc-list a.on .toc-n{color:var(--brand)}

/* --------------------------------------------------------------- article */

.doc{max-width:68ch}
.sec{scroll-margin-top:calc(var(--head-h) + 20px)}
.sec + .sec{margin-top:44px}
.sec h2{
  display:flex;align-items:baseline;gap:12px;
  font-size:21px;font-weight:600;line-height:1.35;letter-spacing:-0.015em;
  margin-bottom:16px;
}
.sec-n{
  flex:none;min-width:26px;height:26px;padding:0 7px;
  display:inline-flex;align-items:center;justify-content:center;
  border-radius:8px;background:rgba(12,187,161,0.12);color:var(--brand);
  font-size:12px;font-weight:600;font-variant-numeric:tabular-nums;
  transform:translateY(-2px);
}
.sec h3{
  font-size:15px;font-weight:600;color:var(--text-1);
  margin:24px 0 10px;letter-spacing:-0.005em;
}
.sec p{font-size:15px;color:var(--text-2);margin-bottom:14px}
.sec p:last-child{margin-bottom:0}
.sec a{color:var(--brand);text-decoration:none;border-bottom:1px solid rgba(12,187,161,0.35)}
.sec a:hover{border-bottom-color:var(--brand)}
.sec strong{font-weight:600;color:var(--text-1)}

.sec ul{list-style:none;margin:0 0 16px;padding:0}
.sec ul li{position:relative;padding-left:20px;font-size:15px;color:var(--text-2);margin-bottom:9px}
.sec ul li::before{
  content:"";position:absolute;left:2px;top:12px;
  width:5px;height:5px;border-radius:50%;background:var(--brand);opacity:.75;
}
.sec ul li:last-child{margin-bottom:0}

.facts{
  margin:0 0 16px;border:1px solid var(--border);border-radius:14px;
  background:var(--sem-5);overflow:hidden;
}
.fact{display:flex;flex-wrap:wrap;gap:4px 14px;padding:12px 16px}
.fact + .fact{border-top:1px solid var(--border)}
.fact dt{flex:none;min-width:132px;font-size:13px;color:var(--text-3)}
.fact dd{font-size:14px;color:var(--text-1);font-weight:400}

/* ---------------------------------------------------------------- footer */

.foot{border-top:1px solid var(--border);padding:32px 0 48px}
.foot-in{
  max-width:1040px;margin:0 auto;padding:0 20px;
  display:flex;flex-wrap:wrap;align-items:center;gap:12px 24px;
}
.foot a{
  font-size:13px;color:var(--text-3);text-decoration:none;
  transition:color .2s ease;
}
.foot a:hover{color:var(--text-1)}
.foot .spacer{flex:1 1 auto}
.foot p{font-size:12px;color:var(--text-4)}

/* ----------------------------------------------------------------- ≥900px */

@media (min-width:900px){
  .head,.wrap,.foot-in{padding-left:32px;padding-right:32px}
  h1{font-size:48px}
  .doc-head{padding:72px 0 48px}
  .cols{grid-template-columns:236px minmax(0,1fr);gap:64px;padding:48px 0 96px}
  .toc{margin-bottom:0}
  .toc-inner{position:sticky;top:calc(var(--head-h) + 32px);max-height:calc(100vh - var(--head-h) - 64px);overflow-y:auto}
  .toc-head{display:none}
  .toc-list{display:block !important;margin-top:0}
}

@media (max-width:480px){
  h1{font-size:30px}
  .doc-head{padding:40px 0 32px}
  .lang-btn{padding:7px 11px;font-size:12px}
  .lang-btn .lang-name{max-width:38vw;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .lang-menu{min-width:min(78vw,240px)}
}

@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *{transition:none !important}
}
"""

JS = r"""
(function () {
  var DATA = __DATA__;
  var SLUG = "__SLUG__";
  var OTHER_SLUG = "__OTHER_SLUG__";
  var CODES = __CODES__;
  var STORE = "quanto-legal-lang";

  var el = {
    html: document.documentElement,
    desc: document.querySelector('meta[name="description"]'),
    h1: document.getElementById("doc-title"),
    updated: document.getElementById("doc-updated"),
    intro: document.getElementById("doc-intro"),
    article: document.getElementById("doc-body"),
    toc: document.getElementById("toc"),
    tocList: document.getElementById("toc-list"),
    tocHead: document.getElementById("toc-head"),
    tocLabel: document.getElementById("toc-label"),
    eyebrow: document.getElementById("eyebrow"),
    lang: document.getElementById("lang"),
    langBtn: document.getElementById("lang-btn"),
    langName: document.getElementById("lang-name"),
    langMenu: document.getElementById("lang-menu"),
    footOther: document.getElementById("foot-other"),
    footHome: document.getElementById("foot-home"),
    footRights: document.getElementById("foot-rights")
  };

  function store(v) {
    try { localStorage.setItem(STORE, v); } catch (e) {}
  }
  function stored() {
    try { return localStorage.getItem(STORE); } catch (e) { return null; }
  }

  /* Pick a language: ?lang= wins, then a stored choice, then the browser. */
  function detect() {
    var q = new URLSearchParams(location.search).get("lang");
    if (q && CODES.indexOf(q) > -1) return q;
    var s = stored();
    if (s && CODES.indexOf(s) > -1) return s;
    var prefs = navigator.languages || [navigator.language || ""];
    for (var i = 0; i < prefs.length; i++) {
      var base = String(prefs[i]).toLowerCase().split("-")[0];
      if (CODES.indexOf(base) > -1) return base;
    }
    return "en";
  }

  var spy = null;

  function watchSections() {
    if (spy) spy.disconnect();
    var links = el.tocList.querySelectorAll("a");
    if (!links.length || !("IntersectionObserver" in window)) return;
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (a) { a.classList.remove("on"); });
        var a = map[entry.target.id];
        if (a) a.classList.add("on");
      });
    }, { rootMargin: "-80px 0px -70% 0px", threshold: 0 });
    el.article.querySelectorAll(".sec").forEach(function (s) { spy.observe(s); });
  }

  function apply(code, pushUrl) {
    var d = DATA[code];
    if (!d) return;

    el.html.setAttribute("lang", d.htmlLang);
    document.title = d.pageTitle;
    if (el.desc) el.desc.setAttribute("content", d.description);

    el.eyebrow.textContent = d.ui.eyebrow;
    el.h1.textContent = d.title;
    el.updated.textContent = d.updated || "";
    el.intro.innerHTML = d.intro;
    el.article.innerHTML = d.article;
    el.tocList.innerHTML = d.tocList;
    el.tocLabel.textContent = d.ui.toc;

    el.langName.textContent = d.native;
    el.langBtn.setAttribute("aria-label", d.ui.language + ": " + d.native);

    var qs = code === "en" ? "" : "?lang=" + code;
    el.footOther.textContent = d.ui.otherTitle;
    el.footOther.href = "/" + OTHER_SLUG + "/" + qs;
    el.footHome.textContent = d.ui.backToSite;
    el.footRights.textContent = d.ui.rights;

    el.langMenu.querySelectorAll("button").forEach(function (b) {
      b.setAttribute("aria-current", b.dataset.code === code ? "true" : "false");
    });

    if (pushUrl) {
      history.replaceState(null, "", "/" + SLUG + "/" + qs + location.hash);
    }
    watchSections();
  }

  /* --- language menu ---------------------------------------------------- */

  function openMenu(open) {
    el.lang.dataset.open = open ? "true" : "false";
    el.langBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  el.langBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    openMenu(el.lang.dataset.open !== "true");
  });
  el.langMenu.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    var code = b.dataset.code;
    store(code);
    apply(code, true);
    openMenu(false);
    el.langBtn.focus();
  });
  document.addEventListener("click", function () { openMenu(false); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && el.lang.dataset.open === "true") {
      openMenu(false);
      el.langBtn.focus();
    }
  });

  /* --- mobile table of contents ----------------------------------------- */

  el.tocHead.addEventListener("click", function () {
    var open = el.toc.dataset.open !== "true";
    el.toc.dataset.open = open ? "true" : "false";
    el.tocHead.setAttribute("aria-expanded", open ? "true" : "false");
  });
  el.tocList.addEventListener("click", function (e) {
    if (e.target.closest("a") && window.matchMedia("(max-width:899px)").matches) {
      el.toc.dataset.open = "false";
      el.tocHead.setAttribute("aria-expanded", "false");
    }
  });

  /* --- boot -------------------------------------------------------------- */

  var initial = detect();
  if (initial === "en") {
    /* English is already in the document; just sync the URL and the menu. */
    apply("en", new URLSearchParams(location.search).has("lang"));
  } else {
    apply(initial, true);
  }
})();
"""


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{PAGE_TITLE}}</title>
<meta name="description" content="{{DESCRIPTION}}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{{SITE}}/{{SLUG}}/">
{{ALTERNATES}}
<link rel="icon" type="image/png" href="/quanto-app-icon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="{{PAGE_TITLE}}">
<meta property="og:description" content="{{DESCRIPTION}}">
<meta property="og:url" content="{{SITE}}/{{SLUG}}/">
<meta property="og:image" content="{{SITE}}/quanto-app-icon.png">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>{{CSS}}</style>
</head>
<body>

<header class="head">
  <div class="head-in">
    <a class="brand" href="/">
      <img src="/quanto-app-icon.png" alt="" width="28" height="28">
      <span>Quanto</span>
    </a>

    <div class="lang" id="lang" data-open="false">
      <button class="lang-btn" id="lang-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="Language: English">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
          <circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18"/>
        </svg>
        <span class="lang-name" id="lang-name">English</span>
        <svg class="chev" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true">
          <path d="M6 9l6 6 6-6"/>
        </svg>
      </button>
      <div class="lang-menu" id="lang-menu" role="menu">{{LANG_BUTTONS}}</div>
    </div>
  </div>
</header>

<main class="wrap">
  <div class="doc-head">
    <p class="eyebrow" id="eyebrow">{{EYEBROW}}</p>
    <h1 id="doc-title">{{TITLE}}</h1>
    <p class="updated" id="doc-updated">{{UPDATED}}</p>
    <p class="intro" id="doc-intro">{{INTRO}}</p>
  </div>

  <div class="cols">
    <aside class="toc" id="toc" data-open="false">
      <div class="toc-inner">
        <button class="toc-head" id="toc-head" type="button" aria-expanded="false" aria-controls="toc-list">
          <span id="toc-label">{{TOC_LABEL}}</span>
          <svg class="chev" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true">
            <path d="M6 9l6 6 6-6"/>
          </svg>
        </button>
        <nav id="toc-list" aria-labelledby="toc-label">{{TOC}}</nav>
      </div>
    </aside>

    <article class="doc" id="doc-body">{{ARTICLE}}</article>
  </div>
</main>

<footer class="foot">
  <div class="foot-in">
    <a id="foot-other" href="/{{OTHER_SLUG}}/">{{OTHER_TITLE}}</a>
    <a id="foot-home" href="/">{{BACK_TO_SITE}}</a>
    <span class="spacer"></span>
    <p id="foot-rights">{{RIGHTS}}</p>
  </div>
</footer>

<script>{{JS}}</script>
</body>
</html>
"""


def load(name):
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def build(kind):
    cfg = DOCS[kind]
    slug, other_slug = cfg["slug"], DOCS[cfg["other"]]["slug"]

    data = {}
    missing = []
    for code, _en_name, native in LANGS:
        if not (CONTENT / ("%s.%s.json" % (kind, code))).exists():
            missing.append(code)
            continue
        doc = load("%s.%s.json" % (kind, code))
        ui = load("ui.%s.json" % code)
        globals()["_typo"] = doc.get("htmlLang", code)
        article = render_article(doc)
        toc = render_toc(doc)
        data[code] = {
            "htmlLang": doc.get("htmlLang", code),
            "native": native,
            "title": typo(doc["title"]),
            "pageTitle": "%s — Quanto" % doc["title"],
            "description": typo(doc["description"]),
            "updated": typo(doc.get("updated") or ""),
            "intro": inline(doc["intro"]),
            "article": article,
            "tocList": toc,
            "ui": {
                "eyebrow": ui["eyebrow"],
                "toc": ui["toc"],
                "language": ui["language"],
                "otherTitle": ui[DOCS[cfg["other"]]["ui_title"]],
                "backToSite": ui["backToSite"],
                "rights": ui["rights"],
            },
        }

    en = data["en"]
    if missing:
        print("  !! missing translations for %s: %s" % (kind, ", ".join(missing)))

    alternates = "\n".join(
        '<link rel="alternate" hreflang="%s" href="%s/%s/%s">'
        % (data[c]["htmlLang"], SITE, slug, "" if c == "en" else "?lang=" + c)
        for c in LANG_CODES if c in data
    )
    alternates += '\n<link rel="alternate" hreflang="x-default" href="%s/%s/">' % (SITE, slug)

    lang_buttons = "".join(
        '<button type="button" role="menuitem" data-code="%s" aria-current="%s">%s</button>'
        % (c, "true" if c == "en" else "false", html.escape(native, quote=False))
        for c, _n, native in LANGS if c in data
    )

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")  # never break out of <script>

    js = (
        JS.replace("__DATA__", payload)
        .replace("__SLUG__", slug)
        .replace("__OTHER_SLUG__", other_slug)
        .replace("__CODES__", json.dumps([c for c in LANG_CODES if c in data]))
    )

    page = PAGE
    for key, value in [
        ("{{PAGE_TITLE}}", html.escape(en["pageTitle"], quote=True)),
        ("{{DESCRIPTION}}", html.escape(en["description"], quote=True)),
        ("{{SITE}}", SITE),
        ("{{SLUG}}", slug),
        ("{{OTHER_SLUG}}", other_slug),
        ("{{ALTERNATES}}", alternates),
        ("{{CSS}}", CSS.strip()),
        ("{{LANG_BUTTONS}}", lang_buttons),
        ("{{EYEBROW}}", html.escape(en["ui"]["eyebrow"], quote=False)),
        ("{{TITLE}}", html.escape(en["title"], quote=False)),
        ("{{UPDATED}}", html.escape(en["updated"], quote=False)),
        ("{{INTRO}}", en["intro"]),
        ("{{TOC_LABEL}}", html.escape(en["ui"]["toc"], quote=False)),
        ("{{TOC}}", en["tocList"]),
        ("{{ARTICLE}}", en["article"]),
        ("{{OTHER_TITLE}}", html.escape(en["ui"]["otherTitle"], quote=False)),
        ("{{BACK_TO_SITE}}", html.escape(en["ui"]["backToSite"], quote=False)),
        ("{{RIGHTS}}", html.escape(en["ui"]["rights"], quote=False)),
        ("{{JS}}", js),
    ]:
        page = page.replace(key, value)

    out_dir = ROOT / slug
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "index.html"
    out.write_text(page, encoding="utf-8")
    print("built %s  (%d languages, %.1f KB)" % (out.relative_to(ROOT), len(data), len(page) / 1024))


if __name__ == "__main__":
    for kind in DOCS:
        build(kind)
