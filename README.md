**scriptable** allows you to call python function from bash. It wires standard input to the function's argument, and prints it's output to stdout.

This allows your python functions to become first class citizens in a bash command line, participating in pipes like regular unix programs.

## Example

Pick a random file from the current directory

    ls -1 | ./scriptable.py random.choice

What **scriptable** does is turn standard input into an array of strings, pass that to the function, and print it's output.

## Use Case

Say you have a script called *pkg* that does something like this:

    data = load_data()
    munged = munge_data(data)
    output(munged)

All of a sudden you learn that you can't load the data yourself, it's going to come from an external program called `data_provider`. No problem, at the bash command line you just do:

    data_provider | scriptable.py pkg.munge_data | scriptable pkg.output

## Details

Not all functions are suitable for this type of pipeling.

First *your function must be a true function*, meaning it's output should be purely a function of it's input - no global variables, no output to the console, etc.

Second, *the function must accept as first argument an iterable of strings*, or nothing. If there are further arguments they must all be strings, and you give them on the command line like in this example.

For this function: `def myfunc(iterable, name)`
Use this: `./scriptable mypackage.myfunc Bob`

**scriptable** must be able to find and import your package. If that is failing, try importing it from python shell.

The function does not need to return a value. If it does return a value, it will be converted to unicode and printed to stdout. If the return value is an iterable (but not a string), the contents will be converted to unicode and printed one per line, allowing the pipeline to continue.

