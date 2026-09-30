# HIMKAVACH Bill of Materials

**Status: PLAN — nothing has been purchased.** Prices are Indian-market
estimates compiled Sep 2026.

> **ESTIMATE — VERIFY BEFORE PURCHASE.** Prices move; confirm on the day
> you order. Quantities are for one twin-board prototype node.

## Simulation / prototype BOM

| Component | Specification | Purpose | Qty | Est. India price (₹) | Status |
|---|---|---|---|---|---|
| ESP32 dev board | ESP32-WROOM-32 | Controller + logging | 2 | 650 × 2 | Not purchased |
| PTC heater | 12 V, ~30 W, self-limiting | Controlled heat source for E1 | 2 | 250 × 2 | Not purchased |
| MOSFET module | e.g. IRFZ44N logic-level | Heater switching | 2 | 120 × 2 | Not purchased |
| 18650 cells | 3.7 V, 3000 mAh (branded, with datasheet) | 2S pack for E3 | 4 | 350 × 4 | Not purchased |
| BMS | 2S 18650 BMS board | Pack protection | 1 | 180 | Not purchased |
| Charger | TP4056 module | Cell charging | 1 | 90 | Not purchased |
| Temp sensors | DS18B20 (waterproof) | Thermal array, E1 | 4 | 150 × 4 | Not purchased |
| Pressure sensor | BMP280 module | Ambient pressure logging | 1 | 250 | Not purchased |
| Power monitor | INA219 module | V/I logging (E1, E3) | 2 | 220 × 2 | Not purchased |
| Display | 0.96" OLED I2C | Local readout | 1 | 280 | Not purchased |
| Storage | microSD module + card | CSV data logging | 1 | 350 | Not purchased |
| Power supply | 12 V 5 A adapter | Bench power | 1 | 450 | Not purchased |
| Misc | Wires, perfboard, enclosure | Assembly | 1 lot | 600 | Not purchased |

**Estimated total: ≈ ₹6,700** [ESTIMATE]. The single largest cost driver is
branded 18650 cells — do not substitute unbranded cells for a battery test.

## Future validation hardware (NOT purchased, NOT costed here)

- Glass desiccator + hand vacuum pump — *partial* low-pressure simulation
  only; honestly framed, never an altitude chamber.
- Chest freezer access (borrowed/shared) for E1/E3 cold testing.
- Accredited environmental chamber time — required for any real
  JSS 55555:2012-aligned qualification; far outside student budget, listed
  for roadmap honesty only.

## Explicit non-claims

- No component above has been ordered, received, or tested.
- No PCB has been fabricated.
- No measurements exist anywhere in this repository.
