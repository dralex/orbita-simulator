#!/usr/bin/python3

from time import sleep
import orbita

api = orbita.OrbitaServerAPI('../orbita_server.cfg',
                             '.',
                             '/static/results',
                             '/static/images/')

print(api.server())
print()

print(api.parameters('planets'))
print()

print(api.devices('planets'))
print()


MODEL = 'planets_gravity'
XML_BLOB = '''<?xml version="1.0" encoding="utf-8"?>
<v:testmodel name="test" xmlns:v="venus">
  <planet>Mars</planet>
  <tick>10</tick>
  <square>10.0</square>
  <mass>100.0</mass>
  <h>50000</h>
  <x>0</x>
  <vy>0</vy>
  <vx>5000</vx>
  <aerodynamic_coeff>0.47</aerodynamic_coeff>
</v:testmodel>'''

res = api.calculation(MODEL, XML_BLOB)
print(res)
print()
task_id = res['id']

sleep(0.1)

print(api.status(MODEL, task_id))
print()

sleep(2)

res = api.status(MODEL, task_id)
print(res)
print()
status = res['status']
assert status == 'completed'

print(api.result(MODEL, task_id))
print()

try:
    api.calculation('aaa', 'bbb')
except orbita.OrbitaNotFoundException:
    pass
try:
    api.calculation('planets', '')
except orbita.OrbitaBadRequestException:
    pass

try:
    api.status('aaa', '123')
except orbita.OrbitaNotFoundException:
    pass
try:
    api.status('planets', '0/1')
except orbita.OrbitaBadRequestException:
    pass

try:
    api.result('aaa', '123')
except orbita.OrbitaNotFoundException:
    pass
