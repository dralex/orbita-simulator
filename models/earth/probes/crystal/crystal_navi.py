# globals
Target_h = 0
DV2 = 0
Start_V = 0
DV = 0
h = 0.0
# globals


def setup_maneuver(h_tar):
    global Target_h
    Target_h = float(h_tar)


def update_maneuver():
    global Start_V, DV
    Start_V = navigation.get_transversal_velocity()
    DV = DV2


def impulse_completed():
    return abs(navigation.get_transversal_velocity() - Start_V) >= DV


def engine_can_be_switched_on():
    global h
    prev_h = h
    h = navigation.get_orbit_height()
    return h <= prev_h


def ready_to_fall():
    na = navigation.get_z_axis_angle()
    return abs(na - normalize_angle(target_angle - 150)) < 0.1
