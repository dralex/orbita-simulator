# globals
transfer_burn_angle = 0
transfer_end_fuel = 0
# globals


max_engine_traction = 0.165
engine_specific_impulse = 3041.0


def calc_fuel():
    global transfer_burn_angle, transfer_end_fuel
    engine.set_state(STATE_ON)
    transfer_start_fuel = engine.get_fuel()
    engine.set_state(STATE_OFF)
    transfer_delta_v = abs(math.sqrt(GM / (initial_height + R_z)) * (math.sqrt(
        2 * (target_height + R_z) / ((target_height + R_z) + (initial_height + R_z))) - 1))
    transfer_end_fuel = ((dry_mass + transfer_start_fuel) / math.exp(
        transfer_delta_v / engine_specific_impulse)) - dry_mass
    if transfer_end_fuel < 0.0:
        transfer_end_fuel = 0.0
    transfer_burn_time = (transfer_start_fuel - transfer_end_fuel) / max_engine_traction
    transfer_burn_angle = transfer_burn_time * initial_nav_angular_velocity
    transfer_delta_v = transfer_delta_v * math.sqrt(
        math.radians(transfer_burn_angle) / (2 * math.sin(math.radians(transfer_burn_angle / 2))))
    transfer_end_fuel = ((dry_mass + transfer_start_fuel) / math.exp(
        transfer_delta_v / engine_specific_impulse)) - dry_mass
    if transfer_end_fuel < 0.0:
        transfer_end_fuel = 0.0
    transfer_burn_time = (transfer_start_fuel - transfer_end_fuel) / max_engine_traction
    transfer_burn_angle = transfer_burn_time * initial_nav_angular_velocity


def is_angle_ok():
    nav_angle = navigation.get_z_axis_angle()
    start_angle = ground_station_angle + 180.0
    start_angle += 90.0
    start_angle += 360.0 * cpu.get_flight_time() / earth_rotation_period
    start_angle = normalize_angle(start_angle)
    return abs(normalize_angle_difference(nav_angle - start_angle)) < transfer_burn_angle / 2
