all:
	rm -rf venus
	pyxbgen xml-schemas/devices.xsd -m venus.devices
	pyxbgen xml-schemas/missions.xsd -m venus.missions
	pyxbgen xml-schemas/probe.xsd -m venus.probe
	pyxbgen xml-schemas/global_parameters.xsd -m venus.global_parameters
	pyxbgen xml-schemas/global_config.xsd -m venus.global_config
	pyxbgen xml-schemas/shortlog.xsd -m venus.shortlog

	protoc --python_out=. api/systems.proto

messages:
	mkdir -p ru/LC_MESSAGES
	msgfmt sputnik.pot -o ru/LC_MESSAGES/sputnik.mo

pylint:
	python3 pylint_test.py

clean:
	rm -rf venus
	rm -rf __pycache__ api/__pycache__ api-test/__pycache__ pycontrol/__pycache__ missions/__pycache__ calcmodels/__pycache__
	rm -rf ru	
	rm -f *~ pycontrol/*~ api/*~ xml-schemas/*~ probes/*~ missions/*~ calcmodels/*~ api-test/*~ api/systems_pb2.py

.PHONY: all clean
