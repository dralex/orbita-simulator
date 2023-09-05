# globals
active = False
decreasing = False
tangented = False
idled = False
observed = False
max_angular_acceleration = 0
sample_time = 0
inertia_moment = 0
target_direction = 0
stabilization_begin_time = 0
# globals

max_orientation_torsion = 0.0165
angular_velocity_precision = 2e-3
orient_angle_precision = 5e-3

# radio_enable_angle = ground_station_angle - 5
# enable_gs = False
# enable_gs_radio_flight = None


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


def calc_tangent_data():
    global desired_a, desired_a_v
    desired_a = normalize_angle(360 - navigation.get_z_axis_angle())
    desired_a_v = -initial_nav_angular_velocity


def calc_observing_data():
    global target_direction, sample_time, desired_a, desired_a_v
    flight_time = cpu.get_flight_time()
    target_angle = normalize_angle(initial_target_angle + flight_time * target_angular_velocity)
    target_x = (target_height + R_z) * math.sin(math.radians(target_angle))
    target_y = (target_height + R_z) * math.cos(math.radians(target_angle))
    our_x = navigation.get_x_coord()
    our_y = navigation.get_y_coord()
    prev_target_direction = target_direction
    prev_sample_time = sample_time
    target_direction = math.degrees(math.atan2(target_y - our_y, target_x - our_x))
    sample_time = flight_time
    if sample_time > prev_sample_time:
        target_direction_angular_velocity = (target_direction - prev_target_direction) / (
                sample_time - prev_sample_time)
    desired_a = target_direction
    desired_a_v = target_direction_angular_velocity


def calculate_torsion():
    global active
    angle = orientation.get_angle(AXIS_Z)
    angular_velocity = orientation.get_angular_velocity(AXIS_Z)
    desired_angle_change = normalize_angle_difference(desired_a - angle)
    proportional_coefficient = 8 * max_angular_acceleration / 180
    differential_coefficient = 8 * math.sqrt(max_angular_acceleration / 360)
    angular_acceleration = desired_angle_change * proportional_coefficient
    angular_acceleration -= (angular_velocity - desired_a_v) * differential_coefficient
    torsion = inertia_moment * angular_acceleration
    if torsion > max_orientation_torsion:
        torsion = max_orientation_torsion
    if torsion < -max_orientation_torsion:
        torsion = -max_orientation_torsion

    orientation.set_motor_moment(AXIS_Z, torsion)
    if not active:
        active = True
        orientation.start_motor(AXIS_Z)


def calculate_reduction():
    global stabilization_begin_time
    stabilization_begin_time = cpu.get_flight_time()


def calculate_acc_inertia():
    global max_angular_acceleration, inertia_moment
    max_angular_acceleration = abs(initial_angular_velocity) / (cpu.get_flight_time() - stabilization_begin_time)
    inertia_moment = max_orientation_torsion / max_angular_acceleration

# def can_be_terminated():
#     global enable_gs, enable_gs_radio_flight
#     if abs(normalize_angle_difference(radio_enable_angle - navigation.get_z_axis_angle())) < navig_angle_precision and not enable_gs:
#         enable_gs = True
#         enable_gs_radio_flight = cpu.get_flight_time()
#     return enable_gs_radio_flight and (cpu.get_flight_time() - enable_gs_radio_flight) >= radio_enable_interval
