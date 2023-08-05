# -*- coding: utf-8 -*-

from integrators import backend
from integrators import profile


__all__ = [
    'exponential_euler',
]


def exponential_euler(f):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def int_f(x, t, *args):
        df, linear_part, g = f(x, t, *args)
        dW = backend.normal(0., 1., backend.shape(x))
        dg = dt_sqrt * g * dW
        exp = backend.exp(linear_part * dt)
        y1 = x + (exp - 1) / linear_part * df + exp * dg
        return y1

    return int_f
