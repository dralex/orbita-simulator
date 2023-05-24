Max_M = 0.000023
M = 0.000001
DW = 0.00001
DA = 0.1
Target_alpha = Target_phi = Target_diff = 0
Wz = 0
Iz = 0
M0 = 0
Start_T = T = 0

def n_angle(angle):
    norm_angle = angle
    while norm_angle < 0.0:
        norm_angle += 360.0
    while norm_angle >= 360.0:
        norm_angle -= 360.0
    return norm_angle

def n_angle_diff(ad):
    while ad < -180:
        ad += 360.0
    while ad >= 180:
        ad -= 360.0
    return ad

def update_turn_parameters(target_alpha, target_delta):
    global Wz, Target_alpha, Target_phi, Target_diff, Iz
    h = navigation.get_orbit_height()
    Wz = 180.0 * math.sqrt(GM / (R_z + h)) / (math.pi * (R_z + h))
    Target_alpha = float(target_alpha)
    Target_diff = float(target_delta)
    Target_phi = n_angle(Target_diff - Target_alpha)
    Iz = probe_inertia()
    debug('target diff {}'.format(Target_diff))

def reduce_speed():
    global T, Start_T
    w0 = orientation.get_angular_velocity(AXIS_Z)
    if abs(w0) < DW:
        T = 0
        m = 0
    else:
        if w0 > 0:
            m = -Max_M
        else:
            m = Max_M
        T = w0 * Iz / Max_M
    Start_T = cpu.get_flight_time()
    debug('rotation t {} m {} w0 {}'.format(T, m, w0))
    orientation.set_motor_moment(AXIS_Z, m)

def calculate_turn():
    global T, Start_T
    phi0 = orientation.get_angle(AXIS_Z)
    dPhi = n_angle(Target_phi - phi0)
    T = math.sqrt(dPhi * Iz / Max_M)
    debug('up target {} phi0 {} delta phi {} t {}'.format(Target_phi, phi0, dPhi, T))
    Start_T = cpu.get_flight_time()
    orientation.set_motor_moment(AXIS_Z, Max_M)

def complete_turn():
    global Start_T
    Start_T = cpu.get_flight_time()
    orientation.set_motor_moment(AXIS_Z, -Max_M)
    debug('up t {}'.format(T))

def completed():
    return cpu.get_flight_time() >= Start_T + T

def is_target_dw():
    return abs(orientation.get_angular_velocity(AXIS_Z)) < DW

def orientation_completed():
    alpha0 = navigation.get_z_axis_angle()
    phi0 = orientation.get_angle(AXIS_Z)
    return abs(n_angle_diff(Target_diff - alpha0 - phi0)) <= DA 
