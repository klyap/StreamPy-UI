
from random import randint
from functools import partial

from Stream import Stream
from Stream import _no_value
from OperatorsTest import stream_func, stream_agent
from Stream import Stream, _no_value
from Agent import *

## Basic Py functions/components

# Prints stream for debugger animation
def print_value(v, index):
        print '[' , index , '] = ', v
        return (index+1)
        
# Makes a stream of rand ints
def generate_of_random_integers(f_args = (100,)):
    max_integer = f_args[0]
    return randint(0, max_integer)

# Split into even odd streams
def split_into_even_odd(m):
    if m%2:
        return [_no_value, m]
    else:
        return [m, _no_value]

# Sorts input stream m into 2 streams based on
# whether it's a multiple of the argument parameter
def split(m, f_args):
    divisor = f_args[0]
    return [_no_value, m] if m%divisor else [m, _no_value]

# Multiply each element by a multiplier parameter
def multiply_elements(v, f_args):
    multiplier = f_args[0]
    return multiplier*v



