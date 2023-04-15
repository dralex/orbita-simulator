# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------

# remove this import before using
from systems import *

t = 508
w = -0.06
M0 = -0.000009
M = 0.000001
dw = 0.00001

mode = 'rotate'
sputnik.orientation.set_motor_moment(AXIS_Z, M0);
sputnik.orientation.start_motor(AXIS_Z);
moment = True

while sputnik.cpu.run():

    if mode == 'rotate' and sputnik.cpu.get_flight_time() >= t: 
        mode = 'ok'
        sputnik.orientation.stop_motor(AXIS_Z)
        moment = False

    if mode == 'ok':
        av = sputnik.orientation.get_angular_velocity(AXIS_Z)
        if abs(av - w) < dw:
            if moment:
                sputnik.orientation.stop_motor(AXIS_Z)
                moment = False
        elif not moment:
            sputnik.orientation.start_motor(AXIS_Z)
            moment = True
            if av > w:
                sputnik.orientation.set_motor_moment(AXIS_Z, -M)
            else:
                sputnik.orientation.set_motor_moment(AXIS_Z, M)
