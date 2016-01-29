.PHONY: all clean

all: relatedwork.pdf

relatedwork.pdf: relatedwork.tex bibliography.bib
	latexmk -pdf -pdflatex='pdflatex -interaction nonstopmode' '$<'

clean:
	$(RM) *.pdf *.bbl *.blg *.log *.fls *.out *.aux *.fdb_latexmk
