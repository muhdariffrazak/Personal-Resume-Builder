# C.A.R. gaps — recommended Results to fill

Audit of every bullet in `data/experience.yaml`, `data/projects.yaml`, and
`data/volunteering.yaml` against Context → Action → **Result** (the pattern your coach's
template models: "achieved zero incidents", "100% signup rate", "completed on schedule").
Originally scoped to just the `mha-drone` resume (since replaced by `home-team`); a later full-repo pass extended it to every
bullet regardless of which variant shows it.

**Nothing here is invented.** Every Result below is either a real figure/outcome you supplied,
or a bullet intentionally cut back to Action because nothing verifiable backed a Result. See
`RULES.md` §3 (numbers policy) for why an invented placeholder is never an option.

---

## Already complete — no action

| Bullet | Result it lands on |
|---|---|
| `capstone` duct/battery mass | roughly 3 dB at hover, redirecting design effort |
| `capstone` test campaign | satisfies FYP + produces publishable data for early-2027 abstract |
| `klass-benchmarking` | 90.03 AUROC on the NSG-VD replication |
| `klass-av-sync` | ~0.3 operating threshold selected via ROC |
| `klass-hpc` | sanity-check protocol caught pipeline errors before 5-hour training/generation runs |
| `sutd-lighting-system` | platform passed T1 autonomous testing at CETRAN |
| `sutd-safety-lstm` | showed fall risk could be predicted from the LSTM model |
| `spf-protective-security` | across 22 months of full-time service |
| `spf-armoury` | zero discrepancies |
| `solustar-pcb` | boards brought to a working prototype |
| `solustar-troubleshooting` | got the VAL2 robot running again |
| `vm-curriculum-design` | 5 published projects, became the standard MODI curriculum, plus instructor training folded in |
| `nullspace-enrichment` | 1,000+ teaching hours |
| `nullspace-curriculum` | positive feedback from students and schools |
| `roscon-2025` | ~1,000 participants from 52 countries, 3 workshops |
| `trolley-robot` (perception bullet) | completed the final demo task |
| `trolley-robot` (firmware bullet) | reliable motor control via the custom serial link |
| `custom-3d-printer` | improved first-layer adhesion/print quality, reduced failed prints |
| `sit-hardware-design` (merged with the old `sit-system-architecture`) | completed chamber handed over to the research team |
| `sit-temperature-control` | holds ±2 °C of a 37 °C setpoint |

---

## RESOLVED from the capstone proposal

The capstone section was rewritten entirely from the MET4004 proposal and now carries
real targets and results: the 78 dBA / 1 m ceiling, 10-minute endurance, 370 mm envelope,
and benchmarking against HKUST's 90.52 dBA reference. (A derated 3.3:1 thrust-to-weight
figure was later removed from the avionics bullet as too specific, and the psychoacoustics
bullet was removed.) The sponsor was corrected from MHA to KLASS. The PRISMA-ScR review,
six-state factorial test, 3 dB mass finding and conference abstract were cut — none appear
in the proposal.

A later pass added that MHA is the drone's **end user** (KLASS remains the funding sponsor),
that the project proposal has been approved, and that the drone's purpose is to **reduce
acoustic detectability** — all now stated in the `capstone` bullets.

---

## Still open — no verifiable Result available yet

- **3 of the 4 `capstone-quiet-quadcopter` bullets** (propulsion stack, avionics/power
  architecture, acoustic validation plan) end on design decisions or plans, not a measured
  outcome; since 2026-10-31 their tense says which ("Selected", "Specified", "the tests
  will"). Confirmed as expected: the project is still in
  progress (Aug 2026 – Apr 2027) and these stages haven't produced test data yet. Revisit once
  bench/flight test results exist.
- **Exact MOE certification title** — `data/awards.yaml` still uses the generic title ("MOE
  (Ministry of Education) Instructor Certification"); confirm against the certificate if you
  want the precise title (tracked in `To-Do.md` item 1).

---

## Cut / merged / no longer applicable

- **`sutd-perception`** — replaced by `sutd-perception-support`, which was itself later
  removed entirely: the 3D LiDAR wiring/integration work was not Ariff's.
- **`capstone` team leadership** bullet ("…coordinating deliverables with MHA and academic
  supervisors") — removed; no equivalent bullet in the current set.
- **`sit-validation-protocols`** — cut entirely rather than given a project count.
- **`sit-system-architecture`** — merged into `sit-hardware-design` rather than kept as a
  separate bullet; the merged bullet's Result is "handing the completed chamber over to the
  research team."
- **`vm-instructor-training`** — merged into `vm-curriculum-design` rather than kept separate;
  the merged bullet's Result is the curriculum becoming VM Education/Playfacto's standard.
- **`nullspace-cert`** — removed as a job bullet (was purely restating the achievement already
  in the Awards section); `data/awards.yaml`'s `moe-instructor-cert` entry now sources from
  the `nullspace` job generally rather than a specific now-deleted bullet.
- **`uav-gps-denied-navigation`** — already removed from `data/projects.yaml` (see README
  "Capstone source of truth": descoped from the capstone, not a separate project).

---

## Note on length

`home-team` (built as `dist/resume-home-team.{pdf,docx}`) replaced the earlier drone-tailored `mha-drone` variant on 2026-10-31, and
`defence-rnd` was split off from it the same day for DSO/DSTA. Unlike
`mha-drone`, it includes the Nullspace entry and the infra/cloud skills block. The three role
variants (`perception-embodied-ai`, `applied-ml-cv`, `embedded-firmware`) also target 2 pages.
`embedded-firmware` dropped `sg-makers-covid` to fit.

On 2026-10-31, adding the new certificates and Nullspace pushed four variants to 3 pages.
The intro-level online courses were split into their own `online-courses` award (only
`perception-embodied-ai` and `full` still show them), and these cuts restored 2 pages:
`home-team` dropped the SIT and SOLUSTAR entries, `defence-rnd` dropped SOLUSTAR, and
`embedded-firmware` dropped `klass-fullstack`. Next trim candidates if anything grows:
the ROSCon volunteering entry, then `klass-fullstack` on `home-team`.

Later on 2026-10-31 the layout moved to 10pt Calibri with right-aligned dates (RULES.md §1),
skills were condensed, intros cut to 3-4 lines and diploma coursework hidden. All five tailored
variants then fit 2 pages with Education whole on page 1; `defence-rnd` also dropped
`klass-av-sync` to get there.

`mha-drone`'s history, for context: three earlier rounds of growth each pushed it to 3 pages,
compensated by cutting `solustar-firmware`, then `sg-makers-covid`, then the whole Nullspace
entry. Trim order for any variant that overflows is in RULES.md §1 "Page length".

`full` is not expected to fit 2 pages and is currently 4.
