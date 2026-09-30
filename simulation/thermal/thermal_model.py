"""
Thermal derating analysis — simulation/thermal/thermal_model.py

Reproducible example: steady-state temperature of a dissipating board at
sea level vs Ladakh altitudes, showing reduced convection at low pressure.

Run:
    python3 thermal_model.py
    python3 thermal_model.py --power 8 --area 0.012

STATUS: SIMULATION. Lumped model with assumed convection scaling, not measured.
"""

import sys, os, argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from physics import standard_atmosphere, thermal_rise, SITE_LEH_M, SITE_CHANG_LA_M  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Thermal derating screening")
    ap.add_argument("--power", type=float, default=6.0, help="dissipated power [W]")
    ap.add_argument("--area", type=float, default=0.01, help="cooled area [m^2]")
    ap.add_argument("--tlimit", type=float, default=85.0,
                    help="component temperature limit [C]")
    args = ap.parse_args()

    sites = [("Sea level", 0.0), ("Leh (~3500 m)", SITE_LEH_M),
             ("Chang La (5360 m)", SITE_CHANG_LA_M)]
    print("%-18s %8s %10s %10s %10s" % ("site", "Tamb(C)", "Tsurface(C)",
                                        "margin(C)", "verdict"))
    for name, h in sites:
        p, t_amb = standard_atmosphere(h)
        ts, conv, rad = thermal_rise(args.power, args.area, t_amb, p)
        ts_c = ts - 273.15
        margin = args.tlimit - ts_c
        verdict = "PASS" if margin >= 20 else ("REVIEW" if margin >= 0 else "REDESIGN")
        print("%-18s %8.1f %10.1f %10.1f %10s"
              % (name, t_amb - 273.15, ts_c, margin, verdict))
    print("\n[COMPUTED] h(p) = h0*(p/p0)^0.8 is an ASSUMED natural-convection")
    print("scaling, not a measured coefficient for this geometry.")


if __name__ == "__main__":
    main()
