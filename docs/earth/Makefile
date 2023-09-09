SOURCE := manual-ru.tex
TARGET := $(patsubst %.tex, %.dvi, $(SOURCE))
TARGET_PDF := $(patsubst %.tex, %.pdf, $(SOURCE))

EN_SOURCE := manual-en.tex
EN_TARGET := $(patsubst %.tex, %.dvi, $(EN_SOURCE))
EN_TARGET_PDF := $(patsubst %.tex, %.pdf, $(EN_SOURCE))

HSM_SOURCE := hsm-manual-ru.tex
HSM_TARGET := $(patsubst %.tex, %.dvi, $(HSM_SOURCE))
HSM_TARGET_PDF := $(patsubst %.tex, %.pdf, $(HSM_SOURCE))

HSM_EN_SOURCE := hsm-manual-en.tex
HSM_EN_TARGET := $(patsubst %.tex, %.dvi, $(HSM_EN_SOURCE))
HSM_EN_TARGET_PDF := $(patsubst %.tex, %.pdf, $(HSM_EN_SOURCE))

IMAGES_SRC := $(wildcard $(addsuffix /*.svg, images ))
IMAGES := $(patsubst %.svg, %.eps, $(IMAGES_SRC))

$(TARGET): $(SOURCE) $(IMAGES)
	latex $(SOURCE)
	latex $(SOURCE)

$(EN_TARGET): $(EN_SOURCE) $(IMAGES)
	latex $(EN_SOURCE)
	latex $(EN_SOURCE)

hsm: $(HSM_TARGET)

$(HSM_TARGET): $(HSM_SOURCE) $(IMAGES)
	latex $(HSM_SOURCE)
	latex $(HSM_SOURCE)

$(HSM_EN_TARGET): $(HSM_EN_SOURCE) $(IMAGES)
	latex $(HSM_EN_SOURCE)
	latex $(HSM_EN_SOURCE)

pdf: $(TARGET) $(EN_TARGET) $(HSM_TARGET) $(HSM_EN_TARGET)
	dvipdf $(TARGET) $(TARGET_PDF)
	dvipdf $(EN_TARGET) $(EN_TARGET_PDF)
	dvipdf $(HSM_TARGET) $(HSM_TARGET_PDF)
	dvipdf $(HSM_EN_TARGET) $(HSM_EN_TARGET_PDF)


clean:
	-rm -f sources/*~
	-rm -rf images/*.eps images/*~
	-rm -f *.dvi *.aux *.log *.out *.toc *~
	-rm -f $(TARGET) $(EN_TARGET) $(HSM_TARGET) $(HSM_EN_TARGET)

%.eps: %.svg
	inkscape -z -f $< -E $@ -D --export-ignore-filters --export-ps-level=3 2>/dev/null

.PHONY: clean pdf hsm
