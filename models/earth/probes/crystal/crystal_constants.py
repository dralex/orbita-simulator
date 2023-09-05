dry_mass = 8.6
volume = 6.8
side = math.pow(volume, 1.0 / 3.0) / 10.0

GM = 6.6742e-11 * 5.9726e24
R_z = 6371032.0

target_orbit = 700.0 * 1000.0
target_angle = 120.0

T = 2 * math.pi * (R_z + target_orbit) / math.sqrt(GM / (R_z + target_orbit))
Traction = 0.009


def probe_mass():
    return dry_mass + engine.get_fuel()


def probe_inertia():
    return side ** 2 * probe_mass() / 6.0


def normalize_angle(angle):
    """ -60 = 300 (if 0< => +360)"""
    while angle >= 360.0:
        angle -= 360.0
    while angle < 0.0:
        angle += 360.0
    return angle
