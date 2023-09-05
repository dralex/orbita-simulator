Min_temp = 263
Max_temp = 313
Max_power = 4

Avg_temp = (Min_temp + Max_temp) / 2
DT = abs(Avg_temp - Min_temp) / 2

def temp_low():
    return heat_control.get_temperature() < Avg_temp - DT

def update_power():
    t = heat_control.get_temperature()
    p = Max_power * 2 * abs(t - Avg_temp) / DT
    heat_control.set_power(p)

update_power()