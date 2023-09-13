# globals
transfer_burn_angle = 0
transfer_end_fuel = 0
transfer_burn_time = 0
transfer_center_angle = 0
is_first_impulse = True
# globals

max_engine_traction = 0.037
engine_specific_impulse = 2705.0


def calc_fuel():
    global transfer_burn_angle, transfer_end_fuel, transfer_burn_time
    if is_first_impulse:
        velocity_fuel = initial_nav_angular_velocity
    else:
        velocity_fuel = target_angular_velocity - (transfer_delta_v / (target_height + R_z))
    engine.set_state(STATE_ON)
    transfer_start_fuel = engine.get_fuel()
    engine.set_state(STATE_OFF)
    transfer_end_fuel = ((dry_mass + transfer_start_fuel) / math.exp(
        transfer_delta_v / engine_specific_impulse)) - dry_mass
    if transfer_end_fuel < 0.0:
        transfer_end_fuel = 0.0
    transfer_burn_time = (transfer_start_fuel - transfer_end_fuel) / (max_engine_traction / 2)
    transfer_burn_angle = transfer_burn_time * velocity_fuel


def is_angle_ok():
    if is_first_impulse:
        return is_angle_ok_first_impulse()
    else:
        return is_angle_ok_second_impulse()


def is_angle_ok_first_impulse():
    target_angle = normalize_angle(initial_target_angle + cpu.get_flight_time() * target_angular_velocity)
    angle_alignment = normalize_angle_difference(target_angle - navigation.get_z_axis_angle())
    return abs(normalize_angle_difference(
        angle_alignment - transfer_angle_alignment - (transfer_burn_time / 2) * (
                initial_nav_angular_velocity - target_angular_velocity))) < navig_angle_precision


def is_angle_ok_second_impulse():
    return abs(normalize_angle_difference(navigation.get_z_axis_angle() - normalize_angle(
        transfer_center_angle + 180.0 - transfer_burn_angle / 2))) < navig_angle_precision


def starting_engine():
    global transfer_center_angle
    nav_angle = navigation.get_z_axis_angle()
    transfer_center_angle = nav_angle + transfer_burn_angle / 2
    engine.set_state(STATE_ON)
    engine.set_traction(max_engine_traction / 2)
    engine.start_engine()


def set_is_first_impulse(impulse: bool):
    global is_first_impulse
    is_first_impulse = (impulse == 'True')
