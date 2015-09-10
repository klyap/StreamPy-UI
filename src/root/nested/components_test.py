'''
This module holds all the basic Python functions that
each component represents.

'''

from random import randint

from Stream import _no_value


'''
generate_of_random_integers() generates
a random integer

Parameters
----------
f_args : tuple
    First element is the maximum integer generated

Returns
-------
randint(0, max_integer) : int
    Integer between 0 and 'max_integer'
'''


def generate_of_random_integers(f_args=(100,)):
    max_integer = f_args[0]
    return randint(0, max_integer)


'''
print_value() prints out to console the value it was passed.

Parameters
----------
v : any
    Value to be printed

index : int
    Index of the value in the stream

Returns
-------
index + 1 : int
    Index of next element to be printed

'''


def print_value(v, index):
        print '[', index, '] = ', v
        return (index+1)


'''
split_into_even_off() returns an even number as the
second value in a 2-element list, where the first value
is '_no_value_' (vice versa for odd numbers).

Parameters
----------
m : int/float
    Number, potentially from a stream

Returns
-------
[_no_value, m] or [m, _no_value] : list
    m is sorted into the 1st or 2nd element
    of the list based on its parity

'''


def split_into_even_odd(m):
    if m % 2:
        return [_no_value, m]
    else:
        return [m, _no_value]


'''
split() returns the input number as the
second value in a 2-element list, where the first value
is '_no_value_' based on whether it's a multiple
of the argument parameter

Parameters
----------
m : int/float
    Number, potentially from a stream

f_args : list
    List where 1st element is a number that you're
    comparing 'm' to
Returns
-------
[_no_value, m] or [m, _no_value] : list
    m is sorted into the 1st or 2nd element
    of the list

'''


def split(m, f_args):
    divisor = f_args[0]
    return [_no_value, m] if m % divisor else [m, _no_value]


'''
multiply_elements() returns the product of
2 numbers

Parameters
----------
v : int/float
    Number, potentially from a stream

f_args : list
    First element is another number.
    Constant parameter.

Returns
-------
multiplier * v : list
    Product

'''


def multiply_elements(v, f_args):
    multiplier = f_args[0]
    return multiplier * v
