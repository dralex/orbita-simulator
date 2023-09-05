dry_mass = 1 + 0.4 + 0.3 + 0.3 + 2 + 0.4 + 0.5 + 0.6
volume = 3.4
a = math.pow(volume, 1.0 / 3.0) / 10.0
I_z = (1.0 / 12.0) * (2.0 * a ** 2) * dry_mass

GM = 6.6742e-11 * 5.9726e24
R_z = 6371032.0


def normalize_angle_difference(angle_difference):
    """ -190 = 170 (if -180< => +360)"""
    normalized_angle_difference = angle_difference
    while normalized_angle_difference < -180:
        normalized_angle_difference += 360
    while normalized_angle_difference >= 180:
        normalized_angle_difference -= 360
    return normalized_angle_difference
