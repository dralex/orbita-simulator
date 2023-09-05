def is_camera_focused_on_target():
    a = navigation.get_z_axis_angle()
    return abs(a - target_angle) <= 1