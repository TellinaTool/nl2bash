## Process data

Suppose the parallel corpus is placed at `../data/<dataset_name>`. The following script converts the parallel corpus into format read by the neural network:
```
./train.sh --process_data --dataset <dataset_name>
```

## Run experiments

The following script can be used to re-train the Tellina model:
```
./bash-final-attn.sh
```

To reproduce the output on the test set:
```
./bash-final-attn.sh --test --decode --fill_argument_slots
```
