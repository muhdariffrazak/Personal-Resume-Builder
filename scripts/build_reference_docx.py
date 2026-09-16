#!/usr/bin/env python3
"""
One-time generator for templates/reference.docx, pandoc's "reference doc"
mechanism for styling the .docx output. Starts from pandoc's own default
reference.docx (a .docx is just a zip of XML — no Word/LibreOffice needed)
and edits word/styles.xml to add an ATS-safe (single-column, no tables)
typographic scale:
  - Title: bold blue, large (unused directly, kept as a sane fallback)
  - Heading 1: gray, bold, caps, bottom border (section headings)
  - ResumeName: bold blue, large (the name header line)
  - EntryHeader: bold, with space before each entry for visual separation

OOXML's schema requires style/pPr children in a strict sequence — this script
inserts new elements at the schema-correct position (not just appended) so
Word opens the result without a "repair" prompt.

Requires pandoc on PATH (run inside the Docker build container).
Usage: python3 scripts/build_reference_docx.py
"""
import subprocess
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "templates" / "reference.docx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W_NS)

# Colors sampled from the coach's Word template (1 - Resume Building Tool_V8.pdf)
BLUE = "1F4E79"
GRAY = "808080"

# Typographic scale (half-points = pt * 2), matching templates/resume.latex:
# body 9pt -> entry title 12pt -> section heading 15pt -> name 18pt.
BODY_SIZE = 18
ENTRY_HEADER_SIZE = 24
SECTION_HEADING_SIZE = 30
NAME_SIZE = 36

STYLE_CHILD_ORDER = [
    "name", "aliases", "basedOn", "next", "link", "autoRedefine", "hidden",
    "uiPriority", "semiHidden", "unhideWhenUsed", "qFormat", "locked",
    "personal", "personalCompose", "personalReply", "rsid",
    "pPr", "rPr", "tblPr", "trPr", "tcPr", "tblStylePr",
]

PPR_CHILD_ORDER = [
    "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr",
    "widowControl", "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs",
    "suppressAutoHyphens", "kinsoku", "wordWrap", "overflowPunct",
    "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi", "adjustRightInd",
    "snapToGrid", "spacing", "ind", "contextualSpacing", "mirrorIndents",
    "suppressOverlap", "jc", "textDirection", "textAlignment",
    "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr",
    "pPrChange",
]

RPR_CHILD_ORDER = [
    "rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps", "strike",
    "dstrike", "outline", "shadow", "emboss", "imprint", "noProof",
    "snapToGrid", "vanish", "webHidden", "color", "spacing", "w", "kern",
    "position", "sz", "szCs", "highlight", "u", "effect", "bdr", "shd",
    "fitText", "vertAlign", "rtl", "cs", "em", "lang", "eastAsianLayout",
    "specVanish", "oMath",
]


def local(tag):
    return tag.split("}")[-1]


def w(tag):
    return f"{{{W_NS}}}{tag}"


def insert_in_order(parent, new_el, order):
    new_idx = order.index(local(new_el.tag))
    insert_pos = len(list(parent))
    for i, child in enumerate(parent):
        try:
            child_idx = order.index(local(child.tag))
        except ValueError:
            continue
        if child_idx > new_idx:
            insert_pos = i
            break
    parent.insert(insert_pos, new_el)
    return new_el


def get_or_create(parent, tag, order):
    existing = parent.find(w(tag))
    if existing is not None:
        return existing
    return insert_in_order(parent, ET.Element(w(tag)), order)


def get_pPr(style_el):
    return get_or_create(style_el, "pPr", STYLE_CHILD_ORDER)


def get_rPr(style_el):
    return get_or_create(style_el, "rPr", STYLE_CHILD_ORDER)


def set_color(rpr, color):
    el = rpr.find(w("color"))
    if el is None:
        el = insert_in_order(rpr, ET.Element(w("color")), RPR_CHILD_ORDER)
    el.set(w("val"), color)


def set_bold(rpr):
    if rpr.find(w("b")) is None:
        insert_in_order(rpr, ET.Element(w("b")), RPR_CHILD_ORDER)


def set_caps(rpr):
    if rpr.find(w("caps")) is None:
        insert_in_order(rpr, ET.Element(w("caps")), RPR_CHILD_ORDER)


def set_size(rpr, half_points):
    el = rpr.find(w("sz"))
    if el is None:
        el = insert_in_order(rpr, ET.Element(w("sz")), RPR_CHILD_ORDER)
    el.set(w("val"), str(half_points))


def style_run_props(style_el, *, color=None, bold=False, caps=False, size=None):
    rpr = get_rPr(style_el)
    if color is not None:
        set_color(rpr, color)
    if bold:
        set_bold(rpr)
    if caps:
        set_caps(rpr)
    if size is not None:
        set_size(rpr, size)


def style_bottom_border(style_el):
    ppr = get_pPr(style_el)
    pbdr = insert_in_order(ppr, ET.Element(w("pBdr")), PPR_CHILD_ORDER)
    bottom = ET.SubElement(pbdr, w("bottom"))
    bottom.set(w("val"), "single")
    bottom.set(w("sz"), "6")
    bottom.set(w("space"), "4")
    bottom.set(w("color"), GRAY)


def style_space_before(style_el, twips):
    ppr = get_pPr(style_el)
    spacing = get_or_create(ppr, "spacing", PPR_CHILD_ORDER)
    spacing.set(w("before"), twips)


def find_style(root, style_id):
    for style in root.findall(w("style")):
        if style.get(w("styleId")) == style_id:
            return style
    return None


def new_paragraph_style(root, style_id, name, based_on="Normal"):
    style = ET.SubElement(root, w("style"))
    style.set(w("type"), "paragraph")
    style.set(w("styleId"), style_id)
    name_el = insert_in_order(style, ET.Element(w("name")), STYLE_CHILD_ORDER)
    name_el.set(w("val"), name)
    based_el = insert_in_order(style, ET.Element(w("basedOn")), STYLE_CHILD_ORDER)
    based_el.set(w("val"), based_on)
    return style


def main():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        base_docx = tmp / "base_reference.docx"
        with open(base_docx, "wb") as f:
            subprocess.run(
                ["pandoc", "--print-default-data-file", "reference.docx"],
                check=True,
                stdout=f,
            )

        extract_dir = tmp / "extracted"
        with zipfile.ZipFile(base_docx) as zf:
            zf.extractall(extract_dir)

        styles_path = extract_dir / "word" / "styles.xml"
        tree = ET.parse(styles_path)
        root = tree.getroot()

        normal = find_style(root, "Normal")
        if normal is not None:
            style_run_props(normal, size=BODY_SIZE)
        else:
            print("warning: 'Normal' style not found in pandoc's default reference.docx")

        title = find_style(root, "Title")
        if title is not None:
            style_run_props(title, color=BLUE, bold=True, size=NAME_SIZE)
        else:
            print("warning: 'Title' style not found in pandoc's default reference.docx")

        heading1 = find_style(root, "Heading1")
        if heading1 is not None:
            style_run_props(heading1, color=GRAY, bold=True, caps=True, size=SECTION_HEADING_SIZE)
            style_bottom_border(heading1)
        else:
            print("warning: 'Heading1' style not found in pandoc's default reference.docx")

        resume_name = new_paragraph_style(root, "ResumeName", "Resume Name")
        style_run_props(resume_name, color=BLUE, bold=True, size=NAME_SIZE)

        entry_header = new_paragraph_style(root, "EntryHeader", "Entry Header")
        style_space_before(entry_header, "120")  # 6pt gap before each new entry
        style_run_props(entry_header, bold=True, size=ENTRY_HEADER_SIZE)

        tree.write(styles_path, xml_declaration=True, encoding="UTF-8")

        OUT.parent.mkdir(parents=True, exist_ok=True)
        if OUT.exists():
            OUT.unlink()
        with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in extract_dir.rglob("*"):
                if path.is_file():
                    zf.write(path, path.relative_to(extract_dir))

    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
