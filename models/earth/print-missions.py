#!/usr/bin/python3

import xmlconverters

m = xmlconverters.Missions.decode(open('missions-ru.xml').read())
print(m.table())

