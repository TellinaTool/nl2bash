# NL2Bash Data

## Content

NL2Bash contains 12k one-line Linux shell commands used in practice and their natural language descriptions provided by experts. The dataset includes 100+ commonly used shell utilities, providing a rich training and test bed for automatically translating natural language into command lines.

The parallel data are stored with a source file `bash/\*.nl` and a target file `bash/\*.cm`.
The entire corpus `bash/all.nl, bash/all.cm` are randomly splited into train, dev, and test set with a ratio of `10:1:1`.

### Manual Evaluations

The manual evaluations of a subset of model predictions are stored in `bash/manual_judgments/` in `csv` format.


## Random Split and Pre-processing

### Filtering
Filtering the raw parallel corpus.
```
python3 scripts/filter_data.py bash
```

### Splitting
Randomly split the filtered parallel corpus into train, dev and test (using fixed random seed).
```
python3 scripts/split_data.py bash
```
Statistics of the dataset split is shown below.

|| Train | Dev | Test |
| :---: | :---: | :---: | :---: |
|# pairs| 8090 | 609 | 606 |

### Preprocessing for running Tensorflow models
```
cd ../experiments

./bash-run.sh --process_data --dataset bash
```

## Citation

If you use the data or source code in your work, please cite
```
@techreport{LinWPVZE2017:TR, 
  author = {Xi Victoria Lin and Chenglong Wang and Deric Pang and Kevin Vu and Luke Zettlemoyer and Michael D. Ernst}, 
  title = {Program synthesis from natural language using recurrent neural networks}, 
  institution = {University of Washington Department of Computer Science and Engineering}, 
  number = {UW-CSE-17-03-01}, 
  address = {Seattle, WA, USA}, 
  month = mar, 
  year = {2017} 
}
```
