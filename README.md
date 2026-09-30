# HIMKAVACH

**SIH26049 — DRDO**

> A physics-guided reliability screening and decision-support system for
> electrical/electronic equipment under subzero temperature and low-pressure
> high-altitude conditions (Ladakh HAA/SHAA).

[![Live Simulator](https://img.shields.io/badge/▶_HIMKAVACH_Live_Simulator-online-brightgreen)](https://himkavach.grok.me)
[![Status](https://img.shields.io/badge/status-simulation_%2B_screening-blue)]()
[![Docs](https://img.shields.io/badge/docs-physics_%2F_validation_%2F_BOM-informational)]()

| [🚀 Live Demo](https://himkavach.grok.me) | [🏗 Architecture](docs/architecture/himkavach-architecture.png) | [📚 Documentation](docs/physics/README.md) | [🧪 Validation](docs/validation/VALIDATION_PLAN.md) |
|---|---|---|---|

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

**SIMULATED** — every number and graph in this repo (all marked
`SIMULATION`): Paschen curves, convection penalty, battery derating,
clearance analysis.

**CONCEPTUAL** — reference photos in `assets/conceptual/` (explicitly not
evidence of a built prototype); hand-pump vacuum desiccator as *partial*
low-pressure simulation.

**TO BE BUILT** — twin-board ESP32 prototype (≈ ₹6,700 [ESTIMATE], BOM
ready, nothing purchased).

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
  [LITERATURE, per-datasheet, chemistry-specific].

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
  `[ESTIMATE]` / `[SIMULATION]` badges and explicit disclaimers —
  *"not a digital twin and not a certification."*

The deployed web app's frontend source is not vendored in this repository;
this repo holds the physics, documentation, and reproducible models behind it.

## Repository map

```
README.md                      ← you are here
docs/
  architecture/                ← himkavach-architecture.png + .svg
  physics/                     ← equations, assumptions, limitations
  validation/                  ← VALIDATION_PLAN.md (E1/E2/E3)
  bom/                         ← BOM.md (ESTIMATE — verify before purchase)
  references/                  ← real citations only
simulation/
  common/physics.py            ← shared library (documented models)
  paschen/  thermal/  battery/  risk-engine/   ← CLI tools + examples
  requirements.txt
screenshots/graphs/            ← generated outputs, all marked SIMULATION
assets/conceptual/             ← reference visuals + PHOTO_STATUS.md
hardware/
  roadmap/                     ← staged plan, [DONE] vs [PLANNED]
  component-list/              ← twin-board sensor map
generate_figures.py            ← regenerates every figure in this repo
```

## Limitations (read before citing this work)

- No accredited environmental chamber — all "altitude" results are computed,
  and the only planned physical pressure test is a *partial* hand-pump
  vacuum desiccator, honestly framed.
- No field validation in Ladakh yet.
- The thermal model's convection exponent (0.8) is an assumption awaiting E1.
- The battery derating curve below −20 °C is an engineering estimate awaiting E3.
- E2 (insulation) stays simulation-only: students do not build HV rigs.
- Prototype limitations: twin-board freezer tests are relative comparisons,
  not absolute altitude qualification.
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

`[LITERATURE]` published value · `[COMPUTED]` produced by `simulation/`
code · `[ESTIMATE]` verify before acting · `[ASSUMPTION]` team modelling
choice. Full definitions in [`docs/physics/README.md`](docs/physics/README.md).

## Reproduce everything

```bash
cd simulation && pip install -r requirements.txt
python3 common/physics.py && python3 paschen/paschen_curve.py \
  && python3 thermal/thermal_model.py && python3 battery/battery_model.py \
  && python3 risk-engine/risk_engine.py
cd .. && python3 generate_figures.py   # every figure in this repo
```

## Security

No secrets are committed to this repository — no API keys, passwords,
tokens, `.env` files, or credentials of any kind.

---

*Team ALPHA 20 · SIH 2026 · Problem Statement SIH26049 (DRDO) · Round-2
submission track: simulation + architecture. Prototype build follows the
[roadmap](hardware/roadmap/README.md).*
