# IPython Cell Functionizer
A cell magic that convert the cell into a function for code reuse.

# Use case
Imaging that you are working on some data processing project. You use the first cell to define the parameters:
```
a = 1
b = 2
...
```
The processing logics are written in the next cell
```
# process
result = (a**2 + b**2) ** 1/2
# visualize
...
```

Later you want to try a different set of parameters. You have to copy and paste the cells and make the little changes.
```
a = 2
b = 3
...
```
```
# process
result = (a**2 + b**2) ** 1/2
# visualize
...
```

If you want to modify the processing logics, you have to apply the change to all duplications. The straightforward 
solution is to wrapping the code in a function block
```
def process(a, b):
    result = (a**2 + b**2) ** 1/2
    # visualize
    ...
    return ...
a = 1
b = 2
result = process(a, b)
a = 2
b = 3
result = process(a, b)
```
Debugging a function is much more difficult than debugging the flat code in a cell because the function will scope 
the variables. Usually we write the cell. Test it. Then wrap it in a function. Later when something bad happens, we 
remove the function header and remove the indent. After fixing the error, wrap it as a function again. This tedious 
process can be automated by this magic.

# Usage
1. Load the extension
```
%load_ext functionizer
```
2. Write some codes
```
# parameter cell
last_name = "W"
first_name = "Y"
```

```
# processing cell
name = first_name + " " + last_name
name
```
3. Convert the processing cell with the magic. The first argument defines the function name. The `-a` defines the 
   list of the function arguments. The `-r` defines the return list.
```
%%functionize get_name -a first_name last_name -r name
name = first_name + " " + last_name
name
```

4. After this cell is executed, a function `get_name` is also defined that takes the arguments you defined and 
   return the variable you requested.
```
get_name("New name", "B")
```

# Arguments
## function name (required)
The name of the function to be defined in the global scope

## Return as dictionary `--as_dict`
The registered return values will be returned in a dictionary with their variable names as the keys

## Input arguments `-a, --args`
The variable names being injected as the arguments. Multiple arguments are separated by space. 

If the name contains assignment such as `-a some_variable="125"`, it will be injected as a keyword argument and 
being moved after the last positional argument. If the functionization cell is not `--skip`ped, this assignment will 
be implicitly executed first to save the explicit assignment in the other cells.

If the name ends with `!`, it will be expanded to the keyword argument using the variable of the same name in the 
global scope. For example, `-a hello!` will be expaneded to `-a hello=hello`. This allows quick reuse of the 
previously defined variables in the function's scope.

## Return arguments `-r, --ret`
The variable names being returned. Multiple return values are separated by space.

## Disable functionization `-d, --disable`
Do not create the function of the cell. Only execute the cell as-is. Note that the keyword argument assignment will 
still be effective in this mode to ensure the cell can execute consistently.

## Skip cell execution `--skip`
Do not run the cell but only create the function only.

## Drop the last line `--skip_last'
Drop the last non-blank line in the cell. This is useful the last line of the cell is an expression that outputs 
some information, and you do not want to keep it after functionization.

## Return last `--return_last`
Use the return value of the last non-blank line as the return value. This will override the return values defined by 
`-r, --ret`.



