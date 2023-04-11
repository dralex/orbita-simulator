all:
	rm -rf venus
	pyxbgen xml-schemas/global_parameters.xsd -m venus.global_parameters
	pyxbgen xml-schemas/shortlog.xsd -m venus.shortlog
	pyxbgen xml-schemas/testmodel.xsd -m venus.testmodel

messages:
	mkdir -p ru/LC_MESSAGES
	msgfmt sputnik.pot -o ru/LC_MESSAGES/sputnik.mo

clean:
	rm -rf venus
	rm -rf __pycache__ calcmodels/__pycache__
	rm -rf ru	
	rm -f *~ xml-schemas/*~ probes/*~ calcmodels/*~

.PHONY: all clean
