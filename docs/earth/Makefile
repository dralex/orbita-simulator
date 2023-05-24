SOURCE := manual-ru.tex
TARGET := $(patsubst %.tex, %.dvi, $(SOURCE))
TARGET_PDF := $(patsubst %.tex, %.pdf, $(SOURCE))

HSM_SOURCE := hsm-manual-ru.tex
HSM_TARGET := $(patsubst %.tex, %.dvi, $(HSM_SOURCE))
HSM_TARGET_PDF := $(patsubst %.tex, %.pdf, $(HSM_SOURCE))

IMAGES_SRC := $(wildcard $(addsuffix /*.svg, images ))
IMAGES := $(patsubst %.svg, %.eps, $(IMAGES_SRC))

$(TARGET): $(SOURCE) $(IMAGES)
	latex $(SOURCE)
	latex $(SOURCE)

hsm: $(HSM_TARGET)

$(HSM_TARGET): $(HSM_SOURCE) $(IMAGES)
	latex $(HSM_SOURCE)
	latex $(HSM_SOURCE)

pdf: $(TARGET) $(HSM_TARGET)
	dvipdf $(TARGET) $(TARGET_PDF)
	dvipdf $(TARGET) $(HSM_TARGET_PDF)

clean:
	-rm -f sources/*~
	-rm -rf images/*.eps images/*~
	-rm -f *.dvi *.aux *.log *.out *.toc *~
	-rm -f $(TARGET) $(HSM_TARGET)

%.eps: %.svg
	inkscape -z -f $< -E $@ -D --export-ignore-filters --export-ps-level=3 2>/dev/null

.PHONY: clean pdf hsm
