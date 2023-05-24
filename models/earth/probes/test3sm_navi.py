Target_h = 0
Traction = 0.009
DV1 = DV2 = Start_V = Target_A = 0
DA = 0.01

def setup_maneuvre(h):
    global Target_h
    Target_h = float(h)

def calculate_maneuvre():
    global Start_V, DV1, DV2, DV, Start_A
    Target_A = navigation.get_z_axis_angle() + 180.0
    if Target_A >= 360.0: Target_A = Target_A - 360.0
    r1 = R_z + navigation.get_orbit_height()
    r2 = R_z + Target_h
    DV1 = math.sqrt(GM / r1) * (math.sqrt(2 * r2 / (r1 + r2)) - 1)
    DV2 = math.sqrt(GM / r2) * (1 - math.sqrt(2 * r1 / (r1 + r2)))
    Start_V = navigation.get_transversal_velocity()
    DV = DV1

def update_maneuvre():
    global Start_V
    Start_V = navigation.get_transversal_velocity()
    DV = DV2

def impulse_completed():
    return abs(navigation.get_transversal_velocity() - Start_V) >= DV1

def has_opposite_position():
    return abs(navigation.get_z_axis_angle() - Target_A) < DA
