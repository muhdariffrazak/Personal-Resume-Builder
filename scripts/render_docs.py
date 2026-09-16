#!/usr/bin/env python3
"""
Regenerate docs/*.md — human-readable, cross-referenced views of data/*.yaml.
These are generated output, not hand-edited; edit the YAML and re-run this.

Usage: python3 scripts/render_docs.py
"""
import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"

HEADER = "<!-- Generated from data/*.yaml by scripts/render_docs.py — edit the YAML, not this file. -->\n"


def load_yaml(name):
    with open(DATA / f"{name}.yaml") as f:
        return yaml.safe_load(f)


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def resolve_bullet_text(bullet, experience_by_id):
    if "ref" in bullet:
        exp_id, bullet_id = bullet["ref"].split(":")
        job = experience_by_id[exp_id]
        for b in job["bullets"]:
            if b["id"] == bullet_id:
                return b["text"]
        raise KeyError(f"bullet ref not found: {bullet['ref']}")
    return bullet["text"]


def render_experience(experience, projects_by_source):
    lines = [HEADER, "# Experience\n"]
    for job in experience:
        lines.append(f"## {job['role']}, {job['company']}")
        loc = f" | {job['location']}" if job.get("location") else ""
        lines.append(f"*{job['dates']}{loc}*")
        lines.append("")
        for b in job["bullets"]:
            tags = ", ".join(b["tags"])
            lines.append(f"- **[{b['id']}]** {b['text']} _(tags: {tags})_")
        related = projects_by_source.get(job["id"], [])
        if related:
            lines.append("")
            links = ", ".join(f"[{p['title']}](projects.md#{slugify(p['title'])})" for p in related)
            lines.append(f"**Related projects:** {links}")
        lines.append("")
    return "\n".join(lines)


def render_projects(projects, experience_by_id):
    lines = [HEADER, "# Projects\n"]
    for proj in projects:
        lines.append(f"## {proj['title']}")
        meta = []
        if proj.get("role"):
            meta.append(proj["role"])
        if proj.get("sponsor"):
            meta.append(proj["sponsor"])
        if proj.get("dates"):
            meta.append(proj["dates"])
        if meta:
            lines.append(f"*{' | '.join(meta)}*")
        if proj.get("status"):
            lines.append(f"**Status:** {proj['status']}")
        if proj.get("todo"):
            lines.append(f"> **TODO:** {proj['todo'].strip()}")
        lines.append("")
        for b in proj["bullets"]:
            lines.append(f"- {resolve_bullet_text(b, experience_by_id)}")
        source = proj.get("source")
        if source:
            job = experience_by_id[source["experience_id"]]
            lines.append("")
            lines.append(
                f"**Source:** pulled from [{job['role']}, {job['company']}]"
                f"(experience.md#{slugify(job['role'] + ', ' + job['company'])})"
            )
        lines.append("")
    return "\n".join(lines)


def render_education(education):
    lines = [HEADER, "# Education\n"]
    for edu in education:
        lines.append(f"## {edu['institution']}")
        lines.append(f"*{edu['degree']} | {edu['dates']}*")
        lines.append("")
        for h in edu["highlights"]:
            lines.append(f"- {h}")
        lines.append("")
    return "\n".join(lines)


def render_skills(skills):
    lines = [HEADER, "# Skills\n"]
    for domain in skills:
        lines.append(f"## {domain['domain']} _(tag: {domain['tag']})_")
        for item in domain["entries"]:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines)


def main():
    experience = load_yaml("experience")
    projects = load_yaml("projects")
    education = load_yaml("education")
    skills = load_yaml("skills")

    experience_by_id = {j["id"]: j for j in experience}

    projects_by_source = defaultdict(list)
    for p in projects:
        if p.get("source"):
            projects_by_source[p["source"]["experience_id"]].append(p)

    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "experience.md").write_text(render_experience(experience, projects_by_source))
    (DOCS / "projects.md").write_text(render_projects(projects, experience_by_id))
    (DOCS / "education.md").write_text(render_education(education))
    (DOCS / "skills.md").write_text(render_skills(skills))
    print("Regenerated docs/experience.md, docs/projects.md, docs/education.md, docs/skills.md")


if __name__ == "__main__":
    main()
