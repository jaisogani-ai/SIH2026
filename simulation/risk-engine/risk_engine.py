"""
Risk engine — simulation/risk-engine/risk_engine.py

Reproducible example: combine the three mechanism margins into one
screening verdict (PASS / REVIEW / REDESIGN) for a design point at
Chang La conditions.

Run:
    python3 risk_engine.py
    python3 risk_engine.py --thermal-margin 12 --insul-margin 1.6 --batt-margin 1.8

STATUS: SIMULATION. Thresholds and weights are team-chosen [ASSUMPTION],
not a standard. This is a screening aid, never a qualification verdict.
"""

import sys, os, argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "common"))
from physics import risk_index  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="HIMKAVACH risk engine")
    ap.add_argument("--thermal-margin", type=float, default=8.0,
                    help="(T_limit - T_predicted) in C")
    ap.add_argument("--insul-margin", type=float, default=1.4,
                    help="Vbd_predicted / V_applied")
    ap.add_argument("--batt-margin", type=float, default=1.2,
                    help="usable_energy / required_energy")
    args = ap.parse_args()

    index, verdict = risk_index(args.thermal_margin, args.insul_margin,
                                args.batt_margin)
    print("thermal margin : %6.1f C" % args.thermal_margin)
    print("insulation     : %6.2f x Vbd/Vapplied" % args.insul_margin)
    print("battery        : %6.2f x energy margin" % args.batt_margin)
    print("RISK INDEX     : %.3f  ->  %s" % (index, verdict))
    print("\n[ASSUMPTION] verdict thresholds (0.75 / 0.50) are team-chosen.")
    print("Workflow: Environment -> Physics -> Risk -> Mitigation ->")
    print("          Physical validation -> Model calibration.")


if __name__ == "__main__":
    main()
