heater_power = 70

heating = False


def control_heat():
    global heating
    temp = heat_control.get_temperature()
    if (temp < 285) and not heating:
        heating = True
        heat_control.set_power(heater_power)
        heat_control.start_heating()
    elif (temp > 300) and heating:
        heating = False
        heat_control.set_power(0)
        heat_control.stop_heating()
