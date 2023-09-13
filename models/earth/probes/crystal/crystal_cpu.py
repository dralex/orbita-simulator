telemetry.set_period(60)

start_time = 0

def switching_off_subsystems():
    global start_time
    start_time = cpu.get_flight_time()
    engine.set_state(STATE_OFF)
    telemetry.set_state(STATE_OFF)
    navigation.set_state(STATE_OFF)
    orientation.set_state(STATE_OFF)
    container.set_state(STATE_ON)
    container.start_experiment()

def switching_on_subsystems():
    container.stop_experiment()
    container.set_state(STATE_OFF)
    heat_control.set_state(STATE_OFF)
    engine.set_state(STATE_ON)
    telemetry.set_state(STATE_ON)
    navigation.set_state(STATE_ON)
    orientation.set_state(STATE_ON)