# Resume

Structured, tailorable resume system. Content lives in `data/*.yaml`; a
Docker-based build produces a styled PDF and an editable `.docx` for whichever
variant you need.

## Layout

```
data/            canonical source of truth (hand-edited YAML)
docs/            generated, human-readable Markdown views of data/ — regenerated, not hand-edited
templates/       Jinja2 -> Markdown template, LaTeX template, and the docx reference-doc
scripts/         build.py, render_docs.py, build_reference_docx.py
archive/         the original flat files this repo replaced, kept for history
dist/            final PDF + docx per variant (committed)
build/           intermediate .md/.tex per variant (gitignored)
```

## Editing content

Edit the relevant file in `data/`:

- `personal.yaml` — contact info
- `education.yaml`, `experience.yaml`, `projects.yaml`, `skills.yaml`, `awards.yaml`, `volunteering.yaml`
- `variants.yaml` — which resume variants exist and what each one includes

Each bullet in `experience.yaml` has its own `id` and `tags`. A project in
`projects.yaml` extracted from a job either writes its own `text`, or points
at an experience bullet with `ref: "<experience_id>:<bullet_id>"` so the
wording isn't duplicated. After editing, regenerate the browsable docs:

```
make docs
```

## Building a resume

Requires [Docker](https://docs.docker.com/get-docker/). Nothing else needs to
be installed — pandoc, LaTeX, and the fonts all live in the build image.

```
make build VARIANT=full                      # -> dist/resume-full.pdf, dist/resume-full.docx
make build VARIANT=mha-drone-example
make build-all                               # builds every variant in data/variants.yaml
```

`VARIANT` defaults to `full` if omitted. The first run builds the Docker
image (a few minutes); after that it's cached.

### Variants

Defined in `data/variants.yaml`:

- `full` — everything, the master reference
- `mha-drone-example` — recreates the tailored resume built manually in `Checklist.md`
- `ai-ml-focused` — leads with AI/ML work
- `robotics-embedded-focused` — leads with robotics/embedded work

Add a new variant by adding an entry to `variants.yaml` — no code changes
needed. Each section accepts `all`, `none`, or `{include: [ids or tags]}`;
`experience` additionally accepts a `bullets: {job_id: [bullet_ids]}` override
to show only specific bullets for a job.

## The editable `.docx`

`dist/resume-<variant>.docx` is generated from the same data as the PDF, styled via
`templates/reference.docx`. It's meant to be hand-edited directly for last-mile
polish before sending a resume out. Re-running `make build` will regenerate
and overwrite it — that's expected; make small edits to the YAML instead if
you want them to stick, or just don't rebuild that variant afterward.

`templates/reference.docx` itself is generated once by
`scripts/build_reference_docx.py` (it starts from pandoc's own default
reference doc and edits the style XML — no Word/LibreOffice needed). Re-run it
only if you want to change the docx's fonts/colors/styles:

```
make reference-docx
```

## Fidelity to the original template

The layout (blue name/contact header, gray section headings with a rule,
bold-title/right-aligned-date entries, numbered projects) is modeled on the
coach-provided template in `archive/1 - Resume Building Tool_V8.pdf`. The PDF
substitutes free metric-compatible fonts (Caladea/Carlito) for Word's
Cambria/Calibri; the `.docx` references the real font names, so it renders
with actual Cambria/Calibri when opened in Microsoft Word.

## Open items

- `data/projects.yaml`'s `capstone-quiet-quadcopter` entry has draft bullets
  with unfilled placeholders (`[team size]`, `[result: ...]`) transcribed from
  `Checklist.md`, plus an unresolved question about whether it's the same
  build as the `aeroacoustic-stealth` project. Resolve both before using that
  variant for a real submission.
