# simulation/

Reproducible physics for HIMKAVACH. **Status: SIMULATION** — computed from
literature models, not measured data.

## Layout

- `common/physics.py` — shared library: standard atmosphere, Paschen's law,
  thermal model, battery model, risk engine. Each function documents its
  purpose, equation, assumptions, inputs, outputs, limitations, and source.
- `paschen/paschen_curve.py` — Vbd tables: sea level vs Leh vs Chang La.
- `thermal/thermal_model.py` — steady-state temperature tables.
- `battery/battery_model.py` — usable-energy / sag tables vs temperature.
- `risk-engine/risk_engine.py` — composite PASS / REVIEW / REDESIGN verdict.

## Run everything

```bash
pip install -r requirements.txt
python3 common/physics.py
python3 paschen/paschen_curve.py
python3 thermal/thermal_model.py
python3 battery/battery_model.py
python3 risk-engine/risk_engine.py
```

All scripts print `[COMPUTED]` / `[ASSUMPTION]` / `[LITERATURE]` tags next to
the claims they make. Regenerate every figure in the repo with:

```bash
python3 ../generate_figures.py
```
