#!/usr/bin/python3

from xmlconverters import Devices
from language import Language

Language.set_lang('ru')
devs = Devices.load_devices_all(Language, 'devices-ru.xml')
print(Devices.table(devs['s'],
                    devs['d'],
                    devs['p']))

