# NL-Bash Parallel Corpus

## Content

The parallel data are stored in a source file `bash/\*.nl` and a target file `bash/\*.cm`.
The entire corpus `bash/all.nl, bash/all.cm` are randomly splited into train, dev, and test set with a ratio of `10:1:1`.

### Manual Evaluations

The manual evaluations of a subset of model predictions are stored in `bash/manual_judgments/` in `csv` format.


## Data Processing

### Filtering
Filtering the raw parallel corpus.
```
python3 scripts/filter_data.py bash
```

### Spliting
Split the filtered parallel corpus into train, dev and test.
```
python3 scripts/split_data.py bash
```

### Converting to format recognized by the Tensorflow models
```
cd ../experiments

./bash-run.sh --process_data --dataset bash
```