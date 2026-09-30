# HIMKAVACH

**SIH26049 — DRDO · Smart India Hackathon 2026 · Team ALPHA 20 · Team ID 131984**

> A physics-guided reliability screening and decision-support system for
> electrical/electronic equipment under subzero temperature and low-pressure
> high-altitude conditions (Ladakh HAA/SHAA).

[![Live Simulator](https://img.shields.io/badge/▶_HIMKAVACH_Live_Simulator-online-brightgreen)](https://himkavach.grok.me)
![SIH 2026](https://img.shields.io/badge/SIH_2026-Hardware-blue)
![Team](https://img.shields.io/badge/Team-ALPHA_20-orange)
![PS](https://img.shields.io/badge/PS-SIH26049_DRDO-red)
![Track](https://img.shields.io/badge/track-simulation_%2B_architecture-lightgrey)
![Python](https://img.shields.io/badge/Python-3.x-yellow)

| [🚀 Live Demo](https://himkavach.grok.me) | [🏗 Architecture](docs/architecture/himkavach-architecture.png) | [📘 Blueprint V9](docs/HIMKAVACH_Hardware_Blueprint_V9.pdf) | [📚 Documentation](docs/physics/README.md) | [🧪 Validation](docs/validation/VALIDATION_PLAN.md) |
|---|---|---|---|---|

> **Evidence honesty:** every number in this repo carries exactly one tag —
> `MEASURED` · `COMPUTED` · `LITERATURE` · `ASSUMPTION` · `ESTIMATE` ·
> `PROPOSED / FUTURE VALIDATION`. *Implemented* and *simulated* appear only as
> plain status words, never as tags. **No PCB has been fabricated, no components
> purchased, no physical measurements exist** — the `MEASURED` track is empty by
> design.

## For Evaluators — the 2-minute tour

1. **See it work (60 s):** open the [HIMKAVACH Live Simulator](https://himkavach.grok.me) →
   pick the *Chang La extreme (−40 °C)* preset → watch pressure, clearance
   margin, junction temperature and battery retention recompute, then open the
   **Report** tab for the verdict and equations.
2. **Check the honesty (30 s):** every number on the site and in this repo
   carries one evidence tag — `[COMPUTED]`, `[LITERATURE]`, `[ESTIMATE]`,
   `[ASSUMPTION]`, or `PROPOSED / FUTURE VALIDATION`. Nothing measured is
   claimed; the `MEASURED` column is empty by design.
3. **Reproduce it (30 s):** one command regenerates every figure in this repo
   from code — see [Reproduce everything](#reproduce-everything).

## Prototype — simulator screenshots

![HIMKAVACH simulator — Mission page, Chang La preset (5,364 m, −14.4 °C), captured 30 Sep 2026](screenshots/simulator-mission-page.png)

*Mission page (Chang La · Jan preset): altitude/air sliders, computed pressure,
density and clearance cards — all badged `[COMPUTED]`. Captured 30 Sep 2026.*

![HIMKAVACH simulator — Report tab verdicts, captured 30 Sep 2026](screenshots/simulator-report-verdicts.png)

*Report tab: "Verdicts at the current air" — Clearance Pass (B3), Thermal Pass,
Battery charge-blocked, Life estimate. Captured 30 Sep 2026.*

**Software evidence only** — these are the web simulator, not hardware.
Try it live: https://himkavach.grok.me

## Contents

- [What is it?](#what-is-it)
- [Why does it matter?](#why-does-it-matter)
- [Why DRDO cares](#why-drdo-cares)
- [Key results at a glance](#key-results-at-a-glance)
- [Battery architecture](#battery-architecture)
- [How does it work?](#how-does-it-work)
- [What is actually implemented? What remains?](#what-is-actually-implemented-what-remains)
- [The problem](#the-problem)
- [Proposed solution](#proposed-solution)
- [Hardware blueprint V9](#hardware-blueprint-v9)
- [Simulation outputs](#simulation-outputs)
- [🚀 Live Demo — HIMKAVACH Live Simulator](#-live-demo--himkavach-live-simulator)
- [Repository map](#repository-map)
- [Reproduce everything](#reproduce-everything)
- [Tech stack](#tech-stack)
- [Limitations (read before citing this work)](#limitations-read-before-citing-this-work)
- [Why HIMKAVACH?](#why-himkavach)
- [Label legend](#label-legend)
- [Security](#security)

![HIMKAVACH architecture](docs/architecture/himkavach-architecture.png)

## What is it?

HIMKAVACH takes a Ladakh operating environment (pressure, temperature,
humidity), runs it through three literature physics models — **thermal**,
**HV/insulation breakdown**, **cold-battery behaviour** — and returns a
screening verdict (**PASS / REVIEW / REDESIGN**) plus mitigation
recommendations. Every prediction is then checked against physical
measurement; **the model loses every tie.**

## Why does it matter?

At 5,360 m (Chang La), air pressure is ≈ 51 kPa — half of sea level.
That single fact simultaneously weakens natural convection, cuts
insulation strength by ~40% (Paschen's law), and combines with −20 °C cold
to slash battery capacity. Equipment qualified for the plains fails in
Ladakh for these three coupled reasons. HIMKAVACH screens for all three
*before* hardware is committed.

## Why DRDO cares

Deep-research passes, 30 Sep 2026 — every fact below carries its source and a
verification flag; full citations in [`docs/references/REFERENCES.md`](docs/references/REFERENCES.md)
and [`docs/references/DRDO-DEEP-CONTEXT.md`](docs/references/DRDO-DEEP-CONTEXT.md).

- The Indian Army permanently stations troops in the High Altitude and
  Super High Altitude Areas of Ladakh and Siachen. Winter clothing for
  these troops is officially specified to withstand temperatures
  **below −50 °C** (PIB, Lok Sabha reply, 3 Feb 2017) `[LITERATURE]`.
- High-altitude troops are officially issued **electronic** aids —
  avalanche victim detectors and trackers — and DRDO's Defence
  Geoinformatics Research Establishment (**DGRE**, Chandigarh) operates
  **72 snow-met observatories and 45 automatic weather stations** (100 more
  under testing, 203 under installation) feeding near-real-time avalanche
  warning bulletins to them (Lok Sabha Starred Q342, 25.03.2025 — primary
  source) `[LITERATURE]`. DGRE's sensor network is itself an exposed
  high-altitude electronics system — the exact reliability problem this
  project screens for.
- Published field-failure data exists: SASE/DGRE derived **exponential
  reliability with constant hazard rate 0.071** for AWS snow-depth sensors
  from **2004–2012 field failure data** — the kind of reliability evidence
  this project's measured-data track is designed to produce `[LITERATURE]`.
- DRDO's Defence Institute of Physiology & Allied Sciences (DIPAS)
  developed the Him-Taapak space-heating device for troops in Eastern
  Ladakh and Siachen; the Army placed orders worth over ₹420 crore (ANI,
  Jan 2021, quoting the DIPAS Director — secondary source)
  `[LITERATURE]`.
- India's military environmental standard **JSS 55555** treats
  cold-plus-thin-air as a distinct qualification case: **Test No. 3
  (Altitude)** covers equipment "under simultaneously applied Service
  conditions of low air pressure and high or low temperature"; Test No. 20
  is Low Temperature (from an unofficial copy of JSS 55555:2012 Rev. 3 —
  the spec is a controlled document with no official free text)
  `[LITERATURE, secondary copy]`. MIL-STD-810H **Method 520.5 (Combined
  Environments)** is the combined altitude+temperature method `[LITERATURE,
  secondary]`.
- The single most actionable design rule: **IPC-2221B Table 6-1** demands
  **2.5 mm creepage at sea level–3,050 m vs 12.5 mm above 3,050 m** for
  301–500 V uncoated external conductors; **conformal coating collapses it
  to 0.8 mm** `[LITERATURE, secondary]`. HIMKAVACH screens exactly this.
- Precedent: **iDEX DISC-5** sought solutions for BMP-2 lead-acid battery
  derating at high altitude; **DISC-14 + ADITI 4.0 (107 challenges)**
  launched 19 Mar 2026 (verified live on idex.gov.in); **TDF** offers up to
  ₹50 cr per project at 90% grant-in-aid; **IIT Roorkee's DIA-CoE** works on
  energy storage, thermal management and snow/avalanche studies — direct
  overlap `[LITERATURE, mixed verification — see deep-context doc]`.
- Honesty note: we found **no verifiable public incident** of electronic
  equipment failing specifically because of altitude, low pressure, or
  cold. The problem statement asserts observed field effects; we treat
  them as the qualification gap to screen for, not as documented
  incidents.

## Key results at a glance

All values below are produced by the code in `simulation/` or cited from
literature — see [Label legend](#label-legend).

| Quantity | Sea level | Chang La (5,360 m) | Label |
|---|---|---|---|
| Air pressure | 101.3 kPa | **51.5 kPa** | `[COMPUTED]` |
| Breakdown voltage, 0.8 mm bare gap | 4,198 V | **2,446 V** | `[COMPUTED]` (Paschen's law) |
| Paschen minimum (air) | 305.3 V | 305.3 V | `[COMPUTED]` repo constants; ≈327 V `[LITERATURE]` textbook figure |
| Usable battery capacity at −20 °C | 100% | **≈ 80%** | `[ASSUMPTION]` — no datasheet on file |
| Twin-board prototype cost | — | ≈ ₹6,700 | `[ESTIMATE]` — verify before purchase |

## Battery architecture

Single, consistent architecture across repo and blueprint: **2S1P 18650** ·
**7.4 V nominal / 8.4 V max / 6.0 V cutoff** · 22.2 Wh rated (3000 mAh-class
cells) · 2S BMS (HX-2S class) · TP5100 charger in 2S/8.4 V mode ·
charge-lock below 0 °C.

**ASSUMPTION — CELL TO BE VERIFIED BEFORE PURCHASE.** No specific 18650 cell
has been selected; no cell datasheet is on file. Unbranded cells are excluded
from E3 by safety rule.

## How does it work?

```
Environment → Physics Models → Electronics Risk Analysis
    → Mitigation Recommendation → Physical Validation → Model Calibration
```

The calibration loop is the point: twin-board experiments (E1/E3) replace
assumed model parameters with measured ones.

## What is actually implemented? What remains?

**IMPLEMENTED** — live web simulator ([HIMKAVACH Live Simulator](https://himkavach.grok.me));
physics library + 4 CLI tools (`simulation/`); risk engine; architecture
diagram; full docs (physics, validation plan, BOM, references, roadmap).

**SIMULATED** — every number and graph in this repo (plain status word, not an
evidence tag): Paschen curves, convection penalty, battery derating,
clearance analysis.

**PROPOSED** — hardware blueprint V9
([`docs/HIMKAVACH_Hardware_Blueprint_V9.pdf`](docs/HIMKAVACH_Hardware_Blueprint_V9.pdf));
TEST-PCB-01 layout; validation rig; experiments E1/E2/E3. Twin-board
prototype ≈ ₹6,700 `[ESTIMATE]` — BOM ready, nothing purchased.

**FUTURE VALIDATION** — E1 thermal, E2 insulation (simulation-only for
students — safety), E3 cold battery; accredited chamber; Ladakh field
validation.

**MEASURED** — nothing yet. No prototype exists; no measurements are
claimed anywhere in this repository.

## The problem

Electronics in Ladakh face three coupled stresses:

- **Low pressure** (~51 kPa at Chang La) — thinner air insulates less
  (breakdown voltage falls) and convects less (components run hotter).
- **Subzero temperature** (≈ −20 °C nominal) — batteries lose usable
  capacity; materials and lubricants change behaviour.
- **Reduced convection** — the same wattage produces a larger temperature
  rise than at sea level.
- **Insulation/breakdown stress** — a 0.8 mm clearance rated 4.2 kV at sea
  level withstands only ~2.4 kV at Chang La [COMPUTED, Paschen's law].
- **Cold battery conditions** — ~80% usable capacity at −20 °C
  [ASSUMPTION — no datasheet on file].

## Proposed solution

HIMKAVACH is a **physics-guided reliability screening and
decision-support system**. It is explicitly **not** a fully validated
qualification system — it screens designs cheaply, recommends mitigations,
and earns trust through the measurement loop, not through claims.

### Three mechanisms

1. **Thermal** — lumped convection+radiation model; convection derated with
   pressure (`h ∝ (p/p0)^0.8` [ASSUMPTION] — the parameter E1 will calibrate).
2. **Electrical insulation / breakdown** — Paschen's law; clearance
   screening sea-level vs Ladakh.
3. **Cold-battery behaviour** — temperature derating of usable capacity and
   internal resistance for a 2S 18650 pack.

## Hardware blueprint V9

**[`docs/HIMKAVACH_Hardware_Blueprint_V9.pdf`](docs/HIMKAVACH_Hardware_Blueprint_V9.pdf)** —
10-page A4 landscape engineering blueprint (Rev B, 30 Sep 2026, supersedes
Rev A): master system architecture (D1), validation rig (D2), data
provenance (D3), proposed test PCB (D4), simulator-vs-repo divergence
disclosure, failure/mitigation matrix, traceability, BOM, risk register
(incl. R-09/R-10), phased roadmap. Full red-team report:
[`docs/HIMKAVACH_RedTeam_Report_V9.md`](docs/HIMKAVACH_RedTeam_Report_V9.md).

## Simulation outputs

Every figure below is simulation output — generated by `generate_figures.py`
from the physics models, stamped on the figure itself. No measurements.

![Paschen curve — simulation output](screenshots/graphs/paschen_curve.png)

*Paschen curve for air, sea level vs Chang La. The 0.8 mm operating point
drops from 4,198 V to 2,446 V — [COMPUTED].*

![Pressure and temperature vs altitude — simulation output](screenshots/graphs/pressure_temperature_vs_altitude.png)

*Standard-atmosphere pressure and temperature vs altitude, marking Chang La
(5,360 m, 51.5 kPa) — [COMPUTED].*

More figures (thermal convection penalty, battery derating, clearance
analysis) live in [`screenshots/graphs/`](screenshots/graphs/).

## 🚀 Live Demo — HIMKAVACH Live Simulator

**[▶ Open the HIMKAVACH Live Simulator](https://himkavach.grok.me)**

Audited live on 30 Sep 2026 — every item below was confirmed present on
the site. (Export/download buttons were seen but not click-tested.)

- **7 modules:** Mission · Air · Clearance · Thermal · Battery · Life · Report
- **Global inputs:** altitude (default 5,364 m) and ambient temperature
  (default −14.4 °C) sliders; computed pressure (51.44 kPa), density, and
  IEC clearance-factor stat cards, all badged `[COMPUTED]`
- **8 site/month presets:** Chang La Jan / Dec / Feb / extreme (−40 °C),
  Leh town Jan / Dec / Feb, and a sea-level lab for comparison
- **Sea-level-vs-Ladakh comparison table** (Mission page: pressure,
  clearance margin, junction temperature, battery retention)
- **Clearance:** working voltage, conductor spacing, coating and
  internal/external toggles; "Required spacing vs altitude" and Paschen
  curve charts; PASS/FAIL margin badges
- **Thermal:** "Tj vs altitude" and "Pmax vs altitude" charts, sensitivity
  table, lumped board map, and mitigation buttons (lower load, better
  package, add cooling)
- **Battery:** "Retention vs cell temperature" chart with literature
  anchors (the −40 °C point flagged estimate), heater/preheat controls,
  FAIL / charge-blocked banners
- **Life:** Arrhenius acceleration-factor chart and predicted-life estimate
- **Report:** entries list, verdicts, before/after comparison, numbered
  equations (1–8), verbatim assumptions, standards section (IPC-2221,
  IEC 60664-1, ISA/ICAO, IMD Leh normals, JSS 55555), **Save as PDF** and
  **CSV exports**
- Honest labelling throughout: `[COMPUTED]` / `[LITERATURE]` /
  `[ESTIMATE]` / `[ASSUMPTION]` badges and explicit disclaimers —
  *"not a digital twin and not a certification."*

The deployed web app's frontend source is not vendored in this repository;
this repo holds the physics, documentation, and reproducible models behind it.
The app's battery/thermal implementations differ in detail from `simulation/`
(lookup-table vs linear battery curve; Theta-JA vs lumped-surface thermal) —
both are `[COMPUTED]` screening models; do not mix the two value sets.

## Repository map

```
README.md                      ← you are here
docs/
  HIMKAVACH_Hardware_Blueprint_V9.pdf  ← hardware blueprint (Rev B)
  architecture/                ← himkavach-architecture.png + .svg
  physics/                     ← equations, assumptions, limitations
  validation/                  ← VALIDATION_PLAN.md (E1/E2/E3)
  bom/                         ← BOM.md (ESTIMATE — verify before purchase)
  references/                  ← REFERENCES.md + DRDO-DEEP-CONTEXT.md (real citations only)
simulation/
  common/physics.py            ← shared library (documented models)
  paschen/  thermal/  battery/  risk-engine/   ← CLI tools + examples
  requirements.txt
screenshots/
  simulator-mission-page.png   ← simulator screenshot (software evidence only)
  simulator-report-verdicts.png← simulator screenshot (software evidence only)
  graphs/                      ← generated outputs (simulation)
results/
  computation_log_2026-09-30.txt ← clean re-run log
assets/conceptual/             ← reference visuals + PHOTO_STATUS.md
hardware/
  roadmap/                     ← staged plan, [DONE] vs [PLANNED]
  component-list/              ← twin-board sensor map
generate_figures.py            ← regenerates every figure in this repo
```

## Reproduce everything

```bash
cd simulation && pip install -r requirements.txt
python3 common/physics.py && python3 paschen/paschen_curve.py \
  && python3 thermal/thermal_model.py && python3 battery/battery_model.py \
  && python3 risk-engine/risk_engine.py
cd .. && python3 generate_figures.py   # every figure in this repo
```

Logged output: [`results/computation_log_2026-09-30.txt`](results/computation_log_2026-09-30.txt).

## Tech stack

- **Models & simulation:** Python 3, NumPy, Matplotlib (`simulation/`,
  `generate_figures.py`)
- **Live simulator:** deployed web app at [himkavach.grok.me](https://himkavach.grok.me)
  (frontend source not vendored — this repo holds the physics behind it)
- **Docs & figures:** Markdown, SVG/PNG generated from code — no
  hand-drawn charts, no screenshots passed off as data

## Limitations (read before citing this work)

- No accredited environmental chamber — all "altitude" results are computed,
  and the only planned physical pressure test is a *partial* hand-pump
  vacuum desiccator, honestly framed.
- No field validation in Ladakh yet.
- The thermal model's convection exponent (0.8) is an assumption awaiting E1.
- The battery derating curve below −20 °C is an engineering estimate awaiting E3;
  the −20 °C 80% anchor is an assumption — no cell datasheet is on file.
- E2 (insulation) stays simulation-only: students do not build HV rigs.
- Prototype limitations: twin-board freezer tests are relative comparisons,
  not absolute altitude qualification.
- The deployed app's battery/thermal implementations differ in detail from
  `simulation/`; the app's 100 Wh pack is a placeholder `[ASSUMPTION]`, not the
  proposed 22.2 Wh hardware — do not mix the two value sets.
- No measurements exist yet — the `MEASURED` category above is empty by design.

## Why HIMKAVACH?

Detailed solvers (Ansys Sherlock, Siemens PollEx, COMSOL) and qualification
standards (JSS 55555, MIL-810H) already exist — HIMKAVACH **complements**
them, it does not replace them. The intended niche is a **low-cost,
field-oriented, altitude-specific screening + physical correlation
workflow**: cheap literature models up front, twin-board measurements that
calibrate those models, and a risk verdict a field engineer can act on —
before expensive chamber time is booked.

## Label legend

`MEASURED` physical sensor data (empty by design) · `[COMPUTED]` produced by
`simulation/` code · `[LITERATURE]` published value · `[ASSUMPTION]` team
modelling choice · `[ESTIMATE]` verify before acting · `PROPOSED / FUTURE
VALIDATION` designed but not yet built/run. *Implemented* and *simulated* are
plain status words, never tags. Full definitions in
[`docs/physics/README.md`](docs/physics/README.md).

## Security

No secrets are committed to this repository — no API keys, passwords,
tokens, `.env` files, or credentials of any kind.

---

*Team ALPHA 20 · SIH 2026 · Problem Statement SIH26049 (DRDO) · Round-2
submission track: simulation + architecture. Prototype build follows the
[roadmap](hardware/roadmap/README.md). Licensed under the [MIT License](LICENSE).*
