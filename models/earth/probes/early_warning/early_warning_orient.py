# globals
active = False
decreasing = False
inertia_moment = 0
max_angular_acceleration = 0
stabilization_begin_time = None
prev_flight_time = None
# globals

max_orientation_torsion = 0.25
angular_velocity_precision = 2e-3
orient_angle_precision = 5e-3

scanning_period = 140.0
angle_offset = 6.0


def is_orientation_needed():
    return (abs(orientation.get_angular_velocity(AXIS_Z) - desired_a_v) > angular_velocity_precision) or (
            abs(normalize_angle_difference(desired_a - orientation.get_angle(AXIS_Z))) > orient_angle_precision)


def start_reduction():
    global decreasing
    angular_velocity = orientation.get_angular_velocity(AXIS_Z)
    if abs(angular_velocity) > angular_velocity_precision:
        if not decreasing:
            decreasing = True
            if angular_velocity > 0:
                torsion = -max_orientation_torsion
            else:
                torsion = max_orientation_torsion
            orientation.start_motor(AXIS_Z)
            orientation.set_motor_moment(AXIS_Z, torsion)

    elif decreasing:
        decreasing = False
        orientation.stop_motor(AXIS_Z)


def calc_observing_data():
    global prev_flight_time, prev_nav_angle, desired_a, desired_a_v
    flight_time = cpu.get_flight_time()
    nav_angle = navigation.get_z_axis_angle()
    if prev_flight_time is not None:
        tick = flight_time - prev_flight_time
        desired_a_v = -1.0 * normalize_angle_difference(nav_angle - prev_nav_angle) / tick
    else:
        desired_a_v = 0.0
    prev_flight_time = flight_time
    prev_nav_angle = nav_angle
    desired_a = normalize_angle((270 - nav_angle) - angle_offset)


def calculate_torsion_orientation():
    # global torsion
    angle = orientation.get_angle(AXIS_Z)
    angular_velocity = orientation.get_angular_velocity(AXIS_Z)
    desired_angle_change = normalize_angle_difference(desired_a - angle)
    proportional_coefficient = 8 * max_angular_acceleration / 180
    differential_coefficient = 8 * math.sqrt(max_angular_acceleration / 360)
    angular_acceleration = desired_angle_change * proportional_coefficient
    angular_acceleration -= (angular_velocity - desired_a_v) * differential_coefficient
    torsion = inertia_moment * angular_acceleration
    return torsion


def calculate_torsion_scanning():
    angle = orientation.get_angle(AXIS_Z)
    nav_angle = navigation.get_z_axis_angle()
    angular_acceleration = (2 * math.pi / scanning_period) ** 2 * normalize_angle_difference((270 - nav_angle) - angle)
    torsion = inertia_moment * angular_acceleration
    return torsion


def set_torsion(torsion: float):
    global active
    if torsion > max_orientation_torsion:
        torsion = max_orientation_torsion
    if torsion < -max_orientation_torsion:
        torsion = -max_orientation_torsion

    orientation.set_motor_moment(AXIS_Z, torsion)
    if not active:
        active = True
        orientation.start_motor(AXIS_Z)


def calculate_reduction():
    global stabilization_begin_time, initial_angular_velocity
    stabilization_begin_time = cpu.get_flight_time()
    initial_angular_velocity = orientation.get_angular_velocity(AXIS_Z)


def calculate_acc_inertia():
    global max_angular_acceleration, inertia_moment
    max_angular_acceleration = abs(initial_angular_velocity) / (cpu.get_flight_time() - stabilization_begin_time)
    inertia_moment = max_orientation_torsion / max_angular_acceleration
