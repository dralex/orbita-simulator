all:
	rm -rf venus
	pyxbgen xml-schemas/planets.xsd -m venus.planets
	pyxbgen xml-schemas/devices.xsd -m venus.devices
	pyxbgen xml-schemas/probe.xsd -m venus.probe
	pyxbgen xml-schemas/global_parameters.xsd -m venus.global_parameters
	pyxbgen xml-schemas/global_config.xsd -m venus.global_config
	protoc --python_out=. api/probe.proto

messages:
	mkdir -p ru/LC_MESSAGES
	msgfmt orbita.pot -o ru/LC_MESSAGES/orbita.mo

pylint:
	pylint *.py

clean:
	rm -rf venus
	rm -rf __pycache__ api/__pycache__ pycontrol/__pycache__
	rm -rf ru	
	rm -f *~ pycontrol/*~ api/*~ xml-schemas/*~ probes/*~ *.pyc api/probe_pb2.py

.PHONY: all clean


