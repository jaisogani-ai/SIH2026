"""
HIMKAVACH shared physics library — SIH26049 / DRDO.

Implements the literature models behind the HIMKAVACH simulator as
plain, reviewable Python. Every function states its source and its
limits in the docstring.

STATUS: SIMULATION ONLY. Nothing here is measured experimental data.
Numbers produced by this module are [COMPUTED] from published models,
not measurements from built hardware (no prototype has been built yet).

Model inventory
---------------
1. standard_atmosphere(h_m) ......... pressure/temperature vs altitude
   Source: U.S. Standard Atmosphere 1976, troposphere branch (h < 11 km).
2. paschen_breakdown_voltage(pd) ..... Vb for air gaps from Paschen's law
   Source: Paschen's law; air constants A=15 cm^-1 Torr^-1,
   B=365 V/(cm Torr), secondary emission coefficient gamma=0.01.
   With THESE constants the computed minimum is 305.3 V at
   pd = 0.8375 Torr-cm [COMPUTED]. Textbooks commonly quote ~327 V;
   the exact minimum depends on the (A, B, gamma) set chosen.
3. thermal_rise(...) .................. lumped steady-state board temperature
   Physics: convection + radiation balance. Convection coefficient is
   derated with pressure as h(p) = h0 * (p/p0)^0.8  [ASSUMPTION —
   empirical natural-convection scaling; not validated for this geometry].
4. battery_usable_capacity(...) ...... Li-ion usable capacity vs temperature
   Anchored to a per-datasheet literature point: ~80% usable at -20 C
   [LITERATURE, chemistry-specific, not universal]. Below that the curve
   is an engineering estimate [ASSUMPTION].
5. risk_index(...) .................... composite PASS / REVIEW / REDESIGN
   [ASSUMPTION] decision thresholds chosen by the team; not a standard.

Units: SI everywhere (m, Pa, K, W, V, m^2) unless a function says otherwise.
"""

import math

# ---------------------------------------------------------------- constants
P0_SEA_LEVEL_PA = 101325.0        # sea-level standard pressure [LITERATURE]
T0_SEA_LEVEL_K = 288.15          # sea-level standard temperature [LITERATURE]
LAPSE_RATE_K_PER_M = 0.0065      # tropospheric lapse rate [LITERATURE]
G = 9.80665                      # m/s^2
M_AIR = 0.0289644                # kg/mol
R_UNIVERSAL = 8.31447            # J/(mol K)
STEFAN_BOLTZMANN = 5.670374419e-8  # W/(m^2 K^4)

# Paschen constants for AIR (parallel-plate, uniform field)
PASCHEN_A = 15.0                 # cm^-1 Torr^-1  [LITERATURE]
PASCHEN_B = 365.0                # V/(cm Torr)    [LITERATURE]
PASCHEN_GAMMA = 0.01             # secondary emission coefficient [LITERATURE, typical]

PA_PER_TORR = 133.3223684211

# Reference Ladakh sites (altitude [LITERATURE]; pressure from the model below)
SITE_CHANG_LA_M = 5360.0         # Chang La pass altitude [LITERATURE]
SITE_LEH_M = 3500.0              # Leh town altitude (approx) [LITERATURE]


# ------------------------------------------------- 1. standard atmosphere
def standard_atmosphere(altitude_m):
    """Pressure and temperature at altitude (troposphere, h < 11000 m).

    Source: U.S. Standard Atmosphere 1976 barometric formula.
    Assumption: dry air, standard lapse rate; real weather deviates.
    Returns (pressure_pa, temperature_k).
    """
    h = float(altitude_m)
    if h < 0 or h > 11000:
        raise ValueError("model valid for 0 <= h <= 11000 m only")
    t = T0_SEA_LEVEL_K - LAPSE_RATE_K_PER_M * h
    exponent = G * M_AIR / (R_UNIVERSAL * LAPSE_RATE_K_PER_M)
    p = P0_SEA_LEVEL_PA * (t / T0_SEA_LEVEL_K) ** exponent
    return p, t


# ------------------------------------------------- 2. Paschen breakdown
def paschen_breakdown_voltage(pd_torr_cm):
    """Breakdown voltage of an air gap from Paschen's law.

    Vb = B * p*d / (ln(A*p*d) - ln(ln(1 + 1/gamma)))

    Purpose:   estimate how much insulation strength a clearance loses
               at low pressure (Ladakh) vs sea level.
    Input:     p*d in Torr*cm (pressure x gap).
    Output:    breakdown voltage in volts.
    Assumptions: uniform field, parallel plates, clean dry air,
               gamma = 0.01. Real PCB geometries (sharp traces,
               contamination, humidity) deviate — this is a screening
               bound, not a qualification value.
    Limitations: invalid very close to the Paschen minimum and for
               p*d far outside ~[0.5, 5000] Torr*cm.
    Source: Paschen's law; constants for air as above.
    """
    pd = float(pd_torr_cm)
    a, b, g = PASCHEN_A, PASCHEN_B, PASCHEN_GAMMA
    denom = math.log(a * pd) - math.log(math.log(1.0 + 1.0 / g))
    if denom <= 0:
        raise ValueError("p*d too close to the Paschen minimum; model singular")
    return b * pd / denom


def paschen_minimum():
    """Numerically locate the Paschen minimum for air. Returns (pd, Vb)."""
    best = None
    pd = 0.05
    while pd < 50.0:
        try:
            v = paschen_breakdown_voltage(pd)
        except ValueError:
            pd *= 1.01
            continue
        if best is None or v < best[1]:
            best = (pd, v)
        pd *= 1.005
    return best  # ~ (0.8375 Torr*cm, 305.3 V) for the A=15, B=365, gamma=0.01 constant set [COMPUTED]


def clearance_breakdown_voltage(gap_mm, pressure_pa):
    """Vb for a gap (mm) at a given pressure (Pa). Convenience wrapper."""
    gap_cm = gap_mm / 10.0
    pressure_torr = pressure_pa / PA_PER_TORR
    return paschen_breakdown_voltage(pressure_torr * gap_cm)


# ------------------------------------------------- 3. thermal model
def thermal_rise(power_w, area_m2, ambient_k, pressure_pa,
                h0_w_per_m2k=8.0, emissivity=0.9):
    """Steady-state surface temperature rise of a dissipating board.

    Energy balance:  P = h(p)*A*dT + eps*sigma*A*((Ta+dT)^4 - Ta^4)

    Purpose:   show how reduced convection at altitude raises
               component temperatures for the same dissipation.
    Inputs:    power_w      — total dissipated power [W]
               area_m2      — effective cooled area [m^2]
               ambient_k    — ambient temperature [K]
               pressure_pa  — ambient pressure [Pa]
               h0           — sea-level natural-convection coefficient [ASSUMPTION]
               emissivity   — surface emissivity [ASSUMPTION]
    Output:    (surface_temp_k, convection_w, radiation_w)
    Assumptions: lumped isothermal surface; h(p) = h0*(p/p0)^0.8 is an
               empirical natural-convection scaling, NOT measured for
               this geometry; still air; no conduction path modelled.
    Limitations: screening only — real boards need per-component
               analysis (Theta-JA, airflow, heatsinks).
    """
    p_ratio = pressure_pa / P0_SEA_LEVEL_PA
    h = h0_w_per_m2k * (p_ratio ** 0.8)          # [ASSUMPTION]
    # Newton iteration on dT
    dt = power_w / (h * area_m2 + 1e-9)          # convection-only seed
    for _ in range(100):
        ts = ambient_k + dt
        f = (h * area_m2 * dt
             + emissivity * STEFAN_BOLTZMANN * area_m2 * (ts ** 4 - ambient_k ** 4)
             - power_w)
        df = (h * area_m2
              + 4.0 * emissivity * STEFAN_BOLTZMANN * area_m2 * ts ** 3)
        step = f / df
        dt -= step
        if abs(step) < 1e-9:
            break
    ts = ambient_k + dt
    conv = h * area_m2 * dt
    rad = power_w - conv
    return ts, conv, rad


# ------------------------------------------------- 4. battery model
def battery_usable_fraction(temp_c):
    """Usable fraction of rated Li-ion capacity at temperature.

    Purpose:   estimate cold-weather energy loss for a 18650-based pack.
    Model:     1.00 for T >= 0 C; linear decline to 0.80 at -20 C.
               The -20 C anchor is an engineering estimate [ASSUMPTION]:
               no specific 18650 datasheet is on file (cell TBD before
               purchase). Below -20 C the curve is a steeper estimate.
    Assumptions: constant-current discharge; no self-heating credit;
               pack = 2S 18650 generic cells.
    Limitations: real derating is chemistry-, rate- and age-dependent;
               this curve is an engineering estimate below -20 C
               [ASSUMPTION], not a measured discharge curve.
    """
    t = float(temp_c)
    if t >= 0:
        return 1.0
    if t >= -20:
        return 1.0 - (0.20 * (0.0 - t) / 20.0)
    # below -20 C: steeper estimate, floored at 0.25
    return max(0.25, 0.80 - 0.030 * (-20.0 - t))


def battery_internal_resistance_factor(temp_c):
    """DCIR multiplier vs 25 C reference (simple exponential fit).

    R(T) = R25 * exp(0.045 * (25 - T)) for T < 25 C  [ASSUMPTION].
    Purpose: estimate extra voltage sag under load in the cold.
    """
    t = float(temp_c)
    if t >= 25:
        return 1.0
    return math.exp(0.045 * (25.0 - t))


# ------------------------------------------------- 5. risk engine
def risk_index(thermal_margin_c, insulation_margin_ratio, battery_margin_ratio,
               weights=(0.35, 0.35, 0.30)):
    """Composite reliability risk index -> PASS / REVIEW / REDESIGN.

    Purpose:   single screening verdict from the three mechanism margins.
    Inputs:    thermal_margin_c        — (T_limit - T_predicted) in C
               insulation_margin_ratio — Vbd_predicted / V_applied
               battery_margin_ratio    — usable_energy / required_energy
               weights                 — (thermal, insulation, battery)
    Scoring:   each margin is normalised to a 0..1 sub-score with a
               soft knee; the index is the weighted sum.
               verdict: >= 0.75 PASS, >= 0.50 REVIEW, else REDESIGN.
    Assumptions: thresholds are TEAM CHOSEN [ASSUMPTION], not a standard;
               equal-ish weighting is a starting point for discussion.
    Limitations: screening aid only — never a qualification verdict.
    Returns (index_0_to_1, verdict_str).
    """
    def _sat(x, knee):
        x = max(0.0, x)
        return x / (x + knee)

    s_thermal = _sat(thermal_margin_c, 20.0)          # 20 C margin -> ~0.5
    s_insul = _sat(insulation_margin_ratio - 1.0, 1.0)  # 2x Vbd -> ~0.5
    s_batt = _sat(battery_margin_ratio - 1.0, 0.5)      # 1.5x energy -> ~0.5
    wt, wi, wb = weights
    index = (wt * s_thermal + wi * s_insul + wb * s_batt) / (wt + wi + wb)
    if index >= 0.75:
        verdict = "PASS"
    elif index >= 0.50:
        verdict = "REVIEW"
    else:
        verdict = "REDESIGN"
    return index, verdict


if __name__ == "__main__":
    # ---- reproducible smoke example -------------------------------------
    p_changla, t_changla = standard_atmosphere(SITE_CHANG_LA_M)
    print("Chang La (5360 m): p = %.1f kPa, T = %.1f C"
          % (p_changla / 1000.0, t_changla - 273.15))
    pd_min, v_min = paschen_minimum()
    print("Paschen minimum (air): pd = %.3f Torr-cm, Vb = %.0f V" % (pd_min, v_min))
    p_sea, _ = standard_atmosphere(0.0)
    v_sea = clearance_breakdown_voltage(0.8, p_sea)
    v_ladakh = clearance_breakdown_voltage(0.8, p_changla)
    print("Vbd(0.8 mm): sea level = %.0f V, Chang La = %.0f V [COMPUTED]"
          % (v_sea, v_ladakh))
