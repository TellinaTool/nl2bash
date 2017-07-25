## Heuristics-Based Bash Parser

This submodule is a generic bash command parser, which is a version of the [bashlex](https://github.com/idank/bashlex) tool augmented with utility-flag, utility-argument and flag-argument relationships. 

_The parser cannot parse multi-command code blocks._

### Test the parser in a simple interactive commandline interface:

```
python data_tools.py
```

### Input: 
```
find /mnt/naspath ! \( -name .snapshot -prune \) -type f -mtime 0 -print0
```

### Output:
The parser outputs the AST structure of the input bash command. By default the arguments in the command are replaced by their types.
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
