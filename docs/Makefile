.PHONY: all clean

all: writeup.pdf

writeup.pdf: $(wildcard *.tex) bibliography.bib architecture.pdf
	latexmk -pdf -pdflatex='pdflatex -interaction nonstopmode' 'writeup.tex'
clean:
	$(RM) *.pdf *.bbl *.blg *.log *.fls *.out *.aux *.fdb_latexmk
