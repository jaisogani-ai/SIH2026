"""
Paschen breakdown analysis — simulation/paschen/paschen_curve.py

Reproducible example: breakdown voltage of air gaps at sea level and at
Ladakh altitudes (Leh ~3.5 km, Chang La 5.36 km).

Run:
    python3 paschen_curve.py
    python3 paschen_curve.py --gap-mm 1.6 --voltage 2800

STATUS: SIMULATION. Computed from Paschen's law, not measured.
"""

import sys, os, math, argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from physics import (standard_atmosphere, clearance_breakdown_voltage,
                     paschen_minimum, SITE_LEH_M, SITE_CHANG_LA_M)  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Paschen breakdown screening")
    ap.add_argument("--gap-mm", type=float, default=0.8,
                    help="clearance gap in mm (default 0.8)")
    ap.add_argument("--voltage", type=float, default=2800.0,
                    help="applied peak voltage in V for margin check (default 2800)")
    args = ap.parse_args()

    pd_min, v_min = paschen_minimum()
    print("Paschen minimum (air, implemented constants): "
          "pd=%.3f Torr-cm, Vb=%.0f V [COMPUTED]" % (pd_min, v_min))
    print("Note: the widely quoted 327 V literature value comes from alternate")
    print("constant sets; the floor near ~300 V is the robust point.\n")

    sites = [("Sea level", 0.0), ("Leh (~3500 m)", SITE_LEH_M),
             ("Chang La (5360 m)", SITE_CHANG_LA_M)]
    print("%-18s %10s %12s %10s %10s" % ("site", "p(kPa)", "Vbd(V)", "margin", "verdict"))
    for name, h in sites:
        p, _ = standard_atmosphere(h)
        vbd = clearance_breakdown_voltage(args.gap_mm, p)
        margin = vbd / args.voltage
        verdict = "PASS" if margin >= 2.0 else ("REVIEW" if margin >= 1.25 else "REDESIGN")
        print("%-18s %10.1f %12.0f %10.2f %10s"
              % (name, p / 1000.0, vbd, margin, verdict))
    print("\n[COMPUTED] margins use Paschen's law with gamma=0.01, uniform field.")
    print("Real PCB clearances derate further (contamination, sharp edges).")


if __name__ == "__main__":
    main()
