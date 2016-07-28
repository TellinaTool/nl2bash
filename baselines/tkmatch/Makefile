SO_DB=../data/stackoverflow/stackoverflow.sqlite

.PHONY: all clean

all: src/model.py

%: %.xz
	unxz --force --keep $<

src/model.py: src/make_model.py ../baseline1/src/bash.py src/common.py $(SO_DB)
	python $< $(SO_DB) >/tmp/f && mv /tmp/f $@

clean:
	$(RM) ../data/stackoverflow/stackoverflow.sqlite
	$(RM) src/model.py
