.PHONY: all clean

all: research_abstract.pdf

research_abstract.pdf: $(wildcard *.tex) sigproc.bib normalization.png 
	latexmk -pdf -pdflatex='pdflatex -interaction nonstopmode' 'main.tex'
clean:
	$(RM) *.pdf *.bbl *.blg *.log *.fls *.out *.aux *.fdb_latexmk
