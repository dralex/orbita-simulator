all:
	rm -rf venus
	python3 ../../pyxbgen.py xml-schemas/global_parameters.xsd -m venus.global_parameters
	python3 ../../pyxbgen.py xml-schemas/global_config.xsd -m venus.global_config
	python3 ../../pyxbgen.py xml-schemas/planets.xsd -m venus.planets
	python3 ../../pyxbgen.py xml-schemas/testmodel.xsd -m venus.testmodel

messages:
	mkdir -p ru/LC_MESSAGES
	msgfmt orbita.pot -o ru/LC_MESSAGES/orbita.mo

pylint:
	pylint *.py

clean:
	rm -rf venus
	rm -rf __pycache__
	rm -rf ru	
	rm -f *~ pycontrol/*~ api/*~ xml-schemas/*~ probes/*~ *.pyc

.PHONY: all clean
