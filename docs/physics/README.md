# HIMKAVACH physics models

**Status: SIMULATION.** Every equation below is a literature model implemented
in `simulation/common/physics.py`. None of them has been validated against
measurements from built hardware — no prototype exists yet. Numbers produced
by these models are **[COMPUTED]**, never measured.

## Label legend (used across this repo, the simulator, and the deck)

| Label | Meaning |
|---|---|
| `[LITERATURE]` | Published value / standard / paper |
| `[COMPUTED]` | Produced by running the code in `simulation/` |
| `[ESTIMATE]` | Team estimate, verify before acting on it |
| `[ASSUMPTION]` | Modelling choice made by the team, not a standard |

## 0. Environment: pressure and temperature vs altitude

- **Purpose:** convert a Ladakh site altitude into the (pressure, temperature)
  the other models need.
- **Equation:** U.S. Standard Atmosphere 1976, troposphere branch (h < 11 km):
  `p = p0 · (T/T0)^(g·M/(R·L))`, `T = T0 − L·h`, with
  p0 = 101.325 kPa, T0 = 288.15 K, L = 0.0065 K/m.
- **Reference values [LITERATURE]:** Chang La 5,360 m → ≈ 51 kPa, ≈ −20 °C;
  Leh ≈ 3,500 m → ≈ 66 kPa.
- **Assumptions:** dry air, standard lapse rate. Real weather deviates.
- **Limitations:** monthly/seasonal extremes are not modelled; the simulator
  site/month presets (if enabled) should be treated as nominal conditions.

## 1. Electrical insulation / breakdown — Paschen's law

- **Purpose:** estimate how much dielectric strength an air clearance loses
  at low pressure, i.e. why a gap that is safe at sea level can arc in Ladakh.
- **Equation:** `Vb = B·p·d / (ln(A·p·d) − ln(ln(1 + 1/γ)))`
  with air constants A = 15 cm⁻¹·Torr⁻¹, B = 365 V/(cm·Torr), γ = 0.01.
- **Computed results [COMPUTED]:**
  - Paschen minimum with these constants: **≈ 305 V** at p·d ≈ 0.84 Torr·cm.
    The widely quoted 327 V literature value comes from alternate constant
    sets; the robust point is the floor near ~300 V, below which no air gap
    can break down.
  - Vbd for a 0.8 mm bare gap: **4,198 V** (sea level) → **2,446 V**
    (Chang La) — a ~42% loss of insulation strength.
- **Assumptions:** uniform field, parallel plates, clean dry air, γ = 0.01.
- **Limitations:** real PCB geometry (sharp trace edges, solder mask,
  contamination, humidity) derates further. This is a **screening bound**,
  not a qualification value. High-voltage arcing stays simulation-only —
  students must not build HV test rigs (safety).
- **Source:** Paschen's law; IEC 60664-1 and IEC 60071-2 for how standards
  handle altitude correction (factors reproduced from secondary engineering
  references — the primary standards are paywalled; verify before quoting).

## 2. Thermal — lumped steady-state board model

- **Purpose:** show that reduced air density at altitude weakens natural
  convection, raising component temperatures for the same dissipation.
- **Equation:** `P = h(p)·A·ΔT + ε·σ·A·((Ta+ΔT)⁴ − Ta⁴)`,
  solved for ΔT by Newton iteration.
- **Assumptions [ASSUMPTION]:** lumped isothermal surface; convection
  coefficient derated as `h(p) = h0·(p/p0)^0.8` — an empirical
  natural-convection scaling, **not measured** for this geometry;
  still air; no conduction path modelled; h0 = 8 W/m²K, ε = 0.9 defaults.
- **Limitations:** screening only. Real boards need per-component analysis
  (θJA, airflow, heatsinks). The exponent 0.8 is the single weakest
  assumption in this repo — E1 (twin-board experiment) exists to replace
  it with measured data.

## 3. Cold battery — Li-ion usable capacity vs temperature

- **Purpose:** estimate cold-weather energy loss for a 2S 18650 pack (7.4 V).
- **Model:** 100% usable at T ≥ 0 °C; linear decline to **80% at −20 °C**
  — anchored to a per-datasheet point **[LITERATURE, chemistry-specific,
  not universal]**; steeper linear decline below −20 °C **[ASSUMPTION]**.
  Internal resistance: `R(T) = R25·exp(0.045·(25−T))` **[ASSUMPTION]**.
- **Limitations:** real derating is chemistry-, rate- and age-dependent.
  This curve is an engineering estimate below −20 °C, not a measured
  discharge curve. A measured curve per chosen cell is an E3 deliverable.

## 4. Risk engine — composite screening verdict

- **Purpose:** one screening verdict from the three mechanism margins:
  **PASS / REVIEW / REDESIGN**.
- **Method:** each margin is normalised to a 0–1 sub-score with a soft knee
  (thermal: 20 °C margin → ~0.5; insulation: 2× Vbd → ~0.5; battery: 1.5×
  energy → ~0.5); weighted sum (0.35 / 0.35 / 0.30). Verdict: ≥ 0.75 PASS,
  ≥ 0.50 REVIEW, else REDESIGN.
- **Assumptions [ASSUMPTION]:** thresholds and weights are team-chosen,
  not a standard. Starting point for discussion, not a verdict.
- **Limitations:** a screening aid only — never a qualification verdict.
  The workflow rule is: **model loses every tie** — measurement overrules
  the model, and the calibration loop exists to encode that.

## Reproducing every number

```bash
cd simulation
pip install -r requirements.txt
python3 common/physics.py            # smoke test: Chang La p/T, Paschen min
python3 paschen/paschen_curve.py     # Vbd table, sea level vs Ladakh
python3 thermal/thermal_model.py     # ΔT table
python3 battery/battery_model.py     # capacity table
python3 risk-engine/risk_engine.py   # composite verdict
python3 ../generate_figures.py       # regenerate every figure in this repo
```
