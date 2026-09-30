"""
Generate all repo figures: screenshots/graphs/*.png (all marked SIMULATION)
and docs/architecture/himkavach-architecture.{png,svg}.

Run:  python3 generate_figures.py
"""

import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "simulation", "common"))
from physics import (standard_atmosphere, clearance_breakdown_voltage,
                     paschen_breakdown_voltage, thermal_rise,
                     battery_usable_fraction, PA_PER_TORR)

ROOT = os.path.dirname(os.path.abspath(__file__))
GRAPH_DIR = os.path.join(ROOT, "screenshots", "graphs")
ARCH_DIR = os.path.join(ROOT, "docs", "architecture")
os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(ARCH_DIR, exist_ok=True)

plt.rcParams.update({"figure.dpi": 150, "font.size": 10,
                     "axes.grid": True, "grid.alpha": 0.25})

SIM_TAG = "SIMULATION — computed from literature models, not measured data"

def sim_footer(fig):
    fig.text(0.5, 0.01, SIM_TAG, ha="center", fontsize=8,
             style="italic", color="#8a1f1f")


# ------------------------------------------------ 1. Paschen curve
def fig_paschen():
    gaps = np.logspace(np.log10(0.05), np.log10(5.0), 200)  # mm
    p_sea, _ = standard_atmosphere(0.0)
    p_changla, _ = standard_atmosphere(5360.0)
    v_sea = [clearance_breakdown_voltage(g, p_sea) for g in gaps]
    v_cl = [clearance_breakdown_voltage(g, p_changla) for g in gaps]
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.semilogx(gaps, np.array(v_sea) / 1000, lw=2, label="Sea level (101.3 kPa)")
    ax.semilogx(gaps, np.array(v_cl) / 1000, lw=2, label="Chang La, 5360 m (51.5 kPa)")
    ax.axhline(0.327, ls="--", color="gray", lw=1)
    ax.text(0.06, 0.36, "Paschen minimum ~327 V [LITERATURE]\n"
            "(305 V with implemented constants)", fontsize=8, color="gray")
    ax.set_xlabel("Clearance gap d (mm)")
    ax.set_ylabel("Breakdown voltage Vb (kV)")
    ax.set_title("Paschen breakdown voltage vs clearance — air, uniform field")
    ax.legend(loc="lower right")
    sim_footer(fig)
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    fig.savefig(os.path.join(GRAPH_DIR, "paschen_curve.png"), bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------ 2. pressure/temperature vs altitude
def fig_atmosphere():
    h = np.linspace(0, 6000, 200)
    p = np.array([standard_atmosphere(x)[0] / 1000 for x in h])
    t = np.array([standard_atmosphere(x)[1] - 273.15 for x in h])
    fig, ax1 = plt.subplots(figsize=(7.5, 4.6))
    ax1.plot(h, p, lw=2, color="#1f4e79", label="Pressure")
    ax1.set_xlabel("Altitude (m)")
    ax1.set_ylabel("Pressure (kPa)", color="#1f4e79")
    ax1.tick_params(axis="y", labelcolor="#1f4e79")
    ax2 = ax1.twinx()
    ax2.plot(h, t, lw=2, color="#c5504b", ls="--", label="Temperature")
    ax2.set_ylabel("Temperature (°C)", color="#c5504b")
    ax2.tick_params(axis="y", labelcolor="#c5504b")
    for name, hh in [("Leh", 3500), ("Chang La", 5360)]:
        ax1.axvline(hh, color="gray", lw=1, ls=":")
        ax1.text(hh + 40, 95, name, fontsize=9, rotation=90, va="top")
    ax1.set_title("Standard-atmosphere pressure & temperature vs altitude")
    sim_footer(fig)
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    fig.savefig(os.path.join(GRAPH_DIR, "pressure_temperature_vs_altitude.png"),
                bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------ 3. thermal convection penalty
def fig_thermal():
    h = np.linspace(0, 6000, 60)
    rise = []
    for x in h:
        p, t_amb = standard_atmosphere(x)
        ts, _, _ = thermal_rise(6.0, 0.01, t_amb, p)
        rise.append(ts - t_amb)
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.plot(h, rise, lw=2, color="#c5504b")
    ax.set_xlabel("Altitude (m)")
    ax.set_ylabel("Steady-state ΔT above ambient (K)")
    ax.set_title("Thermal penalty: same 6 W dissipation, convection derated with pressure")
    ax.text(0.03, 0.95,
            "Model: h(p) = h0·(p/p0)^0.8 [ASSUMPTION]\n"
            "Board 0.01 m², h0 = 8 W/m²K, ε = 0.9",
            transform=ax.transAxes, fontsize=8, va="top",
            bbox=dict(boxstyle="round", fc="white", alpha=0.8))
    sim_footer(fig)
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    fig.savefig(os.path.join(GRAPH_DIR, "thermal_convection_penalty.png"),
                bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------ 4. battery derating
def fig_battery():
    t = np.linspace(-40, 30, 200)
    f = [battery_usable_fraction(x) for x in t]
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.plot(t, np.array(f) * 100, lw=2, color="#2e7d32")
    ax.plot([-20], [80], "o", color="#2e7d32")
    ax.annotate("~80% at −20 °C\n[LITERATURE, per-datasheet;\nchemistry-specific]",
                xy=(-20, 80), xytext=(-38, 88), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="black"))
    ax.axvspan(-40, -20, color="gray", alpha=0.12)
    ax.text(-39, 40, "estimate region\n[ASSUMPTION]", fontsize=8, color="gray")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Usable capacity (% of rated)")
    ax.set_title("Li-ion usable capacity vs temperature — 2S 18650 screening curve")
    sim_footer(fig)
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    fig.savefig(os.path.join(GRAPH_DIR, "battery_derating.png"), bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------ 5. clearance analysis
def required_gap_mm(target_v, pressure_pa):
    """Smallest gap (mm) whose Paschen Vb >= target, bisection on p*d."""
    p_torr = pressure_pa / PA_PER_TORR
    lo, hi = 0.9, 4000.0  # p*d in Torr*cm, above the Paschen minimum
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if paschen_breakdown_voltage(mid) >= target_v:
            hi = mid
        else:
            lo = mid
    return (hi / p_torr) * 10.0


def fig_clearance():
    volts = np.array([500, 1000, 2000, 3000, 5000, 8000])
    p_sea, _ = standard_atmosphere(0.0)
    p_cl, _ = standard_atmosphere(5360.0)
    g_sea = [required_gap_mm(v, p_sea) for v in volts]
    g_cl = [required_gap_mm(v, p_cl) for v in volts]
    x = np.arange(len(volts))
    w = 0.38
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.bar(x - w / 2, g_sea, w, label="Sea level", color="#1f4e79")
    ax.bar(x + w / 2, g_cl, w, label="Chang La (5360 m)", color="#c5504b")
    ax.set_xticks(x)
    ax.set_xticklabels(["%d V" % v for v in volts])
    ax.set_xlabel("Withstand voltage target")
    ax.set_ylabel("Minimum clearance (mm) from Paschen's law")
    ax.set_title("Clearance required for a withstand target — sea level vs Ladakh")
    ax.legend()
    sim_footer(fig)
    fig.tight_layout(rect=[0, 0.06, 1, 0.96])
    fig.savefig(os.path.join(GRAPH_DIR, "clearance_analysis.png"), bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------ 6. architecture diagram
def fig_architecture():
    fig, ax = plt.subplots(figsize=(12.5, 6.2))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.axis("off")

    def box(x, y, w, h, text, fc="#1f4e79", tc="white", fs=9.5):
        r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6",
                           fc=fc, ec="#0d2a45", lw=1.4)
        ax.add_patch(r)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                color=tc, fontsize=fs, weight="bold", linespacing=1.4)

    def arrow(x1, y1, x2, y2, style="-|>", lw=1.6, color="#0d2a45", ls="-"):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                     mutation_scale=14, lw=lw, color=color,
                                     linestyle=ls, shrinkA=1, shrinkB=2))

    Y = 40
    # row 1 — forward pipeline
    box(1, Y, 15, 10, "Ladakh\nEnvironment")
    box(19, Y, 15, 10, "Pressure /\nTemperature /\nHumidity", fc="#2e6e8e")
    box(37, Y, 15, 10, "Physics\nEngine", fc="#0d2a45")
    box(55, Y, 15, 10, "Risk\nEngine", fc="#7a3b1f")
    box(73, Y, 15, 10, "Mitigation\nRecommendation", fc="#2e6e8e")
    box(90.5, Y, 8, 10, "Reliability\nDecision", fc="#1f4e79", fs=8)
    for xa, xb in [(16, 19), (34, 37), (52, 55), (70, 73), (88, 90.5)]:
        arrow(xa, Y + 5, xb, Y + 5)

    # three physics models under the engine
    Y2 = 24
    box(30.5, Y2, 9.5, 9, "Thermal", fc="#4a7fb5", fs=8.5)
    box(42.5, Y2, 9.5, 9, "HV /\nInsulation", fc="#4a7fb5", fs=8.5)
    box(54.5, Y2, 9.5, 9, "Battery", fc="#4a7fb5", fs=8.5)
    for xc in [35.25, 47.25, 59.25]:
        arrow(xc, Y2 + 9, xc, Y)
    ax.text(60, Y2 - 2.6, "three literature models feed the engine",
            ha="center", fontsize=8, style="italic", color="#555")

    # row 2 — validation loop (right-to-left under the pipeline)
    Y3 = 8
    box(37, Y3, 15, 9, "Model\nCalibration", fc="#2e7d32")
    box(55, Y3, 15, 9, "Physical\nValidation", fc="#2e7d32")
    # decision -> validation: down from decision, left, then down into box top
    arrow(94.5, Y, 94.5, 20)
    arrow(94.5, 20, 62.5, 20)
    arrow(62.5, 20, 62.5, Y3 + 9)
    ax.text(82, 22, "measured results", fontsize=8, style="italic", color="#555")
    # validation -> calibration
    arrow(55, Y3 + 4.5, 52, Y3 + 4.5)
    # calibration -> physics engine, straight up through the gap between the
    # Thermal and HV/Insulation boxes (x=41.25 is clear of both)
    arrow(41.25, Y3 + 9, 41.25, Y)
    ax.text(27, 28, "model loses every tie:\nmeasurement overrules model",
            fontsize=8, style="italic", color="#2e7d32", ha="center",
            rotation=90, va="center")

    # input annotation
    ax.text(8.5, Y - 3.2, "Chang La 5360 m · 51 kPa · −20 °C [LITERATURE]",
            ha="center", fontsize=8, color="#333")
    # verdict annotation
    ax.text(62.5, Y - 3.2, "PASS / REVIEW / REDESIGN [ASSUMPTION: team thresholds]",
            ha="center", fontsize=8, color="#7a3b1f")

    ax.set_title("HIMKAVACH — physics-guided reliability screening architecture",
                 fontsize=13, weight="bold", pad=14, color="#0d2a45")
    fig.tight_layout()
    fig.savefig(os.path.join(ARCH_DIR, "himkavach-architecture.png"), bbox_inches="tight")
    fig.savefig(os.path.join(ARCH_DIR, "himkavach-architecture.svg"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_paschen(); print("paschen_curve.png")
    fig_atmosphere(); print("pressure_temperature_vs_altitude.png")
    fig_thermal(); print("thermal_convection_penalty.png")
    fig_battery(); print("battery_derating.png")
    fig_clearance(); print("clearance_analysis.png")
    fig_architecture(); print("himkavach-architecture.png/.svg")
    print("done.")
