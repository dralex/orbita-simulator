unix:
	rm -rf venus
	python3 ../../pyxbgen.py xml-schemas/global_parameters.xsd -m venus.global_parameters
	python3 ../../pyxbgen.py xml-schemas/shortlog.xsd -m venus.shortlog
	python3 ../../pyxbgen.py xml-schemas/testmodel.xsd -m venus.testmodel

win:
	python3 ../../pyxbgen.py xml-schemas/global_parameters.xsd -m venus.global_parameters
	python3 ../../pyxbgen.py xml-schemas/shortlog.xsd -m venus.shortlog
	python3 ../../pyxbgen.py xml-schemas/testmodel.xsd -m venus.testmodel

messages:
	mkdir -p ru/LC_MESSAGES
	msgfmt sputnik.pot -o ru/LC_MESSAGES/sputnik.mo

clean_unix:
	rm -rf venus
	rm -rf __pycache__ calcmodels/__pycache__
	rm -rf ru	
	rm -f *~ xml-schemas/*~ probes/*~ calcmodels/*~

clean_win:
	rmdir venus
	rmdir __pycache__ calcmodels/__pycache__
	rmdir ru	
	rmdir *~ xml-schemas/*~ probes/*~ calcmodels/*~

.PHONY: all clean
