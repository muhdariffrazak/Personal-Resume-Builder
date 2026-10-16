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
make build VARIANT=mha-drone                 # -> dist/Muhammad_Ariff_Resume.pdf/docx (filename override, see below)
make build-all                               # builds every variant in data/variants.yaml
```

`VARIANT` defaults to `full` if omitted. The first run builds the Docker
image (a few minutes); after that it's cached.

### Variants

Defined in `data/variants.yaml`:

- `full` — everything, the master reference
- `mha-drone` — the tailored submission for the MHA Embodied AI lead:
  reverse-chronological experience including National Service, then Projects.
  Builds to the fixed filename `dist/Muhammad_Ariff_Resume.{pdf,docx}` (via
  `filename:` in `variants.yaml`) instead of `dist/resume-mha-drone.*`, since
  this is the copy that actually gets sent out
- `ai-ml-focused` — leads with AI/ML work
- `robotics-embedded-focused` — leads with robotics/embedded work

All variants use the same section order (experience → education → projects →
skills → awards → volunteering, where present); variants differ in which
entries/bullets are included, not the order.

Add a new variant by adding an entry to `variants.yaml` — no code changes
needed. Each section accepts `all`, `none`, or `{include: [ids or tags]}`;
`experience` additionally accepts a `bullets: {job_id: [bullet_ids]}` override
to show only specific bullets for a job. An optional `filename:` key overrides
the `dist/` output basename (default: `resume-<variant-id>`).

## The editable `.docx`

`dist/resume-<variant>.docx` (or the variant's `filename:` override, e.g.
`Muhammad_Ariff_Resume.docx` for `mha-drone`) is generated from the same data as the PDF, styled via
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

## Design: ATS-safe over template-exact

The layout is single-column on purpose: name on its own line, contact info as
plain text below it, "Title, Company — Date" on one plain line, skills as
comma-separated lines, awards as a plain bullet list. No side-by-side columns
and no tables anywhere in the document. This was a deliberate tradeoff — the
original coach-provided template (`archive/1 - Resume Building Tool_V8.pdf`)
used two-column layouts (name/contact side by side, date right-aligned via a
table), which can get extracted in the wrong order or mangled by some ATS
(Applicant Tracking System) parsers. ATS-compatibility was prioritized over
matching that template's exact visual layout. Section headings (gray, bold,
ruled) and the typographic scale (9pt body / 12pt entry titles / 15pt section
headings / 18pt name) still echo the original template's hierarchy.

The PDF substitutes free metric-compatible fonts (Caladea/Carlito) for Word's
Cambria/Calibri; the `.docx` references the real font names, so it renders
with actual Cambria/Calibri when opened in Microsoft Word.

## Page limit

`mha-drone`, `ai-ml-focused`, and `robotics-embedded-focused` are
meant to fit 2 pages (all currently do; `mha-drone` is tuned to fill both). `full` is the
comprehensive master reference and is not expected to fit 2 pages.

## C.A.R (Context-Action-Result) bullets and the numbers policy

Experience, Projects, and Volunteering bullets follow a Context-Action-Result
structure. **Only figures traceable to a verified source appear in `data/`** —
the `1,200`-video dataset, `33` sources, `3 dB` at hover, `90.03` AUROC, the
`~0.3` operating threshold, `10,000` ear savers, `1,000+` teaching hours, `5`
MODI projects. Earlier drafts carried invented placeholder metrics (`___`) and
two unverified "+50%" claims; those were removed rather than guessed at, on the
principle that a reader who knows the domain will probe any number on the page.

If you later confirm a real figure, add it to the relevant bullet in `data/` and
rebuild — don't hand-edit the `.docx`, or the next build will drop it.

## Open items

Things that need a real answer from Ariff, not from the data:

- **Date conflict.** National Service (`spf-procom`, Jan 2021 – Nov 2022) overlaps
  the SOLUSTAR internship (May – Aug 2022), the start of SUTD (Aug 2022), and
  Ngee Ann Polytechnic (Sep 2022). At least the SOLUSTAR overlap looks wrong for
  a full-time NS posting. Verify and correct the dates before sending.
- **MOE certification title.** `data/awards.yaml` uses the generic "MOE (Ministry
  of Education) Instructor Certification". Replace with the exact title printed
  on the certificate.
- **C.A.R. results.** See `CAR-gaps.md` — ~15 bullets still end on an action or a
  purpose rather than an outcome, each with a recommended Result and the figure
  left blank.
- **New volunteering entry** requested but not yet supplied.

## Capstone source of truth

The `capstone-quiet-quadcopter` entry is written strictly from the MET4004
project proposal (submitted 10 Jul 2026). Corrections that proposal forced:

- **The sponsor is KLASS, not MHA.** MHA appears nowhere in the 26-page proposal.
  KLASS provides $6,000 SGD of funding and owns all resulting IP.
- The noise-reduction mechanisms are injection-molded toroidal propellers, custom
  ducts with acoustic lining and **serrated trailing edges** (on the duct, not
  owl-wing blades), 1300 KV low-RPM motors, and AM32 ESC PWM frequency tuning.
- A PRISMA-ScR review of 33 sources, a six-state factorial bench test, the 3 dB
  duct/battery mass finding, and an early-2027 conference abstract all appeared in
  earlier drafts but are **not** in the proposal. They were cut.
- The GPS-denied UAV navigation work was the capstone's original scope, descoped
  for time. It is not a separate project and was removed.

**The proposal PDF is gitignored** (`*projectproposal*`) — it is sponsor-owned IP
and contains teammates' and supervisors' personal contact details. Do not commit it
to this public repository.
