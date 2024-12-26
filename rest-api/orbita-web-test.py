#!/usr/bin/python3

from time import sleep
import requests

BASE_URL = 'http://orbita.kruzhok.org/'

print('server')
url = BASE_URL + 'server'
response = requests.get(url)
print(response.json())
print()

print('parameters')
url = BASE_URL + 'parameters'
response = requests.get(url, json={"model": "planets", "mission": "Moon"})
print(response.json())
print()

print('sample')
url = BASE_URL + 'sample'
response = requests.get(url, json={"model": "planets", "mission": "Moon"})
print(response.json())
print()

print('devices')
url = BASE_URL + 'devices'
response = requests.get(url, json={"model": "planets"})
print('data len: ', len(response.json()['data']))
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

print('calculation')
url = BASE_URL + 'calculation'
response = requests.post(url, json={"model": MODEL, "xml": XML_BLOB})
print(response)
task_id = response.json()['id']
print('task id: ', task_id)
print()

sleep(0.1)

print('status')
url = BASE_URL + 'status'
response = requests.get(url, json={"model": MODEL, "id": task_id})
print(response.json())
print()

sleep(2)

print('status')
url = BASE_URL + 'status'
response = requests.get(url, json={"model": MODEL, "id": task_id})
print(response.json())
print()

print('result')
url = BASE_URL + 'result'
response = requests.get(url, json={"model": MODEL, "id": task_id})
print(response.json())
print()
