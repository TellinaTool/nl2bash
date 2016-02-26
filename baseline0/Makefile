.PHONY: all clean

all: src/model.py

../data/stackoverflow/stackoverflow.sqlite: ../data/stackoverflow/stackoverflow.sqlite.xz
	unxz --force --keep $<

src/model.py: src/make_model.py ../data/stackoverflow/stackoverflow.sqlite
	python $^ >/tmp/f && mv /tmp/f $@

clean:
	$(RM) ../data/stackoverflow/stackoverflow.sqlite
	$(RM) src/model.py
