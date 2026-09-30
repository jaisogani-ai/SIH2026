# Hardware component list

The authoritative component list lives in [`docs/bom/BOM.md`](../../docs/bom/BOM.md).

This folder tracks the *twin-board* build specifically:

- **Board A (control):** room conditions, full sensor set.
- **Board B (test):** freezer / cold-box conditions, full sensor set.

Planned sensor map per board (all [PLANNED] — nothing purchased):

| Sensor | Measures | Experiment |
|---|---|---|
| DS18B20 × 2 | Board + heater temperature | E1 |
| BMP280 × 1 | Ambient pressure | E1 (context) |
| INA219 × 1 | Heater V/I (E1) or pack V/I (E3) | E1, E3 |
| OLED | Local readout | both |
| microSD | CSV logging | both |

Build photos, wiring diagrams, and measured CSVs will be committed here
when the build exists. Until then: nothing to show, and we don't pretend
otherwise.
