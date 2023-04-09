from probeapi import *

engine = False
while probe.run():
    t = probe.cpu_get_flight_time()
    if not engine and 100 <= t <= 300:
        probe.set_device_state('EG1', STATE_ON)
        engine = True
        continue
    if engine and t > 300:
        probe.set_device_state('EG1', STATE_OFF)
        engine = False
        continue
    if probe.navigation_has_landed():
        probe.telemetry_send_message('landed\n')
        break
