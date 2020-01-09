## Bash Command Parser

This submodule is a bash command parser which augments the [bashlex](https://github.com/idank/bashlex) tool with utility-flag, utility-argument and flag-argument edges. 

_The parser cannot parse the following code structures._
1. Multi-statement code blocks.


### Test the parser in a simple commandline interface:

```
python3 -m bashlint.data_tools
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
