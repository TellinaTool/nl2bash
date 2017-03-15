## Heuristics-Based Bash Command Parser

This folder contains the implementation of a general purpose bash command parser, which is implemented on top of the [bashlex](https://github.com/idank/bashlex) tool. It parses a bash oneliner command based on the man-page grammars and heuristics.

The current parser does not parse multi-command code blocks.

### Test the parser in a simple interactive commandline interface:

```
python data_tools.py
```

### Input: 
```
find /mnt/naspath ! \( -name .snapshot -prune \) -type f -mtime 0 -print0
```

### Output:
The output of the parser is the AST structure of the input bash command, with open-vocabulary arguments in the command replaced by their types.
```
ROOT()
    HEADCOMMAND(find)
        ARGUMENT(_REGEX)
        UNARYLOGICOP(!)
        BRACKET()
            FLAG(-name)
                ARGUMENT(_REGEX)
            UNARYLOGICOP(-prune)
        FLAG(-type)
            ARGUMENT(f)
        FLAG(-mtime)
            ARGUMENT(_NUM)
        FLAG(-print0)
 ```
