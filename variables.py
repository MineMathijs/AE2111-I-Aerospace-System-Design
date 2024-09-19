import numpy as np
import math

cruise_h = 10668  # m
landing_field_distance = 1210  # m
takeoff_field_length = 1296  # m
V_cr = .77  # Cruise speed
rhostd = 1.225
climb_rate_requirement = 6.8
# minimum stall speed
obstacle_height = 11
MTOW = 37968
C_lmax_landing = 2.5  # 1.8 < Cl < 2.8
approach_speed = 68  # m/s
landing_mass_fraction = 0.886  # 0.88 final value
cruise_mass_fraction = 0.95
climb_mass_fraction = 0.95
# stall/takeoff/cclimb/

C_lmax_takeoff = 1.8  # 1.6 < Cl < 2.2
C_lmax_cruise = 1.4  # 1.2 < Cl <1.8

# -- Drag Polar sheet --
AR = 8.69
S_wet_S_wing = 6.5

c_f = 0.00275

C_D0 = c_f * S_wet_S_wing  # zero-lift drag coeffficient

psi = 0.0075
phi = 0.97

e = 1/(math.pi * AR * psi + 1/phi)  # assumed oswald efficiency factor
B = 5  # Bypass ratio

max_flap = 35
takeoff_flap = 15
flap_angles = np.array([0, 0, 15, 15, 35, 35])
landing_gear_drag = 0.018  # 0.01 < landing_gear_drag < 0.025

# 0:cruise retracted, 1:cruise extended, 2:TO retracted, 3:TO extended, 4:landing retracted, 5:landing extended
CD_0_phases = np.array([C_D0 + 0.0013 * flap_angles[0], C_D0 + 0.0013 * flap_angles[1] + landing_gear_drag, C_D0 + 0.0013 * flap_angles[2],
                        C_D0 + 0.0013 * flap_angles[3] + landing_gear_drag, C_D0 + 0.0013 * flap_angles[4], C_D0 + 0.0013 * flap_angles[5] + landing_gear_drag])

oswald_phases = np.array([e + degree*0.0026 for degree in flap_angles])

# Climb gradient mass fraction requirements
mass_fraction_119 = 1
mass_fraction_121a = 1
mass_fraction_121b = 1
mass_fraction_121c = 1
mass_fraction_121d = landing_mass_fraction

climb_gradient_119 = 0.032
climb_gradient_121a = 0.0
climb_gradient_121b = 0.024
climb_gradient_121c = 0.012
climb_gradient_121d = 0.021
