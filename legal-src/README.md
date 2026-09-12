# Legal pages

Source for `quanto.app/privacy-policy/` and `quanto.app/terms-of-use/`.

Both pages are generated. **Edit the JSON in `content/`, never the built
`index.html`** — a rebuild overwrites it.

```
python3 legal-src/build.py
```

## Layout

```
content/
  privacy.<lang>.json   the Privacy Policy in that language
  terms.<lang>.json     the Terms of Use in that language
  ui.<lang>.json        page furniture (nav labels, footer, TOC heading)
build.py                generates ../privacy-policy/ and ../terms-of-use/
```

13 languages, matching the locales in the *Quanto - Localisation* sheet, with
the two Spanish locales merged into one (they differ only in number and
currency formatting, which does not affect prose):

`en` `de` `fr` `es` `it` `pt` (pt-BR) `tr` `id` `ms` `ja` `ko` `nl` `pl`

English is the source of truth. Every translation must keep the same section
order and the same block structure — `build.py` renders the table of contents
and anchors (`#s1`…`#sN`) from that structure, and the anchors are shared
across languages so a deep link survives a language switch.

## Content format

A document is a list of sections; each section has a `heading` and `blocks`:

| block | shape | renders as |
|-------|-------|-----------|
| `{"t":"p","x":"…"}` | paragraph | `<p>` |
| `{"t":"h3","x":"…"}` | sub-heading | `<h3>` |
| `{"t":"ul","items":[…]}` | list | bulleted list |
| `{"t":"dl","items":[["key","value"],…]}` | fact table | the boxed key/value card |

Inside any string: `**bold**` and `[text](url)` work. Everything else is
escaped, so text is safe to paste in as-is.

`"updated"` is shown as the pill under the title. Leave it `""` to hide the
pill — the Terms of Use has no date in the source document.

## Adding a language

1. Copy `privacy.en.json`, `terms.en.json` and `ui.en.json` to the new code.
2. Translate the values, keeping the structure identical.
3. Add the code to `LANGS` in `build.py` with its endonym (the name as written
   in that language — "Deutsch", not "German").
4. Rebuild.

## How the page works

Each page is one self-contained HTML file. English is written into the
document statically, so the page works with JavaScript off and is what
crawlers read; the other twelve are embedded as pre-rendered HTML that the
switcher swaps in. The chosen language goes in `?lang=xx`, is remembered in
`localStorage`, and is otherwise guessed once from the browser's
`navigator.languages`. `hreflang` alternates are emitted for all 13.
