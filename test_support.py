"""Test functions to support scriptable unit tests.
"""

def echo(arr):
    return arr

NO_ARGS_OUTPUT = ['No', 'Arguments', 'Thanks']
def no_args():
    return NO_ARGS_OUTPUT

def first_of_array(arr):
    return arr[0]

def return_int(arr):
    return 42
