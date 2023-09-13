dry_mass = 1.7 + 10.0 + 6.6 + 0.6 + 0.2 + 0.4 + 3.0 + 16.0 + 1.5 + 1.5

GM = 6.6742e-11 * 5.9726e24
R_z = 6371032.0

initial_inspector_height = 182000.0
target_height = 790000.0
initial_target_angle = 61.0

initial_angular_velocity = orientation.get_angular_velocity(AXIS_Z)
target_angular_velocity = math.degrees(math.sqrt(GM / ((target_height + R_z) ** 3)))
initial_nav_angular_velocity = math.degrees(math.sqrt(GM / ((initial_inspector_height + R_z) ** 3)))
load_enable_interval = 1.5
ground_station_angle = 121.0
navig_angle_precision = 5e-3
radio_enable_interval = 200

def normalize_angle(angle):
    """ -60 = 300 (if 0< => +360)"""
    normalized_angle = angle
    while normalized_angle < 0:
        normalized_angle += 360
    while normalized_angle >= 360:
        normalized_angle -= 360
    return normalized_angle


def normalize_angle_difference(angle_difference):
    """ -190 = 170 (if -180< => +360)"""
    normalized_angle_difference = angle_difference
    while normalized_angle_difference < -180:
        normalized_angle_difference += 360
    while normalized_angle_difference >= 180:
        normalized_angle_difference -= 360
    return normalized_angle_difference


transfer_angle_alignment = normalize_angle_difference(180 * (1 - math.sqrt(
    (1 + (initial_inspector_height + R_z) / (target_height + R_z)) ** 3) / math.sqrt(8)))

transfer_delta_v = abs(math.sqrt(GM / (initial_inspector_height + R_z)) * (math.sqrt(
    2 * (target_height + R_z) / (
            (target_height + R_z) + (initial_inspector_height + R_z))) - 1))
