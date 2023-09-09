MODELS_DIR := models
MODELS := ${shell ls --hide=__* $(MODELS_DIR)}

all: 
	@for i in $(MODELS); do \
            $(MAKE) -C $(MODELS_DIR)/$$i; \
        done

pylint:
	pylint *.py
	@for i in $(MODELS); do \
            $(MAKE) -C $(MODELS_DIR)/$$i pylint; \
        done

docs:
	$(MAKE) -C docs

clean_unix:
	@for i in $(MODELS); do \
            $(MAKE) -C $(MODELS_DIR)/$$i clean; \
        done
	$(MAKE) -C docs clean
	rm -rf __pycache__ models/__pycache__
	rm -f *~ *.pyc

clean_win:
	@for i in $(MODELS); do \
            $(MAKE) -C $(MODELS_DIR)/$$i clean; \
        done
	$(MAKE) -C docs clean
	rmdir __pycache__ models/__pycache__
	rmdir *~ *.pyc

.PHONY: all clean docs pylint


