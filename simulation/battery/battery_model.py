"""
Cold-battery analysis — simulation/battery/battery_model.py

Reproducible example: usable energy and voltage sag of a 2S 18650 pack
(7.4 V nominal) across temperature, for a fixed load.

Run:
    python3 battery_model.py
    python3 battery_model.py --load-a 1.5 --need-wh 12

STATUS: SIMULATION. Empirical derating curve, not a measured discharge curve.
The -20 C anchor (~80% usable) is per-datasheet [LITERATURE, chemistry-specific].
"""

import sys, os, argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from physics import (battery_usable_fraction, battery_internal_resistance_factor,
                     standard_atmosphere, SITE_LEH_M, SITE_CHANG_LA_M)  # noqa: E402

CELL_RATED_WH = 3.7 * 3.0      # 3.7 V x 3000 mAh generic 18650 [ASSUMPTION]
PACK_CELLS = 2                 # 2S configuration
PACK_NOMINAL_V = 7.4
DCIR_25C_OHM = 0.06            # per-cell DCIR at 25 C [ASSUMPTION]
CUTOFF_V = 6.0                 # 2S pack cutoff [ASSUMPTION]


def main():
    ap = argparse.ArgumentParser(description="Cold-battery screening")
    ap.add_argument("--load-a", type=float, default=1.0, help="load current [A]")
    ap.add_argument("--need-wh", type=float, default=10.0,
                    help="energy the mission requires [Wh]")
    args = ap.parse_args()

    temps_c = [25.0, 0.0, -10.0, -20.0, -30.0]
    print("%-8s %10s %10s %10s %10s" % ("T(C)", "usable(Wh)", "sag(V)",
                                        "margin", "verdict"))
    for t in temps_c:
        usable = PACK_CELLS * CELL_RATED_WH * battery_usable_fraction(t)
        r_pack = PACK_CELLS * DCIR_25C_OHM * battery_internal_resistance_factor(t)
        sag = args.load_a * r_pack
        margin = usable / args.need_wh
        verdict = "PASS" if margin >= 1.5 else ("REVIEW" if margin >= 1.0 else "REDESIGN")
        print("%-8.0f %10.1f %10.2f %10.2f %10s" % (t, usable, sag, margin, verdict))
    print("\n[COMPUTED] derating curve is an engineering estimate below -20 C.")
    print("Real packs need a measured discharge curve per cell chemistry.")


if __name__ == "__main__":
    main()
