.PHONY: all clean

all: NL2Commands.pdf

NL2Commands.pdf: NL2Commands.tex bibliography.bib
	latexmk -pdf -pdflatex='pdflatex -interaction nonstopmode' '$<'

clean:
	$(RM) *.pdf *.bbl *.blg *.log *.fls *.out *.aux *.fdb_latexmk
