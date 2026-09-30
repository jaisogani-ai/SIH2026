# HIMKAVACH hardware roadmap

Planned work is marked **[PLANNED]**; completed work **[DONE]**.
Nothing below is presented as finished until it is.

## Round 2 — simulation + architecture [DONE]

- Physics engine: thermal, HV/insulation (Paschen), battery models —
  implemented in `simulation/`, reproducible.
- Risk engine: PASS / REVIEW / REDESIGN screening — implemented.
- Live simulator deployed (link in root README).
- Architecture, physics docs, validation plan, BOM — this repository.
- SIH 6-slide deck (Round-2 submission).

## Prototype — twin boards [PLANNED]

- Build two identical ESP32 nodes per `docs/bom/BOM.md` (≈ ₹6,700 [ESTIMATE]).
- E1: twin-board thermal experiment (room vs freezer) — calibrate the
  convection exponent in the thermal model.
- E3: freezer discharge of the 2S 18650 pack — replace the estimated
  battery derating curve with a measured one; publish the CSV.
- E2 stays simulation-only (no student HV rig — safety boundary).

## Controlled cold / pressure testing [PLANNED]

- Glass desiccator + hand vacuum pump for *partial* low-pressure checks —
  honestly framed as partial simulation, never an altitude chamber.
- Repeat E1/E3 matrices; freeze model parameters v2.

## Environmental qualification [PLANNED — out of student scope]

- Accredited chamber time; JSS 55555:2012-aligned procedure.
- Requires funding / lab partnership. Listed for honesty, not promised.

## Future field validation [PLANNED — long term]

- Correlate predictions against real high-altitude deployment data
  (Ladakh field partners). No timeline committed.

## The rule at every stage

**Model loses every tie.** Each stage's measurements calibrate the models;
no stage's results are presented as qualification.
