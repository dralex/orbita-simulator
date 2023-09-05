M1 = 0.00002
DW = 0.00001
M2 = 0.00001


def torsion_completed():
    return cpu.get_flight_time() >= Start_T + t0


def is_angle_ok():
    oa = orientation.get_angle(AXIS_Z)
    return oa >= 359.8 or oa <= 0.2


def is_target_dw():
    return abs(orientation.get_angular_velocity(AXIS_Z)) < DW
