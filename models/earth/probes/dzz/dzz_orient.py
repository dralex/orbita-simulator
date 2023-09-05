M = 0.000001
DW = 0.00001
DA = 0.01
Start_T = 0
I_z = 0

t = 508.401589219
w = -0.0621524626414
m0 = -9.7483082844e-05

def calculate_nadir_rotation():
    return w, t, m0

def is_target_dw():
    return abs(orientation.get_angular_velocity(AXIS_Z) - W) < DW
