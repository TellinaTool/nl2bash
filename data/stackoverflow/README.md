# StackOverflow Data

This folder has scripts and data related to StackOverflow.

Contents:

 - `stackoverflow-xml-to-sqlite.py`: converts the raw StackOverflow XML data
   dump into a [SQLite](https://www.sqlite.org/) database for easy use.
 - `stackoverflow.sqlite.xz`: the output of `stackoverflow-xml-to-sqlite.py`
   compressed using [XZ](http://tukaani.org/xz/). To extract this data, just
   run `unxz --keep stackoverflow.sqlite.gz`.

XZ is available for most platforms, and it generally does a better job of
compressing than GZip or BZip2. On OSX, you can install XZ with
[Homebrew](http://brew.sh/): `brew install xz`.
