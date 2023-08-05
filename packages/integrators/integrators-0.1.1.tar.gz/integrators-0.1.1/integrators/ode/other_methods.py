# -*- coding: utf-8 -*-

from integrators import profile
from integrators import backend

__all__ = [
    'exponential_euler',
]


def exponential_euler(f):
    dt = profile.get_dt()

    def int_f(x, t, *args):
        df, linear_part = f(x, t, *args)
        y = x + (backend.exp(linear_part * dt) - 1) / linear_part * df
        return y

    return int_f
