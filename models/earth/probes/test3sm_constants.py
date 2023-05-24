GM = 6.6742e-11 * 5.9726e24
R_z = 6371032.0

Probe_dry_mass = 6.4
Probe_volume = 6.8
Probe_side = math.pow(Probe_volume, 1.0 / 3.0) / 10.0

def probe_mass():
    return Probe_dry_mass + engine.get_fuel()

def probe_inertia():
    return Probe_side ** 2 * probe_mass() / 6.0
