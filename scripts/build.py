#!/usr/bin/env python3
"""
Build a resume variant: data/*.yaml + data/variants.yaml -> rendered Markdown
-> pandoc -> dist/resume-<variant>.pdf and dist/resume-<variant>.docx.

Usage: python3 scripts/build.py --variant full
"""
import argparse
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"
BUILD = ROOT / "build"
DIST = ROOT / "dist"


def load_yaml(name):
    with open(DATA / f"{name}.yaml") as f:
        return yaml.safe_load(f)


def resolve_bullet_text(bullet, experience_by_id):
    if "ref" in bullet:
        exp_id, bullet_id = bullet["ref"].split(":")
        job = experience_by_id[exp_id]
        for b in job["bullets"]:
            if b["id"] == bullet_id:
                return b["text"]
        raise KeyError(f"bullet ref not found: {bullet['ref']}")
    return bullet["text"]


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


def build_experience(cfg, experience):
    ids, bullets_override = resolve_ids(cfg, experience, bullets_key="bullets")
    if ids is None:
        return None
    by_id = {j["id"]: j for j in experience}
    result = []
    for jid in ids:
        job = by_id[jid]
        bsel = bullets_override.get(jid, "all")
        if bsel == "all":
            bullets = [b["text"] for b in job["bullets"]]
        else:
            bmap = {b["id"]: b["text"] for b in job["bullets"]}
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


def build_projects(cfg, projects, experience_by_id):
    ids, _ = resolve_ids(cfg, projects)
    if ids is None:
        return None
    by_id = {p["id"]: p for p in projects}
    result = []
    for pid in ids:
        proj = by_id[pid]
        bullets = [resolve_bullet_text(b, experience_by_id) for b in proj["bullets"]]
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


def build_education(cfg, education):
    ids, _ = resolve_ids(cfg, education)
    if ids is None:
        return None
    by_id = {e["id"]: e for e in education}
    return [by_id[eid] for eid in ids]


def build_skills(cfg, skills):
    if cfg is None or cfg == "none":
        return None
    if cfg == "all":
        return skills
    if isinstance(cfg, dict):
        tags = set(cfg.get("include", []))
        return [d for d in skills if d["tag"] in tags]
    raise ValueError(f"Unrecognised skills selector: {cfg!r}")


def build_awards(cfg, awards):
    ids, _ = resolve_ids(cfg, awards)
    if ids is None:
        return None
    by_id = {a["id"]: a for a in awards}
    return [by_id[aid] for aid in ids]


def build_volunteering(cfg, volunteering):
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
                "bullets": [b["text"] for b in v["bullets"]],
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
    variants = load_yaml("variants")

    variant = next((v for v in variants if v["id"] == args.variant), None)
    if variant is None:
        available = ", ".join(v["id"] for v in variants)
        sys.exit(f"Unknown variant '{args.variant}'. Available: {available}")

    experience_by_id = {j["id"]: j for j in experience}

    ctx = {
        "personal": personal,
        "sections": variant["sections"],
        "experience": build_experience(variant.get("experience"), experience),
        "projects": build_projects(variant.get("projects"), projects, experience_by_id),
        "education": build_education(variant.get("education"), education),
        "skills": build_skills(variant.get("skills"), skills),
        "awards": build_awards(variant.get("awards"), awards),
        "volunteering": build_volunteering(variant.get("volunteering"), volunteering),
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

    DIST.mkdir(parents=True, exist_ok=True)
    pdf_path = DIST / f"resume-{args.variant}.pdf"
    docx_path = DIST / f"resume-{args.variant}.docx"

    lua_filter = str(TEMPLATES / "format-select.lua")
    latex_template = str(TEMPLATES / "resume.latex")
    reference_docx = TEMPLATES / "reference.docx"

    common = ["pandoc", str(md_path), "--from", "markdown+raw_attribute", "--lua-filter", lua_filter]

    subprocess.run(
        common + ["--template", latex_template, "--pdf-engine", "pdflatex", "-o", str(pdf_path)],
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
        print(f"Built {docx_path}")
    else:
        print(f"Skipped docx build: {reference_docx} not found (run scripts/build_reference_docx.py first)")


if __name__ == "__main__":
    main()
