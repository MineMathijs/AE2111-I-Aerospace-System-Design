import math
from ISA import Temperature, Pressure, Density
from variables import *
from MatchingDiagramPlot import *
# root chord, taper ratio
# eq. 8.1, 8.2, 8.3, 8.5, 8.6, 8.4, 8.9, 8.10, 8.11, 8.12, 8.13, example 8.4


def QC4Sweep(M_cr=0.77):
    Q4Sweep_Angle = math.acos(1.16/(M_cr + 0.5))
    return Q4Sweep_Angle


def taper_ratio_real(tip_chord, root_chord):
    TaperRatio = tip_chord/root_chord
    return TaperRatio


def taper_ratio_Mcr(Q4sweep=QC4Sweep()):
    TaperRatio = 0.2 * (2 - Q4sweep)
    return TaperRatio


def wing_span(Aspect_ratio, Surface_area):
    b_w = math.sqrt(Aspect_ratio * Surface_area)
    return b_w


def chord_root(Surface_area, taper_rato, wing_span):
    c_r = (2 * Surface_area)/((1+taper_rato) * wing_span)
    return c_r

# from .6 to .10


def chord_tip(taper, chord_root):
    return taper * chord_root


def span(aspect_ratio, wing_surface):
    return math.sqrt(aspect_ratio*wing_surface)


def form_drag_airfoil(thick_to_chord):
    # 0.06 <= thick_to_chord <= 0.25
    return 0.0035 + 0.018*(thick_to_chord)


def min_form_drag(width_fuselage, chord_root, wing_surface, avg_friction_coefficient):
    return avg_friction_coefficient*(2 - chord_root*width_fuselage/wing_surface)

# from .11


def min_CL_max(QCSweep, CL_max_cr):
    return 1.1 * (CL_max_cr / math.cos(QCSweep))


def tickness_cord_ratio(halveCordSweep, M_cr, CL_cr):
    return (math.pow(math.cos(halveCordSweep), 3) * (0.935 - ((M_cr + 0.03) * math.cos(halveCordSweep)) - (0.115 * math.pow(CL_cr, 1.5)))) / (math.pow(math.cos(halveCordSweep), 2))


# There is a mistake here idk where
def CL_cruise(pressure_cruise, velocity_cruise, wing_loading):
    return (2 / (1.4 * pressure_cruise * math.pow(velocity_cruise, 2))) * wing_loading


def Diherdral(QCSweep, configuration="low", Diherdral_default=3):  # deg > deg
    if configuration.lower() == "low":
        return Diherdral_default - 0.1 * QCSweep + 2
    elif configuration.lower() == "mid":
        return Diherdral_default - 0.1 * QCSweep
    elif configuration.lower() == "high":
        return Diherdral_default - 0.1 * QCSweep - 2
    else:
        raise ValueError("Configuration not found")


def QCSweep_to_HalveCordSweep(QCSweep, taper_ratio, wing_span, root_chord):
    return math.atan(math.tan(QCSweep) - (1/3) * ((2 * root_chord) / wing_span) * (1 - taper_ratio))


def QCSweep_to_LESweep(QCSweep, taper_ratio, wing_span, root_chord):
    return math.atan(math.tan(QCSweep) + (1/4) * ((2 * root_chord) / wing_span) * (1 - taper_ratio))


def mean_aerodynamic_chord(root_chord, taper_ratio):
    return (2/3) * root_chord * (1 + taper_ratio + math.pow(taper_ratio, 2)) / (1 + taper_ratio)


def MAC_spanwise(wing_span, taper_ratio,):
    return (wing_span / 6) * ((1 + 2*taper_ratio) / (1 + taper_ratio))


def MAC_X_LE(yMAC, LE_sweep):
    return yMAC * math.tan(LE_sweep)

######################


QCSweep = QC4Sweep()
taper_ratio = taper_ratio_Mcr()
b = wing_span(AR, wing_surface)
c_r = chord_root(wing_surface, taper_ratio, b)

c_t = chord_tip(taper_ratio, c_r)
dihedral = Diherdral(math.degrees(QCSweep))
halveCordSweep = QCSweep_to_HalveCordSweep(QCSweep, taper_ratio, b, c_r)
LESweep = QCSweep_to_LESweep(QCSweep, taper_ratio, b, c_r)
CL_max_min = min_CL_max(QCSweep, C_lmax_cruise)
C_L_cruise = CL_cruise(Pressure(cruise_h), V_cr, minimum_speed[2])
ticknessToCordRatio = tickness_cord_ratio(
    halveCordSweep, V_cr, C_L_cruise)  # C_l_cruise =/= C_lmax_cruise
MAC = mean_aerodynamic_chord(c_r, taper_ratio)
y_MAC = MAC_spanwise(b, taper_ratio)
XLEMAC = MAC_X_LE(y_MAC, LESweep)

if __name__ == "__main__":
    # print(minimum_speed[2])
    # print(c_r, c_t, b/2, taper_ratio, dihedral)
    # print(math.tan(QCSweep))
    print(f"Wing surface area: {wing_surface} m^2")
    print(f"QCSweep: {math.degrees(QCSweep)} deg")
    print(f"Halve Cord Sweep: {math.degrees(halveCordSweep)} deg")
    print(f"Leading Edge Sweep: {math.degrees(LESweep)} deg")
    print(f"Taper Ratio: {taper_ratio}")
    print(f"Root Chord: {c_r} m")
    print(f"Tip Chord: {c_t} m")
    print(f"Wing Span: {b} m")
    print(f"Diherdral: {dihedral} deg")
    print(f"Minimum airfoil Cl_Max: {CL_max_min}")
    print(f"CL Cruise: {C_L_cruise}")
    print(f"Tickness to Chord Ratio: {ticknessToCordRatio}")
    print(f"Mean Aerodynamic Chord: {MAC} m")
    print(f"MAC Spanwise: {y_MAC} m")
    print(f"XLEMAC: {XLEMAC} m")
    print(f"Density: {Density(cruise_h)}")
