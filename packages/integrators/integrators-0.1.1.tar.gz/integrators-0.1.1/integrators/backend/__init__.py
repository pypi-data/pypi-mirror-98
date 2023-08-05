# -*- coding: utf-8 -*-


import numpy.random
import numpy as np
from numba.extending import overload

__all__ = [
    # basic operations
    'normal',
    'shape',
    'exp',

    # methods
    'set_ops',
    'set_backend',
]

_backend = 'numpy'  # default backend is NumPy

normal = np.random.normal
shape = np.shape
reshape = np.reshape
exp = np.exp
sum = np.sum
zeros = np.zeros
# ones = np.ones
eye = np.eye
outer = np.outer
dot = np.dot


def set_ops(**kwargs):
    if 'normal' in kwargs:
        global normal
        normal = kwargs.pop('normal')

    if 'shape' in kwargs:
        global shape
        shape = kwargs.pop('shape')

    if 'reshape' in kwargs:
        global reshape
        reshape = kwargs.pop('reshape')

    if 'exp' in kwargs:
        global exp
        exp = kwargs.pop('exp')

    if 'sum' in kwargs:
        global sum
        sum = kwargs.pop('sum')

    # if 'ones' in kwargs:
    #     global ones
    #     ones = kwargs.pop('ones')

    if 'zeros' in kwargs:
        global zeros
        zeros = kwargs.pop('zeros')

    if 'eye' in kwargs:
        global eye
        eye = kwargs.pop('eye')

    if 'outer' in kwargs:
        global outer
        outer = kwargs.pop('outer')

    if 'dot' in kwargs:
        global dot
        dot = kwargs.pop('dot')

    if len(kwargs) > 0:
        raise ValueError(f"Unknown operators: {list(kwargs.keys())}")


# @overload(numpy.random.normal)
# def normal_func(loc, scale, size=None):
#     if (size is None) or len(size) == 0:
#         def normal_func(loc, scale, size):
#             return loc + scale * numpy.random.standard_normal()
#     else:
#         def normal_func(loc, scale, size):
#             return loc + scale * numpy.random.standard_normal(size)
#
#     return normal



# @overload(numpy.random.normal)
# def normal_func(size=None):
#     if (size is None) or len(size) == 0:
#         def normal_func(size):
#             return numpy.random.standard_normal()
#     else:
#         def normal_func(size):
#             return numpy.random.standard_normal(size)
#
#     return normal


def set_backend(backend):
    global _backend
    _backend = backend

    if backend == 'numpy':
        set_ops(normal=np.random.normal,
                shape=np.shape,
                exp=np.exp,
                sum=np.sum)

    elif backend == 'numba-gpu':
        pass

    elif backend == 'pytorch':
        pass

    elif backend == 'tensorflow':
        pass

    elif backend == 'jax':
        pass

    else:
        raise ValueError(f'Unknown backend: {backend}.')
