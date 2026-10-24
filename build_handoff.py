"""Export the existing report and talk for offline reading; no research modules.

uv sync --frozen --group handoff
uv run --group handoff playwright install chromium
uv run --group handoff python build_handoff.py
python3 build_handoff.py --check  # read-only, standard library only

PDF bytes depend on Chromium/fonts and creation time. The post-hoc export receipt
records exact shipped bytes and inputs; it is not pre-registration evidence.
"""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import html
from importlib.metadata import version
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import quote, unquote, urlsplit

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
RECEIPT = "data/handoff_exports.json"
OUTPUTS = ("REPORT.html", "REPORT.pdf", "PRESENTATION.pdf")
PUBLIC_SOURCE_BASE = "https://github.com/DennisToma/collusion-22-say-vs-do/blob/main/"

CSS = """
:root { font-family:system-ui,sans-serif; color:#17243b; background:#e8edf5 }
* { box-sizing:border-box } body { margin:0 } a { color:#225cb7 }
main { max-width:1100px; margin:30px auto; padding:40px 55px; background:white }
h1 { font-size:30px; line-height:1.2 } h2 { font-size:23px; margin-top:35px }
h3 { font-size:19px; margin-top:28px } h1,h2,h3,h4 { break-after:avoid }
p,li { font-size:16px; line-height:1.55 } li { margin:8px 0 }
img { display:block; max-width:100%; height:auto; margin:15px auto }
.figure { break-inside:avoid }
pre { padding:16px; background:#f2f5f9; white-space:pre-wrap; overflow-wrap:anywhere }
code { font-size:.88em; overflow-wrap:anywhere } blockquote { border-left:3px solid #abc; padding-left:18px }
.table-wrap { overflow-x:auto; margin:16px 0 } table { width:100%; border-collapse:collapse; font-size:13px;
  font-variant-numeric:tabular-nums } th,td { padding:8px; border:1px solid #d7dfeb; text-align:left }
th { background:#f2f5f9 } td { vertical-align:top } .wide table { min-width:1050px }
nav { padding:16px 24px; background:#f2f5f9; border-left:4px solid #225cb7 }
nav p { margin:0 } nav ul { columns:2; padding-left:22px } nav li { font-size:14px; margin:6px 0 }
.export-note { font-size:13px; color:#53647a; overflow-wrap:anywhere }
@media(max-width:650px) { main { margin:0; padding:22px 18px } nav ul { columns:1 } }
@media print {
 @page { size:A4 portrait; margin:17mm 15mm 18mm }
 @page wide { size:A4 landscape; margin:17mm 15mm 18mm }
 :root,body { background:white } main { margin:0; padding:0; max-width:none }
 h1 { font-size:19pt } h2 { font-size:15pt; margin-top:18pt } h3 { font-size:12pt }
 p,li { font-size:10pt; line-height:1.4; orphans:3; widows:3 } li { margin:5pt 0 }
 nav { display:none } .export-note { font-size:8pt }
 img { max-height:120mm; object-fit:contain; margin:8pt auto }
 table { font-size:8pt } th,td { padding:4pt; overflow-wrap:anywhere }
 thead { display:table-header-group } tr { break-inside:avoid }
 .table-wrap { overflow:visible; margin:10pt 0; break-inside:avoid }
 .wide { page:wide; break-before:page; break-after:page }
 .wide table { min-width:0; font-size:8pt; table-layout:fixed }
 .wide th:first-child,.wide td:first-child { width:17% }
 pre { font-size:8pt; padding:8pt } a { color:inherit; text-decoration:none }
}
"""


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs(root):
    # Images are embedded so the HTML is portable as a single file. Only repo-local
    # image paths are accepted; fail rather than publish an incomplete figure.
    names = {"REPORT.md", "PRESENTATION.html", "PRESENTATION.md", "build_presentation.py",
             "build_handoff.py", "pyproject.toml", "uv.lock"}
    for name in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", (root / "REPORT.md").read_text(encoding="utf-8")):
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()) or path.suffix != ".png" or not path.is_file():
            raise ValueError(f"invalid/missing report image: {name}")
        names.add(name)
    return {name: digest(root / name) for name in sorted(names)}


def check(root=ROOT):
    receipt = json.loads((root / RECEIPT).read_text(encoding="utf-8"))
    if receipt["schema_version"] != 1 or receipt["sources_sha256"] != inputs(root):
        raise ValueError("stale handoff inputs; regenerate with build_handoff.py")
    if set(receipt["outputs"]) != set(OUTPUTS):
        raise ValueError("invalid handoff output inventory")
    for name, obj in receipt["outputs"].items():
        if digest(root / name) != obj["sha256"]:
            raise ValueError(f"handoff SHA-256 mismatch: {name}")
    # Also reject stale talk inputs, without requiring any export dependencies.
    from build_presentation import render
    for name, content in render(root).items():
        if (root / name).read_bytes() != content.encode("utf-8"):
            raise ValueError(f"stale presentation: {name}")
    return receipt


def render_report(root=ROOT):
    from markdown_it import MarkdownIt
    from markdown_it.token import Token
    md = MarkdownIt("commonmark", {"html": False}).enable("table").enable("strikethrough")
    text = (root / "REPORT.md").read_text(encoding="utf-8")
    tokens = md.parse(text)
    headings, cells, image_names, fragments = [], [], [], []
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            slug = f"section-{len(headings) + 1}"
            token.attrSet("id", slug)
            headings.append((int(token.tag[1]), slug, "".join(
                c.content for c in tokens[i + 1].children if c.type in ("text", "code_inline"))))
        if token.type in ("td_open", "th_open"):
            cells.append("".join(c.content for c in tokens[i + 1].children
                                 if c.type in ("text", "code_inline")))
        if token.type == "fence":
            fragments.append(token.content)
        if token.type == "inline":
            fragments.append("".join(c.content for c in token.children
                                     if c.type in ("text", "code_inline")))
        if token.children:
            for child in token.children:
                if child.type == "image":
                    name = child.attrGet("src")
                    image_names.append(name)
                    child.attrSet("src", "data:image/png;base64," +
                                  base64.b64encode((root / name).read_bytes()).decode())
                    if i and tokens[i - 1].type == "paragraph_open":
                        tokens[i - 1].attrSet("class", "figure")
    # Keep each wide table's label (and immediately preceding section heading)
    # on the same landscape PDF page, avoiding empty portrait transition pages.
    opens, closes = set(), set()
    for idx, token in enumerate(tokens):
        if token.type != "table_open":
            continue
        row_end = next(j for j in range(idx + 1, len(tokens)) if tokens[j].type == "tr_close")
        if sum(t.type == "th_open" for t in tokens[idx:row_end]) <= 6:
            continue
        start = idx
        if start >= 3 and tokens[start - 1].type == "paragraph_close":
            start -= 3
        if start >= 3 and tokens[start - 1].type == "heading_close":
            start -= 3
        opens.add(start)
        closes.add(next(j for j in range(idx + 1, len(tokens)) if tokens[j].type == "table_close"))
    wrapped = []
    for idx, token in enumerate(tokens):
        if idx in opens:
            wrapped.append(Token("handoff_wide_open", "section", 1))
        wrapped.append(token)
        if idx in closes:
            wrapped.append(Token("handoff_wide_close", "section", -1))
    md.renderer.rules["handoff_wide_open"] = lambda *_: '<section class="wide">'
    md.renderer.rules["handoff_wide_close"] = lambda *_: '</section>'
    md.renderer.rules["table_open"] = lambda *_: '<div class="table-wrap"><table>\n'
    md.renderer.rules["table_close"] = lambda *_: "</table></div>\n"
    toc = "".join(f'<li><a href="#{slug}">{html.escape(title)}</a></li>'
                  for level, slug, title in headings if level == 2)
    body = md.renderer.render(wrapped, md.options, {})
    source_hash = digest(root / "REPORT.md")
    document = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<title>Say vs. Do — research report</title><style>' + CSS + '</style></head><body><main>'
                '<p class="export-note">Offline rendering of REPORT.md. Figures are embedded; '
                'source links are local in HTML and point to GitHub in PDF. No results recomputed.<br>'
                f'Source SHA-256: {source_hash}</p><nav aria-label="Contents"><p><strong>Contents</strong></p><ul>' +
                toc + '</ul></nav>' + body + '</main></body></html>\n')
    return document, headings, cells, image_names, fragments


def normalize(text):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text)).replace("\u00ad", "")


def prepare_pdf_links(page, root):
    """Use portable GitHub links in the PDF without changing the offline HTML.

    This changes anchor targets in the print document only. It fetches nothing.
    The post-hoc receipt identifies the exact sources independently of main.
    """
    links = page.locator("a[href]").evaluate_all(
        "ns => ns.map(n => ({raw:n.getAttribute('href'), resolved:n.href}))")
    replacements = {}
    for link in links:
        uri = urlsplit(link["resolved"])
        if uri.scheme != "file" or link["raw"].startswith("#"):
            continue
        target = Path(unquote(uri.path)).resolve()
        if not target.is_relative_to(root.resolve()):
            raise ValueError(f"PDF links outside repository: {target}")
        relative = target.relative_to(root.resolve()).as_posix()
        suffix = ("#" + uri.fragment) if uri.fragment else ""
        replacements[link["resolved"]] = PUBLIC_SOURCE_BASE + quote(relative) + suffix
    page.locator("a[href]").evaluate_all("""(ns, replacements) => ns.forEach(n => {
        if (replacements[n.href]) n.href = replacements[n.href];
    })""", replacements)


def export(root=ROOT):
    from playwright.sync_api import sync_playwright
    from pypdf import PdfReader
    # Fail before producing anything if the talk or image inputs are stale.
    source_hashes = inputs(root)
    from build_presentation import render
    for name, content in render(root).items():
        if (root / name).read_bytes() != content.encode("utf-8"):
            raise ValueError(f"stale presentation: {name}")
    document, headings, cells, images, fragments = render_report(root)
    (root / "REPORT.html").write_text(document, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(java_script_enabled=False)
        # Rendering is offline. Never fetch fonts, web assets, or other URLs.
        context.route(re.compile(r"^https?://"), lambda route: route.abort())
        page = context.new_page()
        page.goto((root / "REPORT.html").as_uri(), wait_until="load")
        if not page.locator("img").evaluate_all("ns => ns.every(n => n.complete && n.naturalWidth > 0)"):
            raise ValueError("report image failed to load")
        prepare_pdf_links(page, root)
        page.pdf(path=str(root / "REPORT.pdf"), prefer_css_page_size=True, print_background=True,
                 display_header_footer=True, header_template="<span></span>",
                 footer_template='<div style="width:100%;text-align:center;font-size:8px;color:#53647a">'
                                 'Say vs. Do · <span class="pageNumber"></span> / '
                                 '<span class="totalPages"></span></div>')
        page.goto((root / "PRESENTATION.html").as_uri(), wait_until="load")
        page.emulate_media(media="print")
        slide_titles = page.locator("section.slide h1").all_text_contents()
        slide_fragments = page.locator("section.slide").evaluate_all("""slides => slides.map(s =>
            Array.from(s.querySelectorAll('h1,p,li,th,td,svg text'))
            .filter(n => n.getClientRects().length && getComputedStyle(n).visibility !== 'hidden')
            .map(n => n.textContent))""")
        prepare_pdf_links(page, root)
        page.pdf(path=str(root / "PRESENTATION.pdf"), prefer_css_page_size=True, print_background=True)
        chromium = browser.version
        browser.close()
    report = PdfReader(root / "REPORT.pdf")
    report_text = normalize(re.sub(r"Say vs\. Do · \d+ / \d+", "",
                                   "\n".join(page.extract_text() for page in report.pages)))
    # These are rendering checks against the source, not metric calculations.
    for cell in cells:
        if normalize(cell) not in report_text:
            raise ValueError(f"report PDF lost table cell: {cell}")
    for _, _, title in headings:
        if normalize(title) not in report_text:
            raise ValueError(f"report PDF lost heading: {title}")
    for fragment in fragments:
        if normalize(fragment) not in report_text:
            raise ValueError(f"report PDF lost text: {fragment[:100]}")
    talk = PdfReader(root / "PRESENTATION.pdf")
    if len(talk.pages) != len(slide_titles):
        raise ValueError(f"talk PDF has {len(talk.pages)} pages for {len(slide_titles)} slides")
    for page, title, fragments_for_slide in zip(talk.pages, slide_titles, slide_fragments):
        text_for_slide = normalize(page.extract_text()).casefold()
        if normalize(title).casefold() not in text_for_slide:
            raise ValueError(f"talk PDF slide lost or split: {title}")
        for fragment in fragments_for_slide:
            if normalize(fragment).casefold() not in text_for_slide:
                raise ValueError(f"talk PDF lost visible text on {title}: {fragment[:100]}")
    if inputs(root) != source_hashes:
        raise ValueError("handoff sources changed during export")
    receipt = {"schema_version": 1, "recorded_utc": datetime.now(timezone.utc).isoformat(),
               "note": "Post-hoc rendering provenance only, not pre-registration. PDF bytes vary with renderer/time.",
               "pdf_source_link_base": PUBLIC_SOURCE_BASE,
               "sources_sha256": source_hashes,
               "renderer": {"chromium": chromium,
                            **{n: version(n) for n in ("markdown-it-py", "playwright", "pypdf")}},
               "checks": {"report_pages": len(report.pages), "report_headings": len(headings),
                          "report_table_cells": len(cells), "report_text_fragments": len(fragments),
                          "embedded_figures": len(images),
                          "presentation_pages": len(talk.pages),
                          "presentation_text_fragments": sum(map(len, slide_fragments))},
               "outputs": {name: {"sha256": digest(root / name), "bytes": (root / name).stat().st_size}
                           for name in OUTPUTS}}
    (root / RECEIPT).write_text(json.dumps(receipt, indent=2) + "\n")
    check(root)
    print("PASS: exported offline HTML/PDF; " + json.dumps(receipt["checks"]) + "; no metrics recomputed.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="read-only input/output hash check; stdlib only")
    args = ap.parse_args()
    try:
        if args.check:
            receipt = check()
            print("PASS: offline handoff inputs/outputs match post-hoc receipt (read-only); " +
                  json.dumps(receipt["checks"]))
        else:
            export()
    except (ValueError, KeyError, OSError) as exc:
        raise SystemExit(f"FAIL: {exc}")


if __name__ == "__main__":
    main()
