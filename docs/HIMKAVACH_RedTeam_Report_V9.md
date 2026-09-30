# HIMKAVACH — Final Red-Team Engineering Review (V9)

**Date:** 30 September 2026
**Scope:** Rev A blueprint (10 pp) · `simulation/` repo (`github.com/jaisogani-ai/SIH2026`, HEAD `cf52bdb`) · deployed app `https://himkavach.grok.me` (JS audited 30 Sep 2026) · BOM · references
**Reviewer role:** final red-team engineering reviewer. Job: find what a judge can break in 30 seconds, fix it honestly, hide nothing.

## Standing decisions (read first)

- **D1 — Evidence taxonomy.** The review brief's §3 lists 8 classes (adds IMPLEMENTED, SIMULATED as bracketed tags). The user's standing rule (30 Sep, explicit, repeated) mandates **exactly six** bracketed classes: `MEASURED`, `COMPUTED`, `LITERATURE`, `ASSUMPTION`, `ESTIMATE`, `PROPOSED / FUTURE VALIDATION`. I keep the six-class rule. `IMPLEMENTED DIGITAL PROTOTYPE` and the word "simulated" remain as **plain prose status words, never bracketed tags**. Rationale: switching taxonomy mid-programme would silently reclassify every tagged value in the repo and both documents.
- **D2 — No GitHub push performed** (user instruction 30 Sep 14:28; also the standing no-push-without-authorization rule). All V9 artefacts are local files; the proposed README and repo tree are proposals, not commits.
- **D3 — "9/10" is a target, not a certificate.** Residual gaps are listed in §12 and in the document's own limitations — a transparent limitation beats a false claim.

---

## 1. RED FLAGS FOUND

**RF-01 (HIGH) — Wrong-chemistry datasheet behind the battery anchor.** Ref [10] cites the EVE LF280N (≥70% @ −20 °C) as the battery reference. The LF280N is a **LiFePO4 prismatic 280 Ah cell** — wrong chemistry, wrong form factor, wrong capacity class versus the proposed **2S1P 18650 NMC pack**. The −20 °C battery anchor therefore has **no valid datasheet behind it**. → Remove the reference; the anchor becomes `ASSUMPTION`.

**RF-02 (HIGH) — Two different battery models.** The deployed app uses a lookup table (`−40 °C: 15% estimate · −30 °C: 32.8% 'literature' · −20 °C: 77.4% 'literature' · −10 °C: 88% · 25 °C: 100%` — read from the app's own JS). The repo's `battery_usable_fraction` is linear (1.00 → 0.80 @ −20 °C, floor 0.25 @ −40 °C). Rev A §7.2 quotes the repo; the §5 screenshot shows the app. A judge comparing "−20 °C" in the two places finds two different numbers. → Disclose both, name the source of each, never mix.

**RF-03 (HIGH) — Two different thermal models.** The app uses a **Theta-JA junction model** (`power_W: 8, thetaJA_sea: 12 °C/W, JA scale ×1.20 @ 5,364 m, Tjmax 125 °C` — from the app's JS; reproduces the site's 122.0 / 100.6 °C). The repo's `thermal_rise` is a **lumped-surface model** (2 W, 0.008 m², h0 = 8 W/m²K). The site's "Junction" temperatures cannot be reproduced from `simulation/thermal/thermal_model.py`. → Disclose; the blueprint must not claim the site "implements `simulation/common/physics.py`" without qualification. Also: the repo model yields a *surface* temperature — the blueprint should not let "junction" stand unqualified for the repo path.

**RF-04 (HIGH) — The site's battery scenario is not the proposed hardware.** The app's Mission defaults are `pack_Wh: 100, load_W: 20` — a **100 Wh placeholder pack**. "Usable 83.3 Wh" = 83.3% of that placeholder. The proposed hardware is a **2S1P 18650, 22.2 Wh** pack. A reader who misses this thinks the hardware was sized at 100 Wh. → State the placeholder explicitly in §5.

**RF-05 (MEDIUM) — Cell count mismatch.** BOM lists 4× 18650 for a 2S pack; `battery_model.py` uses `PACK_CELLS = 2` (2S1P, 22.2 Wh). Unexplained. → 2 for the pack + 2 spares for E3 repeats.

**RF-06 (MEDIUM) — Heater rating vs modelled load.** PCB/§7.2 say "2 W thermal loads"; BOM says "12 V ~30 W PTC heaters". A reader sees 2 W in the model and 30 W in the BOM. → Clarify: the 30 W PTC is the heater's *capacity*; E1 drives it derated (PWM via IRLZ44N) to deliver the 2 W test dissipation.

**RF-07 (MEDIUM) — False claim inside `physics.py`.** Module docstring: "Literature value reproduced: Paschen minimum ~327 V for air." With the module's own constants (A=15, B=365, γ=0.01) the minimum is **305.3 V**, not 327 V. The docstring contradicts its own code. → Fix the docstring (applied locally; see §2).

**RF-08 (MEDIUM) — "Per-datasheet" battery anchor with no datasheet on file.** `battery_usable_fraction` docstring: "Anchored to a per-datasheet literature point: ~80% usable at −20 °C [LITERATURE]". Combined with RF-01, no 18650 datasheet is on file. → Reword to `ASSUMPTION` (applied locally; see §2).

**RF-09 (MEDIUM) — Mistagged requirement band.** D1 layer 1: "SIH26049: 3,000–6,000 m · −35…+40 °C [LITERATURE]". PS SIH26049 states HAA/SHAA subzero + low pressure **without numeric bands**; the bands are the team's requirement interpretation. → Retag `[ASSUMPTION — team's requirement interpretation]`.

**RF-10 (MEDIUM) — Unverifiable clearance-margin readout.** The site's comparison table shows "clearance margin 2.50 vs 1.00". The margin formula is **not in the repo** (web-app source is not in the repo). It is plausibly ≈2.8 kV applied on 1.5 mm with IEC derating, but the exact 1.00 cannot be reproduced from repo code. → Standing action: document the formula in-app or align (R-09).

**RF-11 (LOW) — Bracketed `[IMPLEMENTED]`** in the §8.1 column header and ref [12] violates the six-class rule. → Prose form: "(IMPLEMENTED DIGITAL PROTOTYPE)".

**RF-12 (LOW) — "SIMULATED" used tag-like** in §4 ("all outputs COMPUTED / SIMULATED") and §5 ("badged COMPUTED / SIMULATED", "all SIMULATED"). → Normalize to `[COMPUTED]`.

**RF-13 (LOW) — App's 'literature' battery anchors unsourced.** The app's JS labels −30 °C 32.8%, −20 °C 77.4%, −10 °C 88% as `kind: 'literature'`; no source documents are in the repo. → `REFERENCE TO VERIFY` before the blueprint cites them as literature.

**RF-14 (LOW) — App source not in repo.** The blueprint's "Computation source: simulation/" needs the qualifier that the deployed app is a **separate implementation** (its JS is not in the repo). → Added to §5 and limitations.

**Positive controls (audited, no issue):** IEC factor interpolation 1.560 @ 5,364 m ✓ · stat cards 51.44 kPa / 0.693 kg/m³ / ρ 0.565 with the −14.4 °C ambient override (consistent, not ISA — the override is the point) ✓ · Paschen minimum **agrees** site↔repo (305.3 V both; the site uses A=112.5/B=2737.5 which has the identical B/A ratio) ✓ · hand-pump conversion 63.5 cm Hg → ≈16.6–17 kPa abs ✓ · 2S electrical chain 7.4/8.4/6.0 V + BMS + TP5100 ✓ · charge-lock < 0 °C (standard Li-ion guidance) ✓ · DIHAR correction ✓ · HV simulation-only rule ✓ · no hardware photographs in the blueprint (photo policy satisfied trivially) ✓ · site's own honesty ("Simulation only", "computed" badges, "not a digital twin and not a certification") ✓.

---

## 2. TECHNICAL CORRECTIONS

- **TC-01** — `simulation/common/physics.py` module docstring: *"Literature value reproduced: Paschen minimum ~327 V for air."* → *"With these constants the computed minimum is 305.3 V at pd = 0.8375 Torr·cm [COMPUTED]. Textbooks commonly quote ≈327 V; the exact minimum depends on the (A, B, γ) set chosen."* (Applied locally, unpushed.)
- **TC-02** — `battery_usable_fraction` and `simulation/battery/battery_model.py` docstrings: *"Anchored to a per-datasheet literature point"* → *"Engineering estimate [ASSUMPTION]; no specific 18650 datasheet is on file — cell TBD before purchase."* (Applied locally, unpushed.)
- **TC-03** — D1 layer-1 band: `[LITERATURE]` → `[ASSUMPTION — team's requirement interpretation; PS states HAA/SHAA subzero + low pressure without numeric bands]`.
- **TC-04** — BOM BAT-01 qty `4` → `2 + 2 spares` (2S1P pack + E3 repeats).
- **TC-05** — BOM THM-01/02 spec → *"12 V PTC, ~30 W max, run derated to the 2 W E1 test load via PWM [ASSUMPTION]"*.
- **TC-06** — §7.2: add reference-conditions note (all anchors at ISA unless stated) and the site-vs-repo scenario note.
- **TC-07** — §8: add the single battery-architecture box (see §6).
- **TC-08** — §5: document the site's actual scenario parameters + the two-implementations disclosure (see §7).
- **TC-09** — Risk register: add R-09 (model divergence) and R-10 (100 Wh placeholder).
- **TC-10** — §10.2: remove/replace EVE ref; fix ref [12]; add app-source note.

## 3. CLAIMS THAT MUST BE REMOVED

1. Ref [10] EVE LF280N as the 18650 battery reference (wrong chemistry — RF-01).
2. "Anchored to a per-datasheet literature point" for the −20 °C value (no datasheet on file — RF-08).
3. `physics.py`'s "Literature value reproduced: Paschen minimum ~327 V" (false for its constants — RF-07).
4. "Cell datasheet (≥70% @ −20 °C)" in §8.1 R5 (the 70% was the LF280N).
5. Any implication that the site's 100 Wh / 83.3 Wh battery scenario describes the proposed 22.2 Wh hardware (RF-04).

## 4. CLAIMS THAT SHOULD BE REPHRASED

| # | Before (Rev A) | After (V9) | Why |
|---|---|---|---|
| 1 | "all outputs COMPUTED / SIMULATED and badged as such" (§4) | "all outputs [COMPUTED] and badged as such" | RF-12, six-class rule |
| 2 | "Every output on the site is badged COMPUTED / SIMULATED" (§5) | "Every output on the site is badged [COMPUTED]" | RF-12 |
| 3 | "Graphs … all SIMULATED" (§5) | "Graphs … all [COMPUTED] simulation figures" | RF-12 |
| 4 | "0.80 usable @ −20 °C [COMPUTED from LITERATURE-anchored model]" (§7.1 FM-03) | "0.80 usable @ −20 °C [COMPUTED from repo model — anchor ASSUMPTION until a specific 18650 datasheet is selected]" | RF-01/08 |
| 5 | "charging below 0 °C plates lithium [LITERATURE]" (FM-03) | "charging below 0 °C plates lithium [LITERATURE, general manufacturer guidance]" | precision |
| 6 | "0.80 @ −20 °C (datasheet anchor)" (§7.2) | "0.80 @ −20 °C [ASSUMPTION — no 18650 datasheet on file; cell TBD]" | RF-01/08 |
| 7 | "Paschen minimum … vs ~327 V quoted in literature with other constant sets" (§7.2) | "vs ≈327 V commonly quoted in textbooks; the exact minimum depends on the (A, B, γ) set — ours gives 305.3 V [COMPUTED]" | avoid false attribution |
| 8 | "Simulator [IMPLEMENTED]" (§8.1 header) | "Simulator (IMPLEMENTED DIGITAL PROTOTYPE)" | RF-11 |
| 9 | "[12] … (screenshot §5). [IMPLEMENTED]" | "[12] … (screenshot §5). (IMPLEMENTED DIGITAL PROTOTYPE — software only)" | RF-11 |
| 10 | "IEC 60664-1 Tab. A.2" bare (§8.1) | "IEC 60664-1 Table A.2 (secondary citation — paywalled)" | §7 honesty |
| 11 | D1 "SIH26049: 3,000–6,000 m · −35…+40 °C [LITERATURE]" | "… [ASSUMPTION — team's requirement interpretation]" | RF-09 |

## 5. REFERENCES THAT NEED VERIFICATION

- **[5] IEC 60664-1 Table A.2 factors** — secondary citation; standard paywalled, not primary-verified. Keep the flag. (Corroboration: the deployed app independently cites "IEC 60664-1:2007 Table A.2" — still secondary.)
- **[7] JSS 55555 Rev. 3, Test No. 3** — unofficial copy of a controlled document. Keep the flag.
- **App's battery 'literature' anchors** (77.4% @ −20 °C, 88% @ −10 °C, 32.8% @ −30 °C) — source documents not in the repo. **REFERENCE TO VERIFY** before the blueprint cites them as literature.
- **IRLZ44N Vgs(th) 1–2 V; TP5100 2S/8.4 V mode** — standard public specs; attach the manufacturer datasheets at purchase (note added to N1/N2).
- **"≈327 V" textbook Paschen minimum** — commonly quoted; exact (A, B, γ) attribution not verified — reworded per §4 #7.
- **[10] slot** — replaced with an explicit TBD: no 18650 datasheet on file.

## 6. BATTERY CONSISTENCY FIX — the single architecture

There is now **one** battery architecture, stated identically in §3 (PCB), §7, §8 (BOM) and the README:

- **Configuration:** 2S1P 18650 · **7.4 V nominal · 8.4 V max · 6.0 V cutoff · 22.2 Wh rated** (3000 mAh-class cells)
- **Cell:** branded 18650 with published datasheet — **ASSUMPTION — CELL TO BE VERIFIED BEFORE PURCHASE** (no cell selected; no datasheet on file; unbranded cells excluded from E3 by safety rule)
- **Protection:** 2S BMS (HX-2S class) · **Charger:** TP5100 in 2S/8.4 V mode (TP4056 is single-cell and cannot charge 2S — corrected N2)
- **Charge-lock:** no charging below 0 °C (lithium-plating risk) [LITERATURE, general manufacturer guidance] · heater pre-warm via BAT-IF/HTR-IF [PROPOSED]
- **Model:** repo curve 1.00 / 1.00 / 0.80 / 0.25 @ 25/0/−20/−40 °C [COMPUTED from ASSUMPTION-anchored model]; self-heating not credited [ASSUMPTION]; E3 measures the real discharge curve
- **Simulator note:** the deployed app's Mission page uses its **own** lookup-table curve (77.4% @ −20 °C) and a **100 Wh placeholder pack** — disclosed in §5, never mixed with the hardware numbers.

## 7. SIMULATOR / BLUEPRINT CONSISTENCY FIX

| Parameter | Repo → blueprint §7.2 anchors | Deployed app → §5 screenshot | Disposition |
|---|---|---|---|
| Atmosphere @ 5,360 m | 51.47 kPa, −19.84 °C (ISA) [COMPUTED] | 51.44 kPa @ 5,364 m, ambient override −14.4 °C | Consistent — different operating points, both stated |
| Paschen minimum | 305.3 V @ 0.8375 Torr·cm (A=15, B=365, γ=0.01) | 305.3 V (A=112.5, B=2737.5 — identical B/A ratio) | **Consistent ✓** |
| Vbd (0.8 mm) | 4.198 → 2.446 kV [COMPUTED] | App defaults 1.5 mm / 100 V / γ=0.01 (different scenario) | Disclosed as scenario difference |
| Thermal | Lumped surface: 2 W/0.008 m² → 18.7 K / 29.1 K rise [COMPUTED] | Theta-JA: 8 W, 12 °C/W, ×1.20 → 122.0 / 100.6 °C "junction" [COMPUTED] | Different models — disclosed, both [COMPUTED] |
| Battery | Linear: 80% @ −20 °C; 22.2 Wh pack | Lookup: 77.4% @ −20 °C; **100 Wh placeholder** pack | Disclosed; align-or-version action (R-09) |
| Clearance margin 2.50→1.00 | — (app-only readout) | Formula not in repo | Document-or-align (R-09) |
| IEC factor | ×1.48 @ 5 km (Table A.2) | 1.560 @ 5,364 m (interpolated) | Consistent ✓ |

Rule applied throughout: **document the difference; never silently change a scientific result to make the numbers match.** The blueprint now states, per value, whether it comes from `simulation/` or from the deployed app.

## 8. FINAL V9 BLUEPRINT STRUCTURE (10 pages)

Same skeleton as Rev A (all strong sections kept: five-layer architecture · digital physics screening · electronics digital representation · physical validation pathway · measured/computed separation · failure→mitigation→validation matrix · traceability · BOM · risk register · phased roadmap). Changes are **corrections and disclosures only**:

- P1 — §4 wording fix (#1); legend gains the taxonomy note (D1).
- P2 — D1: layer-1 band retagged [ASSUMPTION] (TC-03).
- P3 — BAT-IF bullet gains the pack electrical definition (§6).
- P4 — unchanged (rig diagram already honest).
- P5 — "Reading the screenshot" rewritten: site scenario parameters, two-implementations disclosure, placeholder-pack statement; data-flow line fix (#3); DIHAR correction kept.
- P6 — unchanged.
- P7 — FM-03 reword (#4, #5); §7.2 reference-conditions note (TC-06); battery bullet reword (#6); site-vs-repo note (TC-06); Paschen reword (#7); E1 heater clarification (RF-06).
- P8 — table header fix (#8); R5 fix; battery-architecture box (TC-07); BAT-01 qty (TC-04); THM spec (TC-05); IEC citation flag (#10).
- P9 — N3 cell-TBD note; R-09/R-10 added (TC-09); N1/N2 datasheet-at-purchase notes.
- P10 — ref [10] replaced with TBD slot; ref [12] fix (#9); app-source limitation; battery-anchor verification note (RF-13).

## 9. EXACT TEXT CHANGES PAGE-BY-PAGE

Applied in `~/workspace/sih2026-blueprint/build_pdf.py` (V9 generator) and `diagrams.py` (D1 band retag). The PDF is rebuilt from these sources — no hand edits.

- **P1 §4:** "all outputs COMPUTED / SIMULATED and badged as such" → "all outputs [COMPUTED] and badged as such".
- **P1 legend:** add row-note: "IMPLEMENTED and SIMULATED appear in this document only as plain status words (e.g. 'IMPLEMENTED DIGITAL PROTOTYPE'), never as bracketed evidence tags."
- **P1 §2:** unchanged (already states no measurements).
- **D1 (P2):** "SIH26049: 3,000–6,000 m · −35…+40 °C [LITERATURE]" → "… [ASSUMPTION — team's requirement interpretation]".
- **P3 BAT-IF bullet:** append "Pack: 2S1P 18650, 7.4 V nominal / 8.4 V max / 6.0 V cutoff, 22.2 Wh (3000 mAh-class cells — ASSUMPTION, cell TBD)."
- **P5 "Reading the screenshot":** replaced with the site-scenario + two-implementations disclosure (§7 of this report, condensed).
- **P5 data-flow:** "COMPUTED results → SIMULATED figures & risk index" → "COMPUTED results → figures & risk index".
- **P7 FM-03:** per §4 #4/#5. **P7 §7.2:** per §4 #6/#7 + reference-conditions note + site-vs-repo note + heater clarification.
- **P8:** per §4 #8/#10; battery-architecture box; BAT-01 "2 + 2 spares"; THM-01/02 derated-PWM note.
- **P9:** N3 += "Exact cell TBD — ASSUMPTION — CELL TO BE VERIFIED BEFORE PURCHASE."; add R-09/R-10; N1/N2 += "datasheet to be attached at purchase."
- **P10:** ref [10] → "18650 cell datasheet — NOT YET SELECTED. No cell datasheet is on file; the −20 °C anchor is ASSUMPTION. [ASSUMPTION — CELL TO BE VERIFIED BEFORE PURCHASE]"; ref [12] per §4 #9; limitations += app-source note + battery-anchor verification note (RF-13).

## 10. FINAL GITHUB FILE STRUCTURE (proposed — not pushed)

```
SIH2026/
├── README.md                        ← rewritten per §11
├── LICENSE
├── simulation/
│   ├── common/physics.py            ← TC-01/TC-02 docstring fixes (local, unpushed)
│   ├── battery/battery_model.py     ← TC-02 docstring fix (local, unpushed)
│   ├── thermal/thermal_model.py
│   ├── paschen/paschen_curve.py
│   └── risk-engine/risk_engine.py
├── hardware/
│   └── bom/                         ← 2S1P clarification (proposed)
├── docs/
│   ├── HIMKAVACH_Hardware_Blueprint_V9.pdf
│   ├── validation-plan.md           ← E1/E2/E3 procedures (to write)
│   ├── risk-register.md             ← P9 register as standalone (to write)
│   └── requirements-traceability.md ← P8.1 as standalone (to write)
├── diagrams/                        ← D1–D4 PNGs
├── screenshots/
│   └── simulator_mission_2026-09-30.png  ← the real screenshot, badged software-only
├── results/
│   └── computation_log_2026-09-30.txt
└── presentation/                    ← SIH deck (existing)
```

`docs/validation-plan.md`, `docs/risk-register.md`, `docs/requirements-traceability.md` are extracted from V9 §§7–9 — proposed, not yet written; writing them is the next documentation step after V9.

## 11. FINAL README CONTENT (proposed — `~/workspace/your_files/HIMKAVACH_README_proposed.md`)

```markdown
# HIMKAVACH — Physics-Guided Reliability Screening for High-Altitude Electronics

**PS SIH26049 (DRDO)** · Team ALPHA 20 · Live simulator: https://himkavach.grok.me

> **What this is:** an IMPLEMENTED DIGITAL PROTOTYPE (web simulator) plus a
> hardware validation blueprint. **No PCB has been fabricated, no components
> purchased, no physical measurements exist.** Every number in this repo carries
> one evidence tag: MEASURED · COMPUTED · LITERATURE · ASSUMPTION · ESTIMATE ·
> PROPOSED / FUTURE VALIDATION.

## Status at a glance
- **IMPLEMENTED:** web simulator (physics screening, risk index, comparison tables).
  All its outputs are COMPUTED — simulation output, not measurements.
- **COMPUTED:** `simulation/` — atmosphere, Paschen clearance, thermal, battery,
  risk engine. Re-run: `python3 simulation/common/physics.py`.
- **PROPOSED:** TEST-PCB-01 layout, validation rig, experiments E1/E2/E3.
- **FUTURE VALIDATION:** chamber testing per JSS 55555 Test No. 3 class.
- **NOT MEASURED:** the measured-data track is specified end-to-end and empty
  by design. It fills only when the rig runs. The model loses every tie:
  discrepancies are reported as error bands, never used to overwrite data.

## Reproduce
`python3 simulation/common/physics.py` · `python3 simulation/battery/battery_model.py`
`python3 simulation/thermal/thermal_model.py` · `python3 simulation/paschen/paschen_curve.py`
See `results/computation_log_2026-09-30.txt` for the logged anchors.

## Battery architecture (single, consistent)
2S1P 18650 · 7.4 V nominal / 8.4 V max / 6.0 V cutoff · 22.2 Wh (3000 mAh-class,
ASSUMPTION — CELL TO BE VERIFIED BEFORE PURCHASE) · 2S BMS · TP5100 2S charger ·
charge-lock below 0 °C. No cell datasheet is on file.

## Documents
- `docs/HIMKAVACH_Hardware_Blueprint_V9.pdf` — the full blueprint
- `docs/validation-plan.md`, `docs/risk-register.md`, `docs/requirements-traceability.md`
- `diagrams/` · `screenshots/` (simulator only — software evidence, never hardware)

## Limitations (read before citing)
- Student engineering document. Not DRDO-certified. No DRDO logo.
- IEC 60664-1 factors via secondary citation (paywalled); JSS 55555 via unofficial copy.
- The deployed app's battery/thermal implementations differ in detail from
  `simulation/` (lookup-table vs linear battery curve; Theta-JA vs lumped thermal);
  both are COMPUTED screening models — see blueprint §5/§7.2, do not mix the sets.
```

## 12. FINAL JUDGE ATTACK QUESTIONS + ANSWERS

### A. DRDO hardware engineer

1. **"Your −20 °C battery number — which cell's datasheet?"**
   None on file. V9 states it plainly: the 0.80 anchor is ASSUMPTION until a specific branded 18650 is selected (RF-01/08, §6). E3 exists to measure the real curve. A disclosed assumption beats a borrowed LiFePO4 datasheet.
2. **"You cite IEC 60664-1 but haven't read it — the factors are paywalled."**
   Correct, and the document says so twice (§7.2, §10.2): secondary citation, not primary-verified, used as design guidance — never claimed as compliance.
3. **"A hand-pump desiccator is not altitude qualification."**
   Agreed — V9 frames it as partial room-temperature pressure-response only (R-03, §10.1). Only a combined-environment chamber qualifies; that's Phase 4, outside student budget, stated openly.
4. **"Your convection exponent 0.8 contradicts textbooks (0.5–0.67)."**
   Known and disclosed: 0.8 is deliberately conservative, flagged ASSUMPTION, and E1's entire purpose is to calibrate it (R-01, FM-01).
5. **"Where is the measured data?"**
   There is none — page 1 says so, the MEASURED track is specified-but-empty by design, and the data architecture (§6) exists precisely so future measurements can't be silently mixed with simulation.

### B. SIH hardware evaluator

1. **"Is any hardware actually built?"**
   No. IMPLEMENTED = the web simulator only. The blueprint's first page, every diagram stamp, and the BOM ("Not purchased") say so.
2. **"Your simulator and your repo disagree on the battery curve."**
   Yes — disclosed in V9 §5/§7.2 with both curves named (RF-02). Both are COMPUTED; the blueprint's anchors come from the repo, the screenshot from the app, each labelled.
3. **"The site shows a 100 Wh battery but your BOM is 22.2 Wh."**
   The site's 100 Wh is a scenario placeholder (RF-04); the hardware is 2S1P 22.2 Wh. V9 states this on the screenshot page so nobody mistakes one for the other.
4. **"Why should we believe the Paschen numbers?"**
   Because they're reproducible: `paschen_minimum()` in `physics.py`, both constant sets in use give 305.3 V, the 327 V textbook figure is disclosed as a different constant set — and E2 stays simulation-only so no student ever tests it with hardware.
5. **"What exactly will you measure first?"**
   E1 (thermal: freezer + desiccator, T1–T3 resolve ambient vs component) and E3 (cold discharge of the 2S1P pack with charge-lock) — procedures in the validation plan, Phase 1, with the measured track ready to receive them.

### C. Skeptical technical founder / investor

1. **"This is a simulator, not a product. What's real?"**
   The physics screening workflow is real and reproducible; the validation pathway (PCB → rig → chamber) is engineered on paper. What's not real yet: every measurement. V9 never blurs that line.
2. **"Why would DRDO care about a student simulator?"**
   It wouldn't, as a product. The honest positioning (kept from Rev A): pre-qualification screening for the altitude trio that Sherlock-class tools don't model as one workflow — it complements chambers and standards, never replaces them.
3. **"Your BOM is ₹6,800 of unpurchased parts. What's the real cost to first data?"**
   ₹6,800 [ESTIMATE — VERIFY BEFORE PURCHASE] to first E1/E3 data; chamber time is deliberately un-costed and flagged as the step that needs institutional access (N5, R-06).
4. **"Two battery models, two thermal models — which one is right?"**
   Neither is "right" — both are screening models with stated assumptions. The repo is the reference implementation; the app is the deployed variant. R-09 tracks aligning them. A founder who asks this gets the table in §7, not a hand-wave.
5. **"What kills this project?"**
   No chamber access (R-06), an uncalibrated convection exponent (R-01), or measuring a no-name cell and calling it data (N3/R-04). All three are in the risk register with dispositions. That's the point of the register.

---

**Reviewer sign-off:** V9 corrects every red flag above without inventing a single measurement, datasheet, or validation result. Residual limitations (R-09 alignment, app-source publication, cell selection, chamber access) are tracked in the open. The document a judge reads now is the document the evidence supports — nothing more.
