SOURCE := manual-ru.tex
TARGET := $(patsubst %.tex, %.dvi, $(SOURCE))
TARGET_PDF := $(patsubst %.tex, %.pdf, $(SOURCE))

SOURCE_EN := manual-en.tex
TARGET_EN := $(patsubst %.tex, %.dvi, $(SOURCE_EN))
TARGET_PDF_EN := $(patsubst %.tex, %.pdf, $(SOURCE_EN))

IMAGES_SRC := $(wildcard $(addsuffix /*.svg, images ))
IMAGES := $(patsubst %.svg, %.eps, $(IMAGES_SRC))

$(TARGET): $(SOURCE) $(IMAGES)
	latex $(SOURCE)
	latex $(SOURCE)

$(TARGET_EN): $(SOURCE_EN) $(IMAGES)
	latex $(SOURCE_EN)
	latex $(SOURCE_EN)

pdf: $(TARGET) $(TARGET_EN)
	dvipdf $(TARGET) $(TARGET_PDF)
	dvipdf $(TARGET_EN) $(TARGET_PDF_EN)

clean:
	-rm -f sources/*~
	-rm -rf images/*.eps images/*~
	-rm -f *.dvi *.aux *.log *.out *.toc *~
	-rm -f $(TARGET) $(TARGET_EN)

%.eps: %.svg
	inkscape -z -f $< -E $@ -D --export-ignore-filters --export-ps-level=3 2>/dev/null

.PHONY: clean pdf
