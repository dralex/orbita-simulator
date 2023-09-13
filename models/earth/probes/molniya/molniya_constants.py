dry_mass = 40.0 + 25.0 + 6.6 + 0.6 + 0.4 + 3.0 + 32.0 + 1.5 + 7.5

GM = 6.6742e-11 * 5.9726e24
R_z = 6371032.0

initial_height = 550000.0
target_height = 40000000.0

earth_rotation_period = 86164.1
ground_station_angle = 0.0

initial_nav_angular_velocity = math.degrees(math.sqrt(GM / ((initial_height + R_z) ** 3)))


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
