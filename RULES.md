# Resume Rules

The standing rules every variant must follow. `README.md` explains how the build system
works; this file governs what "correct" looks like once it's built. When a new bullet, a new
variant, or a template change conflicts with something here, this file wins — update it
deliberately (and say why) rather than drift past it silently.

---

## 1. Structure & Formatting

### Section order
Every variant renders sections in this order, skipping any it doesn't include:

```
Work Experience → Education → Projects → Skills / Competencies → Awards → Volunteering
```

Variants differ in **which entries and bullets** appear per section (via `data/variants.yaml`
selectors), never in section order. If a variant ever needs a different order, that's a
deliberate exception — call it out in the variant's `description` field.

### Summary
An optional opening paragraph, rendered directly under the contact line with **no section
heading** and no entry in `sections:` — it is part of the header block, not a section. A
variant opts in with `summary: <id>` in `data/variants.yaml`, pointing at an entry in
`data/summary.yaml`; a variant with no `summary:` key renders none, which is the default.

- Same content rules as any bullet: no first person (§2), no buzzword padding (§2), and every
  claim traceable to a real bullet elsewhere on that variant (§3). Write it in resume voice.
- It must not cite something the variant doesn't show. The `mha-public-safety` summary
  deliberately omits the teaching history for this reason — `mha-drone` cuts the Nullspace
  entry, so a summary citing it would point at nothing.
- One summary per variant. Tailor by writing a new id rather than by hedging one text to
  cover several audiences.

### Entry headers
Each entry's header is a single styled paragraph, split onto its own lines with a markdown
hard break (never crammed onto one line, never a bare blank line between them):

- **Experience** — 3 lines: **Company** (+ ` | Location` if present) / Role / Dates
- **Projects** — 3 lines: **N. Title** / Role (+ ` (Sponsor)` if present) / Dates
- **Education** — 2 lines: **Institution** / Dates. Degree is the entry's first bullet, not
  a header line.
- **Volunteering** — 2 lines: **Name** / Dates. No role field.

Only the first line (name/title) is bold. A line is omitted entirely if its underlying field
is empty (e.g. an entry with no dates skips the date line) — never render an empty line.

### Bullets
- One fact per bullet, one line of markdown per bullet (it may wrap visually; it is not
  multiple `-` items).
- No sub-bullets, no bolding or nested formatting inside a bullet.
- A project bullet is either its own `text:` or a `ref: "job_id:bullet_id"` reuse of an
  experience bullet — never a re-typed paraphrase of one (see §3, single source of truth).

### Page length
- `full` is the master reference and is **not** expected to fit any page limit.
- Every tailored variant (currently `mha-drone`, `ai-ml-focused`, `robotics-embedded-focused`)
  targets **exactly 2 pages**. Check with `pdfinfo dist/<file>.pdf | grep Pages` after every
  rebuild. A variant that used to fit and no longer does is fixed by a content trim **or** by
  shifting the whole typographic scale down — never by tightening margins, and never by
  shrinking one level in isolation.
- **Scale offset.** The four sizes in `templates/resume.latex` may be lowered together by a
  uniform offset (a multiple of 0.5pt, since the docx expresses sizes in half-points), keeping
  the 3pt step between levels and the font + 2pt leading intact. This rule previously forbade
  a font change outright; it was relaxed deliberately when the MHA summary was added, because
  a 0.5pt offset held 2 pages while every content trim on the table cost a real signal —
  ROSCon, SOLUSTAR, or the HPC bullet. Three files hardcode the scale and must move together:
  `templates/resume.latex`, the size constants in `scripts/build_reference_docx.py`, and the
  `*_LINE_PT` leading constants in `templates/format-select.lua` (get that last one wrong and
  the page-break reservations below silently stop matching reality). After any offset change,
  run `make reference-docx`, then `make build-all`, then re-check page counts and breaks.
  Current offset: **0.5pt** (body 8.5 / entry 11.5 / section 14.5 / name 17.5). Do not go
  below body 8pt — that is the floor for comfortable print legibility.
- When trimming, cut in this order: excess volunteering entries → SOLUSTAR bullets → teaching
  (Nullspace/VM Education) bullets → the newest/least-load-bearing bullet in an otherwise-long
  job. Never trim by deleting a Result clause and leaving the bullet ending on Action — cut the
  whole bullet instead.

### Page breaks
An entry header must never be stranded at the foot of a page without at least its first
bullet. Section headings likewise never end a page alone. This is enforced structurally, not
by hand-tuning content, and it is enforced **twice** because the PDF and the docx paginate
independently:

- **PDF** — `templates/format-select.lua` emits a `\needspace{}` ahead of every `EntryHeader`
  Div, sized from that header's own line count (2-line Education/Volunteering headers reserve
  less than 3-line Experience/Projects ones). A **section heading reserves for itself plus
  whatever follows it** — the next entry header's full requirement when one follows, two body
  lines when the section is a bare list (Awards, Skills). That look-ahead is load-bearing, not
  belt-and-braces: an entry header's own `\needspace` creates a legal breakpoint immediately
  above itself, so without it a section heading gets stranded at the page foot by the very
  mechanism meant to prevent stranding. `templates/resume.latex` sets
  `\widowpenalty`/`\clubpenalty` to 10000 so no paragraph leaves a single line either side of
  a break.
- **docx** — `scripts/build_reference_docx.py` sets `keepNext` on `EntryHeader` and `Heading1`
  (bind a header to what follows it) and `keepLines` on `EntryHeader` (the 2-3 hard-broken
  header lines never straddle a break). After changing that script, regenerate with
  `make reference-docx` — `templates/reference.docx` is a build artifact, and a variant
  rebuild alone will not pick up style changes.

Bullets *may* continue onto the next page once the header and first bullet are together; a
whole entry is deliberately not held together, because forcing that on a 5-bullet entry
(KLASS, the capstone) costs more page budget than a 2-page variant has. The one case this
does not structurally prevent is a trailing single list item landing alone after a break —
a section's last award or bullet. Check for it by eye when a section's item count changes.

### docx / PDF parity
Both outputs are built from the same Markdown, so **they must paginate identically** — same
page count, same content at each page break. They do not get there on their own: pandoc's
stock `reference.docx` is tuned for prose documents and disagreed with the LaTeX build by
roughly a third of a page. Everything that governs layout is therefore pinned explicitly in
`scripts/build_reference_docx.py`, mirroring `templates/resume.latex`:

| What | LaTeX | docx |
|---|---|---|
| Page size + margins | `geometry` A4, 0.85in, top 0.7in | explicit `pgSz` + `pgMar` in `sectPr` |
| Paragraph spacing | `\parskip` 0 | `docDefaults` spacing `after=0` |
| Section heading | `\titlespacing` 10pt / 6pt | `Heading1` before 200 / after 120 twips |
| Skills + summary text | `\parskip` 0 | `BodyText` before 0 / after 0 |
| Bullets | `\setlist itemsep=1pt` | `Compact` before 0 / after 20 twips |
| Entry gap | `\AfterEndEnvironment{itemize}{\vspace{6pt}}` | `EntryHeader` before 120 twips |

Pandoc's bare `<w:sectPr/>` carries **no page size at all**, so without the explicit `pgSz`
Word falls back to its own default — frequently US Letter — and silently loses ~0.5in of
height against A4. That alone can cost a page.

Note the `EntryHeader` style is deliberately **not** bold: only the first header line is bold
(§1 "Entry headers"), and the template already marks it with `**...**`. Bolding the style
bolds the role and date lines too.

### ATS-safety
- Single-column layout only. No tables, no side-by-side columns, no text boxes.
- No graphics, icons, or images.
- Section headings are plain text (styled via custom Div, not raw markdown headers with
  decoration).

### Output filenames
- Default: `dist/resume-<variant-id>.{pdf,docx}`.
- A variant may set `filename:` in `data/variants.yaml` to override this — used for
  `mha-drone`, which builds to `dist/Muhammad_Ariff_Resume.{pdf,docx}` because that's the
  literal file that gets sent out. Only give a variant a fixed filename if it is an actual
  send-out copy, not a general-purpose tailored variant.

---

## 2. Tone & Voice

- **No first person.** Bullets and headers never contain "I", "my", or "we" — the resume
  format implies first person; stating it is redundant filler.
- **Active voice, strong verbs.** "Designed and built," "Led," "Engineered," "Reproduced" —
  not "Was responsible for" or "Helped with."
- **Tense by role status.** A finished role/project uses past tense throughout its bullets. An
  ongoing role (`dates` ending "Present," e.g. Nullspace) uses present tense. Don't mix tenses
  within a single entry.
- **C.A.R. discipline (Context → Action → Result).** Every bullet should land on an outcome,
  not trail off on the action or its purpose. "Built X for Y" is Context + Action with no
  Result; "Built X for Y, achieving Z" or "...adopted by N teams" closes the loop. See
  `CAR-gaps.md` for the live audit of which bullets still fall short and why.
- **Precision over impressiveness.** Name the actual tool/framework/standard (RAFT, SAM 2,
  ISO 532-1, STM32F7) rather than a vaguer category term. A reader who knows the domain should
  recognize real technical choices, not marketing language.
- **No unverifiable claims.** If a Result can't be backed by a real number or a concrete,
  checkable outcome, don't invent one — see the numbers policy in §3. A bullet that ends on
  Action because its Result was cut is preferable to a plausible-sounding fabrication.
- **No buzzword padding.** Words like "passionate," "synergy," "results-driven," "dynamic" as
  a standalone descriptor are not used. Let the bullets demonstrate the trait instead of
  naming it.

---

## 3. Content & Data Policy

### Single source of truth
Every fact about a job lives exactly once, in `data/experience.yaml`, with a stable `id`. A
project bullet that describes work also covered by a job bullet uses `ref: "job_id:bullet_id"`
to reuse that exact wording — it never re-describes the same fact in different words. If the
wording needs to change, it changes once, at the source (`data/experience.yaml`), and every
`ref:` picks it up automatically on rebuild.

### Numbers policy
Only figures traceable to a real, verifiable source appear in any bullet — a measured result,
a document (e.g. the MET4004 proposal), or something the person can state confidently in an
interview. Never:
- Invent a placeholder metric (`___`, `[X]%`) and leave it as if it were real.
- Round or embellish a real figure to sound more impressive.
- Carry forward an old unverified number (e.g. a legacy "+50%") without re-confirming it.

If a bullet's natural Result would need a number nobody can verify, either find the true
number, replace it with a qualitative-but-honest outcome (e.g. "used company-wide," "validated
in on-robot trials"), or cut the result clause and leave the bullet on Action. Do not soften
an unverifiable claim into vague language that sounds like a number without being one.

### Data model
- `data/*.yaml` are the only hand-edited sources for resume content. `docs/*.md` and every
  `dist/*.{pdf,docx}` are generated — never hand-edit generated output; edit the YAML and
  rebuild. (The one sanctioned exception: last-mile hand edits to a `.docx` right before
  sending, per `README.md` §"The editable .docx" — understand that the next rebuild will
  overwrite them.)
- Every bullet, job, project, award, and volunteering entry has a stable `id`. Don't reuse an
  `id` for a different fact, and don't rename an `id` without checking `data/variants.yaml`
  and any `ref:` pointers still reference it.
- `tags:` on jobs/bullets/skills exist so variants can select by theme (e.g. `ai-ml`,
  `robotics-embedded`) — keep them accurate to the bullet's actual content, since a tailored
  variant's relevance depends on them.

### Variant selection
- A variant's `experience`/`projects`/`education`/`awards`/`volunteering` keys each take
  `all`, `none`, or `{include: [ids]}`; `experience` additionally accepts
  `bullets: {job_id: [bullet_ids]}` to narrow which bullets of an included job show up.
- Prefer narrowing bullets over excluding a whole job/entry when only part of it is relevant
  to the variant's audience.

---

## Before sending any resume

1. Rebuild (`make build VARIANT=<id>` or `make build-all`) — never send a `dist/` file that
   predates the latest `data/*.yaml` edit.
2. `pdfinfo dist/<file>.pdf | grep Pages` — confirm the variant's page target still holds.
   Then check each page boundary against §1 "Page breaks" — no header stranded at a page
   foot, no lone trailing list item:

   ```sh
   n=$(pdfinfo dist/<file>.pdf | awk '/^Pages/{print $2}')
   for p in $(seq 1 $((n-1))); do
     echo "--- end of p$p ---";   pdftotext -f $p -l $p dist/<file>.pdf - | grep -v '^\s*$' | tail -3
     echo "--- start of p$((p+1)) ---"; pdftotext -f $((p+1)) -l $((p+1)) dist/<file>.pdf - | grep -v '^\s*$' | head -3
   done
   ```
3. Check the **docx** paginates the same as the PDF (§1 "docx / PDF parity") — it is the file
   that actually gets sent, and it is laid out by Word, not by LaTeX. There is no Writer on
   this machine, so render it in a throwaway container:

   ```sh
   docker run --rm -v "$PWD":/work -w /work --user root resume-builder bash -c '
     apt-get update -qq >/dev/null 2>&1
     DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
       libreoffice-writer-nogui >/dev/null 2>&1
     soffice --headless -env:UserInstallation=file:///tmp/lo --convert-to pdf \
       --outdir /work/build/docxcheck dist/<file>.docx >/dev/null 2>&1
     chmod -R a+rw /work/build/docxcheck'
   pdfinfo build/docxcheck/<file>.pdf | grep Pages
   ```

   LibreOffice is a close approximation of Word, not Word itself — treat a mismatch as real
   and a match as strong evidence, not proof.
4. Skim every bullet against §2 (C.A.R., tense, no first person) and §3 (no invented numbers).
5. If `data/variants.yaml` or `templates/resume.md.j2` changed, re-check `CAR-gaps.md`'s
   "Note on length" section is still accurate — update it if a trim/reorder changed the story.
6. Confirm section order matches §1 exactly, and every entry header follows its format (3-line
   Experience/Projects, 2-line Education/Volunteering).
