#!/usr/bin/env python3
"""
Build a resume variant: data/*.yaml + data/variants.yaml -> rendered Markdown
-> pandoc -> dist/resume-<variant>.pdf and dist/resume-<variant>.docx.

Usage: python3 scripts/build.py --variant full
"""
import argparse
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"
BUILD = ROOT / "build"
DIST = ROOT / "dist"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W_NS)


def dedupe_docx_styles(docx_path):
    """
    Pandoc's docx writer adds its own stub definition for a custom-style it
    encounters, even when a full definition for that same styleId already
    exists in --reference-doc, leaving duplicate <w:style> elements with
    undefined precedence in Word. Keep only the first (our styled) one.
    """
    with zipfile.ZipFile(docx_path) as zf:
        entries = {name: zf.read(name) for name in zf.namelist()}

    styles_xml = entries["word/styles.xml"]
    tree = ET.ElementTree(ET.fromstring(styles_xml))
    root = tree.getroot()

    seen = set()
    for style in list(root.findall(f"{{{W_NS}}}style")):
        style_id = style.get(f"{{{W_NS}}}styleId")
        if style_id in seen:
            root.remove(style)
        else:
            seen.add(style_id)

    entries["word/styles.xml"] = ET.tostring(root, xml_declaration=True, encoding="UTF-8")

    with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries.items():
            zf.writestr(name, data)


def apply_docx_margin(docx_path, margin_in):
    """
    Mirror a variant's `margin_in:` override in the docx: rewrite the section's
    page margins, and move the EntryHeader right tab stop (the right-aligned
    dates) out to the new text width. Plain string substitution, not an XML
    round-trip, so Word's namespace prefixes (mc:Ignorable etc.) survive intact.
    """
    import re

    twips = round(margin_in * 1440)
    with zipfile.ZipFile(docx_path) as zf:
        entries = {name: zf.read(name) for name in zf.namelist()}

    doc = entries["word/document.xml"].decode("utf-8")
    page_w = re.search(r'<w:pgSz\b[^>]*\bw:w="(\d+)"', doc)
    if page_w is None:
        raise RuntimeError("docx has no <w:pgSz w:w=...>; was templates/reference.docx regenerated?")
    old_mar = re.search(r'<w:pgMar\b[^>]*\bw:left="(\d+)"', doc)
    old_text_width = int(page_w.group(1)) - 2 * int(old_mar.group(1))
    new_text_width = int(page_w.group(1)) - 2 * twips

    def set_margins(m):
        tag = m.group(0)
        for side in ("top", "bottom", "left", "right"):
            tag = re.sub(rf'\bw:{side}="\d+"', f'w:{side}="{twips}"', tag)
        return tag

    doc, n = re.subn(r"<w:pgMar\b[^>]*/>", set_margins, doc)
    if n != 1:
        raise RuntimeError(f"expected one <w:pgMar>, found {n}")
    entries["word/document.xml"] = doc.encode("utf-8")

    styles = entries["word/styles.xml"].decode("utf-8")
    styles, n = re.subn(
        rf'(<w:tab\b[^>]*\bw:pos=")({old_text_width})(")',
        rf"\g<1>{new_text_width}\g<3>",
        styles,
    )
    if n == 0:
        raise RuntimeError(f"no right tab stop at the old text width ({old_text_width} twips)")
    entries["word/styles.xml"] = styles.encode("utf-8")

    with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries.items():
            zf.writestr(name, data)


def match_docx_list_indent(docx_path, indent_twips=240):
    """
    Pandoc writes its own word/numbering.xml (it is not taken from the reference
    doc) with top-level bullets indented 720 twips (0.5in). The PDF indents
    bullets by 1.2em (~12pt = 240 twips), so docx bullet text runs ~24pt
    narrower and wraps more often -- enough to push a one-page variant onto a
    second page. Set level-0 bullets to the PDF's indent. Applied to condensed
    variants only, so the existing 2-page docx files are unchanged.
    """
    import re

    with zipfile.ZipFile(docx_path) as zf:
        entries = {name: zf.read(name) for name in zf.namelist()}
    if "word/numbering.xml" not in entries:
        return
    numbering = entries["word/numbering.xml"].decode("utf-8")

    def fix_level0(m):
        return re.sub(
            r'<w:ind w:left="\d+" w:hanging="\d+"\s*/>',
            f'<w:ind w:left="{indent_twips}" w:hanging="{indent_twips}" />',
            m.group(0),
        )

    numbering = re.sub(r'<w:lvl w:ilvl="0">.*?</w:lvl>', fix_level0, numbering, flags=re.S)
    entries["word/numbering.xml"] = numbering.encode("utf-8")

    with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in entries.items():
            zf.writestr(name, data)


def load_yaml(name):
    with open(DATA / f"{name}.yaml") as f:
        return yaml.safe_load(f)


def pick_text(item, condensed):
    """
    A bullet's wording. Condensed variants (`condensed: true` in variants.yaml,
    used for one-page resumes) take the bullet's optional `short:` wording and
    fall back to `text:` when it has none. `short:` restates the same fact more
    tightly -- it is not a separate fact, so it lives beside `text:` on the same id.
    """
    if condensed and item.get("short"):
        return item["short"]
    return item["text"]


def resolve_bullet_text(bullet, experience_by_id, condensed=False):
    if "ref" in bullet:
        exp_id, bullet_id = bullet["ref"].split(":")
        job = experience_by_id[exp_id]
        for b in job["bullets"]:
            if b["id"] == bullet_id:
                return pick_text(b, condensed)
        raise KeyError(f"bullet ref not found: {bullet['ref']}")
    return pick_text(bullet, condensed)


def resolve_ids(cfg, all_items, bullets_key=None):
    """Shared logic for 'all' / 'none' / {'include': [...]} selectors."""
    if cfg is None or cfg == "none":
        return None, {}
    by_id = {item["id"]: item for item in all_items}
    if cfg == "all":
        return list(by_id.keys()), {}
    if isinstance(cfg, dict):
        ids = cfg.get("include", list(by_id.keys()))
        bullets_override = cfg.get(bullets_key, {}) if bullets_key else {}
        return ids, bullets_override
    raise ValueError(f"Unrecognised selector: {cfg!r}")


def build_experience(cfg, experience, condensed=False):
    ids, bullets_override = resolve_ids(cfg, experience, bullets_key="bullets")
    if ids is None:
        return None
    by_id = {j["id"]: j for j in experience}
    result = []
    for jid in ids:
        job = by_id[jid]
        bsel = bullets_override.get(jid, "all")
        if bsel == "all":
            bullets = [pick_text(b, condensed) for b in job["bullets"]]
        else:
            bmap = {b["id"]: pick_text(b, condensed) for b in job["bullets"]}
            bullets = [bmap[bid] for bid in bsel]
        result.append(
            {
                "company": job["company"],
                "role": job["role"],
                "location": job.get("location"),
                "dates": job["dates"],
                "bullets": bullets,
            }
        )
    return result


def build_projects(cfg, projects, experience_by_id, condensed=False):
    ids, bullets_override = resolve_ids(cfg, projects, bullets_key="bullets")
    if ids is None:
        return None
    by_id = {p["id"]: p for p in projects}
    result = []
    for pid in ids:
        proj = by_id[pid]
        selected = proj["bullets"]
        bsel = bullets_override.get(pid, "all")
        if bsel != "all":
            bmap = {b["id"]: b for b in proj["bullets"] if "id" in b}
            missing = [bid for bid in bsel if bid not in bmap]
            if missing:
                raise KeyError(f"project {pid}: unknown bullet id(s) {missing}")
            selected = [bmap[bid] for bid in bsel]
        bullets = [resolve_bullet_text(b, experience_by_id, condensed) for b in selected]
        result.append(
            {
                "title": proj["title"],
                "role": proj.get("role"),
                "sponsor": proj.get("sponsor"),
                "dates": proj.get("dates"),
                "bullets": bullets,
            }
        )
    return result


def build_education(cfg, education, condensed=False):
    ids, _ = resolve_ids(cfg, education)
    if ids is None:
        return None
    by_id = {e["id"]: e for e in education}
    result = []
    for eid in ids:
        edu = dict(by_id[eid])
        if condensed and "short_highlights" in edu:
            edu["highlights"] = edu["short_highlights"]
        result.append(edu)
    return result


def build_skills(cfg, skills, condensed=False):
    if cfg is None or cfg == "none":
        return None
    if cfg == "all":
        selected = skills
    elif isinstance(cfg, dict):
        tags = set(cfg.get("include", []))
        selected = [d for d in skills if d["tag"] in tags]
    else:
        raise ValueError(f"Unrecognised skills selector: {cfg!r}")
    if not condensed:
        return selected
    return [
        {
            **d,
            "domain": d.get("short_domain", d["domain"]),
            "entries": d.get("short_entries") or d["entries"],
        }
        for d in selected
    ]


def build_awards(cfg, awards, condensed=False):
    ids, _ = resolve_ids(cfg, awards)
    if ids is None:
        return None
    by_id = {a["id"]: a for a in awards}
    result = []
    for aid in ids:
        award = by_id[aid]
        if condensed and award.get("short"):
            # One-line wording that replaces the name/date (or the whole entries list).
            award = {"name": award["short"]}
        result.append(award)
    return result


def build_summary(cfg, summaries):
    """
    `summary:` in a variant is a single id (or absent/"none"), not a selector --
    a resume has at most one opening paragraph, so there is nothing to include
    a list of.
    """
    if cfg is None or cfg == "none":
        return None
    by_id = {s["id"]: s for s in summaries}
    if cfg not in by_id:
        available = ", ".join(by_id) or "(none defined)"
        raise KeyError(f"Unknown summary id {cfg!r}. Available: {available}")
    return by_id[cfg]["text"]


def build_volunteering(cfg, volunteering, condensed=False):
    ids, _ = resolve_ids(cfg, volunteering)
    if ids is None:
        return None
    by_id = {v["id"]: v for v in volunteering}
    result = []
    for vid in ids:
        v = by_id[vid]
        result.append(
            {
                "name": v["name"],
                "dates": v.get("dates"),
                "bullets": [pick_text(b, condensed) for b in v["bullets"]],
            }
        )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", default="full", help="Variant id from data/variants.yaml")
    args = parser.parse_args()

    personal = load_yaml("personal")
    experience = load_yaml("experience")
    projects = load_yaml("projects")
    education = load_yaml("education")
    skills = load_yaml("skills")
    awards = load_yaml("awards")
    volunteering = load_yaml("volunteering")
    summaries = load_yaml("summary")
    variants = load_yaml("variants")

    variant = next((v for v in variants if v["id"] == args.variant), None)
    if variant is None:
        available = ", ".join(v["id"] for v in variants)
        sys.exit(f"Unknown variant '{args.variant}'. Available: {available}")

    experience_by_id = {j["id"]: j for j in experience}
    condensed = bool(variant.get("condensed", False))

    awards_built = build_awards(variant.get("awards"), awards, condensed)
    # `certifications_in_skills: true` renders the selected awards as one labelled
    # "Certifications:" line at the end of the Skills section instead of as their
    # own section -- saves a section heading on the one-page variants.
    certifications_line = None
    if variant.get("certifications_in_skills") and awards_built:
        certifications_line = "; ".join(a["name"] for a in awards_built)

    ctx = {
        "personal": personal,
        "certifications_line": certifications_line,
        "summary": build_summary(variant.get("summary"), summaries),
        "sections": variant["sections"],
        # Optional per-variant section-heading overrides, e.g. {awards: "CERTIFICATIONS"}.
        "headings": variant.get("headings", {}),
        "experience": build_experience(variant.get("experience"), experience, condensed),
        "projects": build_projects(variant.get("projects"), projects, experience_by_id, condensed),
        "education": build_education(variant.get("education"), education, condensed),
        "skills": build_skills(variant.get("skills"), skills, condensed),
        "awards": awards_built,
        "volunteering": build_volunteering(variant.get("volunteering"), volunteering, condensed),
    }

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    rendered = env.get_template("resume.md.j2").render(**ctx)

    variant_build_dir = BUILD / args.variant
    variant_build_dir.mkdir(parents=True, exist_ok=True)
    md_path = variant_build_dir / "resume.md"
    md_path.write_text(rendered)

    basename = variant.get("filename", f"resume-{args.variant}")
    DIST.mkdir(parents=True, exist_ok=True)
    pdf_path = DIST / f"{basename}.pdf"
    docx_path = DIST / f"{basename}.docx"

    lua_filter = str(TEMPLATES / "format-select.lua")
    latex_template = str(TEMPLATES / "resume.latex")
    reference_docx = TEMPLATES / "reference.docx"

    common = ["pandoc", str(md_path), "--from", "markdown+raw_attribute", "--lua-filter", lua_filter]

    # Optional page-margin override (inches), used by the one-page variants only.
    margin_in = variant.get("margin_in")
    latex_vars = ["-V", f"margin={margin_in}in"] if margin_in else []

    subprocess.run(
        common + latex_vars + ["--template", latex_template, "--pdf-engine", "pdflatex", "-o", str(pdf_path)],
        check=True,
        cwd=variant_build_dir,
    )
    print(f"Built {pdf_path}")

    if reference_docx.exists():
        subprocess.run(
            common + ["--reference-doc", str(reference_docx), "-o", str(docx_path)],
            check=True,
            cwd=variant_build_dir,
        )
        dedupe_docx_styles(docx_path)
        if margin_in:
            apply_docx_margin(docx_path, float(margin_in))
        if condensed:
            match_docx_list_indent(docx_path)
        print(f"Built {docx_path}")
    else:
        print(f"Skipped docx build: {reference_docx} not found (run scripts/build_reference_docx.py first)")


if __name__ == "__main__":
    main()
