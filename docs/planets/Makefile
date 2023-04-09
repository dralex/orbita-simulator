SOURCE := manual-ru.tex
TARGET := $(patsubst %.tex, %.dvi, $(SOURCE))
TARGET_PDF := $(patsubst %.tex, %.pdf, $(SOURCE))

IMAGES_SRC := $(wildcard $(addsuffix /*.svg, images ))
IMAGES := $(patsubst %.svg, %.eps, $(IMAGES_SRC))

$(TARGET): $(SOURCE) $(IMAGES)
	latex $(SOURCE)
	latex $(SOURCE)

pdf: $(TARGET)
	dvipdf $(TARGET) $(TARGET_PDF)

clean:
	-rm -f sources/*~
	-rm -rf images/*.eps images/*~
	-rm -f *.dvi *.aux *.log *.out *.toc *~
	-rm -f $(TARGET)

%.eps: %.svg
	inkscape -z -f $< -E $@ -D --export-ignore-filters --export-ps-level=3 2>/dev/null

.PHONY: clean pdf
