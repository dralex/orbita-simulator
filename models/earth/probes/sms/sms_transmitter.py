message_index = 0
routing = [(6, 10), (16, 3), (11, 14), (1, 5), (9, 17)]
station_angles = [6, 27, 52, 61, 88, 116, 127, 157, 164, 197, 213, 230, 241, 273, 291, 316, 322, 353]
radio_angle_precision = 10.0

def is_KA_near_to_recipient():
    return abs(normalize_angle_difference(station_angles[routing[message_index][1]] - navigation.get_z_axis_angle())) < radio_angle_precision
