# Manual Evaluation Script

## Change Directory
Enter the [experiments](https://github.com/TellinaTool/nl2bash/tree/master/experiments) directory.
```
cd experiments
```

## Run Manual Evaluation
```
<experiment-bash-script> --manual_eval <gpu-id>
```
For example, to obtain the manual evaluation results of the sub-token CopyNet model, run the following.
```
./bash-copy-partial-token.sh --manual_eval 0
```

This will print the manual evaluation results if there are no unjudged predictions in the dataset being evaluated. 

By default, 100 examples are randomly sampled to pass through the manual evaluation.

If there are unjudged prediction (e.g. the model has been updated), the above command triggers a commandline interface which will prompt you to input the judgement for the new predictions.

## Manual Evaluation Interface

<p align="left">
  <img src="http://victorialin.net/img/github/nl2bash_manual_eval_script.png" width="600" title="NL2Bash utility distribution">
</p>

The commandline interface will prompt you to input two judgements.

1. Is the structure of the predicted command correct? In other words, is the predicted command correct ignoring the errors in its arguments?

2. Is the predicted command correct (executable and semantically correct)? 

For both questions, replying "y" or "Y" implies a "correct" judgement; any other input string will be taken as an "incorrect" judgement. 

If an "incorrect" judgement is received for the first question, the second question will be skipped and an "incorrect" judgement will be automatically recorded for it.

All of your judgement inputs are written to `[data/bash/manual_judgements/manual.evaluations.author](https://github.com/TellinaTool/nl2bash/blob/master/data/bash/manual_judgements/manual.evaluations.author)` and will be reused in future experiments.

The manual evaluation results will be printed once you have input the judgements for all new predictions.
```
100 examples evaluated
Top 1 Command Acc = 0.370
Top 3 Command Acc = 0.490
Top 1 Template Acc = 0.500
Top 3 Template Acc = 0.620
```

## Customize the Interface
To customize the manual evaluation interface, please modify the `get_manual_evaluation_metrics` function in `eval/eval_tools.py`(https://github.com/TellinaTool/nl2bash/blob/master/eval/eval_tools.py#L83).





