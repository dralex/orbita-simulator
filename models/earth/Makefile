unix:
	rm -rf venus
	python3 ../../pyxbgen.py xml-schemas/devices.xsd -m venus.devices
	python3 ../../pyxbgen.py xml-schemas/missions.xsd -m venus.missions
	python3 ../../pyxbgen.py xml-schemas/probe.xsd -m venus.probe
	python3 ../../pyxbgen.py xml-schemas/global_parameters.xsd -m venus.global_parameters
	python3 ../../pyxbgen.py xml-schemas/global_config.xsd -m venus.global_config
	python3 ../../pyxbgen.py xml-schemas/shortlog.xsd -m venus.shortlog

	protoc --python_out=. api/systems.proto

win:
	python3 ../../pyxbgen.py xml-schemas/devices.xsd -m venus.devices
	python3 ../../pyxbgen.py xml-schemas/missions.xsd -m venus.missions
	python3 ../../pyxbgen.py xml-schemas/probe.xsd -m venus.probe
	python3 ../../pyxbgen.py xml-schemas/global_parameters.xsd -m venus.global_parameters
	python3 ../../pyxbgen.py xml-schemas/global_config.xsd -m venus.global_config
	python3 ../../pyxbgen.py xml-schemas/shortlog.xsd -m venus.shortlog

	protoc --python_out=. api/systems.proto

messages:
	mkdir -p ru/LC_MESSAGES
	msgfmt sputnik.pot -o ru/LC_MESSAGES/sputnik.mo

pylint:
	python3 pylint_test.py

clean_unix:
	rm -rf venus
	rm -rf __pycache__ api/__pycache__ api-test/__pycache__ pycontrol/__pycache__ missions/__pycache__ calcmodels/__pycache__
	rm -rf sm/__pycache__ sm/test/__pycache__
	rm -rf ru	
	rm -f *~ pycontrol/*~ api/*~ xml-schemas/*~ probes/*~ missions/*~ calcmodels/*~ api-test/*~ api/systems_pb2.py
	rm -f sm/*~ sm/templates/*~ sm/test/*~ sm/test/graphs/*~

clean_win:
	rmdir venus
	rmdir __pycache__ api/__pycache__ api-test/__pycache__ pycontrol/__pycache__ missions/__pycache__ calcmodels/__pycache__
	rmdir sm/__pycache__ sm/test/__pycache__
	rmdir ru	
	rmdir *~ pycontrol/*~ api/*~ xml-schemas/*~ probes/*~ missions/*~ calcmodels/*~ api-test/*~ api/systems_pb2.py
	rmdir sm/*~ sm/templates/*~ sm/test/*~ sm/test/graphs/*~

.PHONY: all clean