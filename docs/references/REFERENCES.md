# HIMKAVACH references

Real sources only. Nothing here is fabricated. Standards marked
(paywalled) could not be primary-verified; their factors are used via
secondary engineering references and flagged as such wherever they appear.

## Atmospheric / altitude

- U.S. Standard Atmosphere 1976 (NOAA/NASA/USAF) — barometric formula used
  in `standard_atmosphere()`. Public-domain model.
- Chang La altitude 5,360 m and the ≈ 51 kPa / ≈ −20 °C nominal conditions
  used as the reference site [LITERATURE — standard geographic/meteorological
  references; treat as nominal, not a measured deployment log].

## Insulation / breakdown

- Paschen's law — breakdown voltage vs pressure×gap for air; constants
  A = 15 cm⁻¹·Torr⁻¹, B = 365 V/(cm·Torr), γ = 0.01 (typical textbook values
  for air). The ~327 V Paschen minimum for air is the widely quoted
  literature value (alternate constant sets give ~305 V — see
  `docs/physics/README.md`).
- IEC 60664-1 — insulation coordination for equipment within low-voltage
  supply systems (altitude correction factors). (Paywalled — via secondary
  references.) https://webstore.iec.ch
- IEC 60071-2 — insulation coordination, application guide including
  altitude correction. (Paywalled — via secondary references.)
  https://webstore.iec.ch
- IPC-2221B — generic printed board design; clearance/creepage tables used
  as the cross-check for E2. https://www.ipc.org

## Thermal reliability

- Natural-convection heat-transfer textbooks (Incropera / Bergman et al.,
  *Fundamentals of Heat and Mass Transfer*) — basis for the lumped
  convection+radiation balance; the pressure scaling `h ∝ (p/p0)^0.8`
  applied here is the team's empirical assumption, not a textbook result.

## Battery, low temperature

- 18650 Li-ion cell datasheets (branded cells, e.g. Samsung/LG/Molicel
  class) — the ~80% usable-capacity at −20 °C anchor is per-datasheet
  [LITERATURE, chemistry-specific, not universal]. Always re-anchor to the
  datasheet of the cell you actually buy.

## Qualification standards

- JSS 55555:2012 — Indian military environmental test standard; the
  validation target for the eventual qualification framing.
- MIL-STD-810H — U.S. environmental engineering considerations; referenced
  as a complement, not a claim of compliance.

## Positioning (what we complement, not replace)

- Ansys Sherlock / Siemens PollEx / COMSOL — detailed physics solvers.
  HIMKAVACH's niche is the **low-cost, field-oriented, altitude-specific
  screening + physical correlation workflow** around them: cheap models up
  front, twin-board measurements that calibrate the models, and a risk
  verdict a field engineer can act on. We do not claim these tools
  "cannot" do anything — they solve a different (deeper, more expensive)
  problem.
