SO_DB=../data/stackoverflow/stackoverflow.sqlite

.PHONY: all clean

%: %.xz
	unxz --force --keep $<

preprocess: src/preprocess.py
	python src/preprocess.py $(SO_DB)

clean:
	$(RM) ../data/stackoverflow/stackoverflow.sqlite
	$(RM) src/preprocess.py
