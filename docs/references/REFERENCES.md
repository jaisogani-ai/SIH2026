# HIMKAVACH references

Real sources only. Nothing here is fabricated. Standards marked
(paywalled) could not be primary-verified; their factors are used via
secondary engineering references and flagged as such wherever they appear.
Research pass: 30 Sep 2026.

## DRDO / Indian government context (verified 30 Sep 2026)

- PIB, 3 Feb 2017 (PRID 1481715) — Lok Sabha reply by MoS Defence:
  Siachen winter clothing "designed to withstand extreme temperatures
  that even go below minus 50 degree Celsius"; FRP insulated shelters /
  insulated tents for troops.
  https://www.pib.gov.in/PressReleasePage.aspx?PRID=1481715&reg=3&lang=2
  (official)
- PIB, 10 Dec 2021 (PRID 1780097) — Lok Sabha reply by Raksha Rajya
  Mantri: troops in High Altitude Areas equipped with "Avalanche Victim
  Detectors, Trackers and Ricoh reflectors"; DGRE runs observatories and
  automated weather stations with near-real-time avalanche bulletins;
  SASE stations at Sasoma and Srinagar.
  https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=1780097&reg=3&lang=2
  (official)
- DRDO Soldier Support System cluster listing — DGRE (Chandigarh) and
  DIPAS (Delhi) listings, verified live 30 Sep 2026.
  https://drdo.gov.in/drdo/en/organisation/technology-cluster/life-sciences
  (official)
- DRDO Electronics & Communication Systems cluster — mandate "design and
  develop electronic, electro-optical and laser based sensors and
  systems"; DEAL (Dehradun) listing, verified live 30 Sep 2026.
  https://drdo.gov.in/drdo/en/organisation/technology-cluster/electronics-and-communication-systems
  (official)
- DIPAS Him-Taapak space-heating device — Army order "more than
  Rs 420 crores" per ANI (Jan 2021) quoting DIPAS Director
  Dr Rajeev Varshney.
  https://www.indiandefensenews.in/2021/01/amid-border-clash-drdo-develops.html
  (secondary news quoting DRDO official)
- iDEX DISC-11 — sought improved tank starter-generators and
  ultra-capacitors "for reliable engine starts in temperatures as low as
  −50°C" because "traditional batteries often fail to provide the
  necessary power in extreme cold."
  https://defence.in/threads/idex-seeks-innovations-for-upgraded-tank-starter-generators-and-ultra-capacitors-in-extreme-conditions.5641/
  (secondary; official idex.gov.in challenge page not located)
- Parliamentary record — Siachen equipment incl. surveillance radars,
  thermal imagers, UAVs, snow scooters.
  https://archive.org/download/eparlib.nic.in.693046/44873.pdf
  (official record via archive)
- Honesty note: DIHAR (Leh) is a cold-arid agro-animal / life-sciences
  lab (GoI portal:
  https://www.indiascienceandtechnology.gov.in/organisations/ministry-and-departments/defence-research-and-development-organisation-drdo-govt-india/defence-institute-high-altitude-research-dihar),
  not an electronics lab — its mandate is not cited for this problem.

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
  `docs/physics/README.md`). Constants A = 112.50 (kPa·cm)⁻¹,
  B = 2737.50 V·(kPa·cm)⁻¹; minimum at pd = 0.567 torr·cm:
  https://en.wikipedia.org/wiki/Paschen%27s_law and
  http://gbppr.net/mil/emp/jimlux/hv/paschen.htm (Jim Lux / JPL, Naidu data).
- FAA AC 43-206 — low-pressure effects on avionics materials (outgassing,
  seal breathing); no explicit corona-vs-altitude design rule found.
  https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_43-206_CHG_1.pdf
  (official)
- IEC 60664-1 — insulation coordination for equipment within low-voltage
  supply systems. Table A.2 altitude correction factors (×1.14 @ 3,000 m,
  ×1.29 @ 4,000 m, ×1.48 @ 5,000 m, ×1.70 @ 6,000 m) quoted via ABB
  application note:
  https://library.e.abb.com/public/dff53861b5b040bca99e754853560976/1SAC200234W0001_F_Application_Note_Low-voltage-high_altitudes.pdf
  (paywalled standard — via secondary reference). Worked example
  (TI SLUP419, 3.6 mm → 5.33 mm at 5,000 m): secondary mirror at
  https://github.com/averyy/pcbparts-mcp/blob/HEAD/data/design-rules/rules_sources/protection/isolation/ti-slup419-demystifying-clearance-and-creepage-distance.md
- IEC 60071-2 — insulation coordination, application guide including
  altitude correction. (Paywalled — via secondary references.)
  https://webstore.iec.ch
- IPC-2221B — generic printed board design; clearance/creepage Table 6-1
  used as the cross-check for E2. Note: uses B2/B3 altitude columns, NOT
  multiplicative altitude factors — the 1.14/1.29 figures sometimes
  attributed to it are IEC 60664-1 Table A.2 values. https://www.ipc.org
  (paywalled standard)

## Thermal reliability

- Natural-convection heat-transfer textbooks (Incropera / Bergman et al.,
  *Fundamentals of Heat and Mass Transfer*) — basis for the lumped
  convection+radiation balance; textbook correlations give h ∝ ρ^1/2
  (laminar) to h ∝ ρ^2/3 (turbulent). The pressure scaling
  `h ∝ (p/p0)^0.8` applied here is the team's deliberately conservative
  assumption (stronger derating than the textbook range), not a textbook
  result — see `docs/physics/README.md`.
- Industry derating practice: Flex DN025 forced-air derating factors for
  DC/DC modules (0.83 @ 3,000 m, 0.78 @ 4,000 m):
  https://dev-flex-main.pantheonsite.io/downloads/dn025-forced-air-cooling-at-high-altitude;
  ABB rated-current correction ∝ √(ph/pn) → 0.82 at 5,000 m (ABB
  application note, same URL as above).

## Battery, low temperature

- 18650 Li-ion cell datasheets (branded cells, e.g. Samsung/LG/Molicel
  class) — the ~80% usable-capacity at −20 °C anchor is per-datasheet
  [LITERATURE, chemistry-specific, not universal]. Always re-anchor to the
  datasheet of the cell you actually buy.
- EVE LF280N 3.2 V 280 Ah LiFePO₄ manufacturer product specification:
  discharge capacity at −20 °C ≥ 70% of typical (standard charge, 24 h rest
  at −20±2 °C, 1.0C to 2.0 V cutoff); ≥ 95% at 55 °C.
  https://batteryfinds.com/wp-content/uploads/2021/06/EVE-280Ah-Lithium-Iron-PhosphateLiFePO4-LFP-Battery-Cell-Product-Specification.pdf
  (secondary-hosted copy of the manufacturer spec)
- Arrhenius reliability model: R = A·exp(−Ea/kT); AF = exp[Ea/k ·
  (1/Tuse − 1/Tstress)]; Ea ≈ 0.3–1.0 eV, 0.7 eV conventional default.
  https://parts.jpl.nasa.gov/asic/Appendix.7.html (JPL),
  https://www.edn.com/models-predict-failure-rates/ (EDN),
  https://arxiv.org/pdf/0708.0369 (Meeker et al. review)

## Qualification standards

- JSS 55555:2012 — Indian military environmental test standard; the
  validation target for the eventual qualification framing. Test No. 3
  (Altitude) covers equipment "under simultaneously applied Service
  conditions of low air pressure and high or low temperature"; Test No. 20
  is Low Temperature, Test No. 17 High Temperature (from an unofficial
  Scribd copy of Rev. 3 — the spec is a controlled document with no
  official free text:
  https://www.scribd.com/document/410784337/JSS-55555-2012-pdf).
- MIL-STD-810H — U.S. environmental engineering considerations; referenced
  as a complement, not a claim of compliance. Method 500.6 (Low
  Pressure/Altitude): storage/air transport, operation/air carriage, rapid
  decompression; Method 502.7 (Low Temperature): storage, operation,
  manipulation in cold-weather clothing (secondary descriptions:
  https://en.wikipedia.org/wiki/MIL-STD-810).
- Honesty note: no verifiable public source was found attributing an
  electronic equipment failure to high altitude, low pressure, arcing, or
  extreme cold (research pass 30 Sep 2026).

## Positioning (what we complement, not replace)

- Ansys Sherlock / Siemens PollEx / COMSOL — detailed physics solvers.
  HIMKAVACH's niche is the **low-cost, field-oriented, altitude-specific
  screening + physical correlation workflow** around them: cheap models up
  front, twin-board measurements that calibrate the models, and a risk
  verdict a field engineer can act on. We do not claim these tools
  "cannot" do anything — they solve a different (deeper, more expensive)
  problem.
