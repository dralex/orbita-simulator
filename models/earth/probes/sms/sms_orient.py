M = 0.000001
DW = 0.00001


def calculate_nadir_rotation():
    h = navigation.get_orbit_height()
    w0 = orientation.get_angular_velocity(AXIS_Z)

    w = -360.0 * math.sqrt(GM / (R_z + h)) / (2 * math.pi * (R_z + h))
    t = 2 * 270.0 / (w0 - w)
    m0 = (w - w0) * I_z / t

    return w, t, m0


def is_target_dw():
    return abs(orientation.get_angular_velocity(AXIS_Z) - W) < DW
