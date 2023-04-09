MODELS := planets earth

all: 
	@for i in $(MODELS); do \
            $(MAKE) -C $$i; \
        done

pdf:
	@for i in $(MODELS); do \
            $(MAKE) -C $$i pdf; \
        done

clean:
	-rm -f *~
	@for i in $(MODELS); do \
            $(MAKE) -C $$i clean; \
        done

.PHONY: all clean
