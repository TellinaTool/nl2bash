# Manual Evaluation Script

## Change Directory
Enter the [scripts](https://github.com/TellinaTool/nl2bash/tree/master/scripts) directory.
```
cd scripts
```

## Run Manual Evaluation
```
<experiment-start-script> --manual_eval <gpu-id>
```
For example, to obtain the manual evaluation results of the sub-token CopyNet model, run 
```
./bash-copy-partial-token.sh --manual_eval 0
```

This will print the manual evaluation results if there are no unjudged predictions in the data being evaluated. 

By default, the top 3 predictions of 100 randomly sampled examples are passed through the manual evaluation.

If there are unjudged predictions (e.g. you have just updated the model and it made many new predictions), the above will trigger a commandline interface which will prompt you to input the judgement for the new predictions.

## Manual Evaluation Interface

<p align="left">
  <img src="http://victorialin.net/img/github/nl2bash_manual_eval_script.png" width="600" title="NL2Bash utility distribution">
</p>

The commandline interface prompts you to input two judgements.

1. Is the structure of the predicted command correct? In other words, is the predicted command correct if we ignore the errors in its arguments?

2. Is the predicted command correct (i.e. executable and semantically correct)? 

For both questions, replying "y" or "Y" implies a "correct" judgement; any other input string is interpreted as an "incorrect" judgement. 

If an "incorrect" judgement is received for the first question, the second question will be skipped and an "incorrect" judgement will be automatically recorded for it.

All the judgements you input are saved to [data/bash/manual_judgements/manual.evaluations.author](https://github.com/TellinaTool/nl2bash/blob/master/data/bash/manual_judgements/manual.evaluations.author) and will be reused in future experiments.

The manual evaluation results will be printed once you have input the judgements for all new predictions.
```
100 examples evaluated
Top 1 Command Acc = 0.370
Top 3 Command Acc = 0.490
Top 1 Template Acc = 0.500
Top 3 Template Acc = 0.620
```

## Customize the Interface
To customize the manual evaluation interface, please modify the `get_manual_evaluation_metrics` function in [eval/eval_tools.py](https://github.com/TellinaTool/nl2bash/blob/master/eval/eval_tools.py#L83).





