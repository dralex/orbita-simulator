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

clean:
	@for i in $(MODELS); do \
            $(MAKE) -C $(MODELS_DIR)/$$i clean; \
        done
	rm -rf __pycache__ models/__pycache__
	rm -f *~ *.pyc

.PHONY: all clean
