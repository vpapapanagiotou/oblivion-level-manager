# oblivion-level-manager
A level manager utility for the game *The Elder Scrolls IV: Oblivion*.

## Program arguments

### General use:

```
usage: oblivionlevelmanagercli.py [-h] [--path PATH] {new,load} ...

positional arguments:
  {new,load}
    new        Create a new character
    load       Load a character

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  Path to load/save the character files
```

### `new` command:

```
usage: python oblivionlevelmanagercli.py new [-h] name

positional arguments:
  name        The name of the new character

optional arguments:
  -h, --help  show this help message and exit
```

### `load` command:

```
usage: python oblivionlevelmanagercli.py load [-h] [--level LEVEL] name

positional arguments:
  name           The name of the character to load

optional arguments:
  -h, --help     show this help message and exit
  --level LEVEL  The level of the character to load (default: max available)
```

## List of commands

```
print           Usage: print [all|character|attributes|skills|plan]
                Print information about your character, attributes, skills, or level-
                up plan
                Alternative names: show
set-value       Usage: set-value {level|attribute|skill} [name] value
                Utility to set-up your character after creation. Sub-commands
                'attribute' and 'skill' require a 'name' argument (i.e. name of the
                attribute or skill whose value is being set).
                Alternative names: setvalue, set-val, setval
increase-skill  Usage: increase-skill [value]
                Increase a skill by 1 point. Argument 'value' can be used to increase
                (or decrease if negative) by more points.
                Alternative names: increase, inc-skill, inc
level-up        Usage: level-up att1 att2 att3
                Level up your character by one level. Command arguments are the three,
                unique attributes that you want to increase during the leveling up.
                Alternative names: levelup, level, up
plan            Usage: plan att1 att2 [att3]
                Set a plan for current level. You can choose 2 or 3 attributes to plan
                a level (you should only choose 2 attributes if you plan to level-up
                Luck). If you have already set a plan, it will bereplaced.
save            Saves the character to a (pickle) file. A different file is created
                for each character level. If a file exists for a given level, it is
                overwriten.
quit            Quits this program. No changes are saved.
                Alternative names: exit
help            Shows this help

```
