# HIMKAVACH validation plan

**Status: PLAN — no validation has been performed yet. No prototype has been
built. This document describes what *will* be measured, in what order, and
what a student team can and cannot validate.**

Core doctrine: **model loses every tie.** Measurement overrules the model;
the calibration loop (`Model Calibration` in the architecture) exists to
update model parameters from measured data.

Target standard for the eventual qualification framing: **JSS 55555:2012**
(Indian military environmental test standard). Sherlock/PollEx/COMSOL and
JSS 55555 / MIL-810H chambers are **complements** to this workflow, never
replacements — HIMKAVACH is a pre-qualification screening + physical
correlation workflow, not a qualification rig.

## E1 — Thermal (twin-board experiment)

| Step | Detail |
|---|---|
| **Input** | Two identical boards: one at room conditions, one in a freezer / cold box. Known dissipation (resistive load), DS18B20 thermal array, BMP280 pressure, INA219 logging, microSD. |
| **Test** | Run both boards at fixed power; log board temperature vs time to steady state. Repeat at 2–3 power levels. |
| **Measurement** | Steady-state ΔT above ambient per board; convection coefficient inferred per condition. |
| **Model comparison** | Compare measured ΔT against `thermal_rise()` predictions. The exponent in `h(p) = h0·(p/p0)^0.8` is the parameter to calibrate — it is currently the weakest assumption in the repo. |
| **Can validate** | Relative convection penalty between conditions; thermal margin workflow end-to-end. |
| **Cannot validate** | True altitude convection (a freezer is not a low-pressure chamber); per-component θJA. |

## E2 — Electrical / insulation (simulation-only for students)

| Step | Detail |
|---|---|
| **Input** | Clearance values from a real PCB layout; applied voltages. |
| **Test** | **No physical HV test.** Paschen-based clearance screening only (`paschen_curve.py`, `clearance_analysis.png`). |
| **Measurement** | None by the student team — high-voltage arcing rigs are a safety boundary. |
| **Model comparison** | Cross-check computed Vbd against IPC-2221B clearance tables and IEC 60664-1 altitude correction factors (secondary references). |
| **Can validate** | That the screening flags the same clearances a standards table would flag. |
| **Cannot validate** | Actual breakdown voltage — no HV rig, no accredited lab. This lane stays honest about that. |

## E3 — Cold battery (freezer discharge)

| Step | Detail |
|---|---|
| **Input** | 2S 18650 pack with BMS + TP4056 charger, INA219 logging, freezer at ≈ −18 °C (typical) vs room temperature. |
| **Test** | Constant-current discharge at 2–3 rates; log voltage, current, temperature, delivered Wh. |
| **Measurement** | Usable Wh at cold vs room; voltage sag under load; cutoff behaviour. |
| **Model comparison** | Replace the estimated derating curve in `battery_model.py` with the measured curve for the chosen cell; publish the CSV. |
| **Can validate** | Relative capacity loss; whether the −20 °C / 80% datasheet anchor holds for the chosen cells. |
| **Cannot validate** | −40 °C or high-altitude-combined behaviour without a chamber; ageing effects (needs months). |

## What a student prototype can and cannot do (honest boundary)

**Can:** twin-board thermal correlation in a freezer; cold battery discharge
curves; end-to-end screening workflow (environment → physics → risk →
mitigation → decision); CSV-logged, reproducible measurements.

**Cannot:** true low-pressure testing (a hand-pump vacuum desiccator is a
partial simulation, never an altitude chamber); HV breakdown testing
(safety); accredited environmental qualification (needs a real chamber and
JSS 55555:2012 procedure); field validation in Ladakh (future work).

Every future measurement gets committed under `measurements/` with raw CSV,
conditions, and the calibration delta applied to the models.
