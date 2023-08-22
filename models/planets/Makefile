unix:
	rm -rf venus
	python3 ../../pyxbgen.py xml-schemas/planets.xsd -m venus.planets
	python3 ../../pyxbgen.py xml-schemas/devices.xsd -m venus.devices
	python3 ../../pyxbgen.py xml-schemas/probe.xsd -m venus.probe
	python3 ../../pyxbgen.py xml-schemas/global_parameters.xsd -m venus.global_parameters
	python3 ../../pyxbgen.py xml-schemas/global_config.xsd -m venus.global_config
	protoc --python_out=. api/probe.proto

win:
	python3 ../../pyxbgen.py xml-schemas/planets.xsd -m venus.planets
	python3 ../../pyxbgen.py xml-schemas/devices.xsd -m venus.devices
	python3 ../../pyxbgen.py xml-schemas/probe.xsd -m venus.probe
	python3 ../../pyxbgen.py xml-schemas/global_parameters.xsd -m venus.global_parameters
	python3 ../../pyxbgen.py xml-schemas/global_config.xsd -m venus.global_config
	protoc --python_out=. api/probe.proto	

messages:
	mkdir -p ru/LC_MESSAGES
	msgfmt orbita.pot -o ru/LC_MESSAGES/orbita.mo

pylint:
	pylint *.py

clean_unix:
	rm -rf venus
	rm -rf __pycache__ api/__pycache__ pycontrol/__pycache__ api-test/__pycache__
	rm -rf ru	
	rm -f *~ pycontrol/*~ api/*~ xml-schemas/*~ probes/*~ *.pyc api-test/*~ api/probe_pb2.py

clean_win:
	rmdir venus
	rmdir __pycache__ api/__pycache__ pycontrol/__pycache__ api-test/__pycache__
	rmdir ru	
	rmdir *~ pycontrol/*~ api/*~ xml-schemas/*~ probes/*~ *.pyc api-test/*~ api/probe_pb2.py

.PHONY: all clean


