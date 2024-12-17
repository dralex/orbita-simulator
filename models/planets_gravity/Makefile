unix:
	rm -rf venusg
	python3 ../../pyxbgen.py xml-schemas/global_parameters.xsd -m venusg.global_parameters
	python3 ../../pyxbgen.py xml-schemas/global_config.xsd -m venusg.global_config
	python3 ../../pyxbgen.py xml-schemas/planets.xsd -m venusg.planets
	python3 ../../pyxbgen.py xml-schemas/testmodel.xsd -m venusg.testmodel

win:
	python3 ../../pyxbgen.py xml-schemas/global_parameters.xsd -m venusg.global_parameters
	python3 ../../pyxbgen.py xml-schemas/global_config.xsd -m venusg.global_config
	python3 ../../pyxbgen.py xml-schemas/planets.xsd -m venusg.planets
	python3 ../../pyxbgen.py xml-schemas/testmodel.xsd -m venusg.testmodel

messages:
	mkdir -p ru/LC_MESSAGES
	msgfmt orbita.pot -o ru/LC_MESSAGES/orbita.mo

pylint:
	pylint *.py

clean_unix:
	rm -rf venusg
	rm -rf __pycache__
	rm -rf ru	
	rm -f *~ pycontrol/*~ api/*~ xml-schemas/*~ probes/*~ *.pyc

clean_win:
	rmdir venusg
	rmdir __pycache__
	rmdir ru	
	rmdir *~ pycontrol/*~ api/*~ xml-schemas/*~ probes/*~ *.pyc

.PHONY: all clean
