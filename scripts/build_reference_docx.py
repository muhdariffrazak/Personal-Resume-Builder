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

# Typographic scale (half-points = pt * 2), matching templates/resume.latex --
# including its uniform scale offset, currently 0.5pt down from the original
# 9/12/15/18. Half-points are why the offset is restricted to multiples of
# 0.5pt: anything finer cannot be expressed here, and the docx would silently
# drift from the PDF.
#   body 8.5pt -> entry title 11.5pt -> section heading 14.5pt -> name 17.5pt
BODY_SIZE = 17
ENTRY_HEADER_SIZE = 23
SECTION_HEADING_SIZE = 29
NAME_SIZE = 35

# Page geometry, in twips (1440 = 1 inch), mirroring the \usepackage{geometry}
# call in templates/resume.latex: A4, 0.85in margins, 0.7in top. Pandoc's stock
# reference.docx ships a bare <w:sectPr/> with no page size and no margins at
# all, so Word falls back to its own application defaults -- frequently US
# Letter at 1in margins. That silently costs ~0.4in of width and ~0.5in of
# height versus the PDF, which is enough to push a tuned 2-page resume to 3.
TWIPS_PER_INCH = 1440
PAGE_W = 11906  # A4 width  (210mm)
PAGE_H = 16838  # A4 height (297mm)
MARGIN_SIDE = round(0.85 * TWIPS_PER_INCH)
MARGIN_TOP = round(0.70 * TWIPS_PER_INCH)
MARGIN_BOTTOM = round(0.85 * TWIPS_PER_INCH)

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


def style_spacing(style_el, before=None, after=None):
    """
    Set explicit paragraph spacing, in twips (20 = 1pt). Pandoc's stock styles
    carry print-document spacing that is wildly looser than the LaTeX build --
    Heading1 alone reserves 24pt before, against \\titlespacing's 10pt -- so
    every style the resume actually uses gets pinned to its PDF counterpart
    here. Without this the two outputs disagree by roughly a third of a page.
    """
    ppr = get_pPr(style_el)
    spacing = get_or_create(ppr, "spacing", PPR_CHILD_ORDER)
    if before is not None:
        spacing.set(w("before"), str(before))
    if after is not None:
        spacing.set(w("after"), str(after))


def style_keep_with_next(style_el):
    """
    Word's "Keep with next": the paragraph cannot be the last thing on a page.
    On EntryHeader this binds a header to the first bullet beneath it; on
    Heading1 it binds a section heading to the first entry beneath it. This is
    the docx-side counterpart of the \\needspace{} that
    templates/format-select.lua emits for the PDF build -- the two outputs
    paginate independently, so both need saying.
    """
    get_or_create(get_pPr(style_el), "keepNext", PPR_CHILD_ORDER)


def style_keep_lines(style_el):
    """
    Word's "Keep lines together": the paragraph's own lines never straddle a
    page break. Entry headers are a single paragraph of 2-3 hard-broken lines
    (institution / role / dates), so without this Word may split the name away
    from the dates.
    """
    get_or_create(get_pPr(style_el), "keepLines", PPR_CHILD_ORDER)


def set_page_geometry(doc_root):
    """
    Give the document's section an explicit A4 page size and margins matching
    templates/resume.latex. Without this the docx inherits Word's own defaults
    and paginates differently from the PDF built from the same Markdown.
    """
    body = doc_root.find(w("body"))
    sect = body.find(w("sectPr"))
    if sect is None:
        sect = ET.SubElement(body, w("sectPr"))

    for tag in ("pgSz", "pgMar"):
        existing = sect.find(w(tag))
        if existing is not None:
            sect.remove(existing)

    pg_sz = ET.SubElement(sect, w("pgSz"))
    pg_sz.set(w("w"), str(PAGE_W))
    pg_sz.set(w("h"), str(PAGE_H))

    pg_mar = ET.SubElement(sect, w("pgMar"))
    pg_mar.set(w("top"), str(MARGIN_TOP))
    pg_mar.set(w("bottom"), str(MARGIN_BOTTOM))
    pg_mar.set(w("left"), str(MARGIN_SIDE))
    pg_mar.set(w("right"), str(MARGIN_SIDE))
    # \pagestyle{empty} in the LaTeX build -- no running head or foot to reserve.
    pg_mar.set(w("header"), "0")
    pg_mar.set(w("footer"), "0")
    pg_mar.set(w("gutter"), "0")


def clear_default_paragraph_spacing(styles_root):
    """
    Pandoc's stock reference.docx puts <w:spacing w:after="200"/> in
    docDefaults, i.e. 10pt of dead space after EVERY paragraph -- every bullet
    and every header line. The LaTeX build uses \\parskip 0 with 1pt between
    list items, so this one default is the single largest source of drift
    between the two outputs. Zero it and let the EntryHeader style's explicit
    6pt "before" provide the only deliberate gap, matching the PDF's
    \\AfterEndEnvironment{itemize}{\\vspace{6pt}}.
    """
    defaults = styles_root.find(w("docDefaults"))
    if defaults is None:
        return
    ppr_default = defaults.find(w("pPrDefault"))
    if ppr_default is None:
        return
    ppr = ppr_default.find(w("pPr"))
    if ppr is None:
        return
    spacing = ppr.find(w("spacing"))
    if spacing is None:
        spacing = insert_in_order(ppr, ET.Element(w("spacing")), PPR_CHILD_ORDER)
    spacing.set(w("after"), "0")
    spacing.set(w("before"), "0")
    spacing.set(w("line"), "240")  # single spacing
    spacing.set(w("lineRule"), "auto")


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

        document_path = extract_dir / "word" / "document.xml"
        doc_tree = ET.parse(document_path)
        set_page_geometry(doc_tree.getroot())
        doc_tree.write(document_path, xml_declaration=True, encoding="UTF-8")

        styles_path = extract_dir / "word" / "styles.xml"
        tree = ET.parse(styles_path)
        root = tree.getroot()

        clear_default_paragraph_spacing(root)

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
            style_keep_with_next(heading1)
        else:
            print("warning: 'Heading1' style not found in pandoc's default reference.docx")

        resume_name = new_paragraph_style(root, "ResumeName", "Resume Name")
        style_run_props(resume_name, color=BLUE, bold=True, size=NAME_SIZE)

        # Pin the spacing of every style the resume actually uses to its LaTeX
        # counterpart (twips: 20 = 1pt). Pandoc's defaults are tuned for prose
        # documents and are far looser than templates/resume.latex.
        #   Heading1 -> \titlespacing{\section}{0pt}{10pt}{6pt}
        #   BodyText -> \parindent 0, \parskip 0 (skills lines, the summary)
        #   Compact  -> \setlist itemsep=1pt (every bullet)
        for style_id, before, after in (
            ("Heading1", 200, 120),
            ("BodyText", 0, 0),
            ("Compact", 0, 20),
        ):
            style = find_style(root, style_id)
            if style is not None:
                style_spacing(style, before=before, after=after)
            else:
                print(f"warning: '{style_id}' style not found in pandoc's default reference.docx")

        entry_header = new_paragraph_style(root, "EntryHeader", "Entry Header")
        style_spacing(entry_header, before=120)  # 6pt gap before each new entry
        style_keep_with_next(entry_header)
        style_keep_lines(entry_header)
        # NOT bold at style level. The header is one paragraph of 2-3 hard-broken
        # lines and only the first (company/title) is bold -- RULES.md §1 -- which
        # the template already expresses by wrapping just that line in **...**.
        # Bolding the style bolded the role and date lines too, so the docx came
        # out heavier than the PDF built from the same Markdown.
        style_run_props(entry_header, size=ENTRY_HEADER_SIZE)

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
