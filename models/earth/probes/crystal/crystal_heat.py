heating = False


def control_heat():
    global heating
    temp = heat_control.get_temperature()
    if temp < 290:
        if not heating:
            heat_control.start_heating()
            heating = True
    else:
        if heating:
            heat_control.stop_heating()
            heating = False
