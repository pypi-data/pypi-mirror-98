# -*- coding: utf-8 -*-

import math

from integrators import profile
from integrators import backend


__all__ = [
    'srk1_weak',
    'srk2_weak',

]



def srk1_weak(f=None, g=None, num_iter=None):
    """Order 2.0 weak SRK methods for Ito SDEs with multi-dimensional
    Wiener process.

    The Butcher table is:

    .. math::

    References
    ----------

    .. [1] Rößler, Andreas. "Strong and weak approximation methods for stochastic differential
            equations—some recent developments." Recent developments in applied probability and
            statistics. Physica-Verlag HD, 2010. 127-153.
    .. [2] Rößler, Andreas. "Runge–Kutta methods for the strong approximation of solutions of
            stochastic differential equations." SIAM Journal on Numerical Analysis 48.3
            (2010): 922-952.

    """
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def ito_wrapper(f, g, num_iter):
        def int_func(x, t, *args):
            g_t_H0s0 = g(x, t, *args)  # shape (d, m)
            d, m = backend.shape(g_t_H0s0)

            # single Ito integrals #
            # -------------------- #
            I1 = backend.normal(0., dt_sqrt, (m,))  # shape (m,)

            # double Ito integrals #
            # -------------------- #
            # I^{alpha,beta}(h_n), alpha,beta = 0, 1, …, m-1
            h = (2.0 / dt) ** 0.5
            A = backend.zeros(shape=(m, m))
            for k in range(1, num_iter + 1):
                X = backend.normal(loc=0.0, scale=1.0, size=m)
                Y = backend.normal(loc=0.0, scale=1.0, size=m) + h * I1
                A += (backend.outer(X, Y) - backend.outer(Y, X)) / k
            A *= 0.5 * dt / math.pi
            I2 = 0.5 * (backend.outer(I1, I1) - dt * backend.eye(m)) + A  # shape (m, m)

            # numerical integration #
            # --------------------- #
            f_t_H0s1 = f(x, t, *args)  # shape (d,)
            s2_H0 = x + f_t_H0s1 * dt  # shape (d,)
            f_t_H0s2 = f(s2_H0, t + dt, *args)  # shape (d,)
            g_t_all_k = backend.dot(g_t_H0s0, I2) / dt_sqrt  # shape (d, m)
            prefix = backend.reshape(s2_H0, backend.shape(s2_H0) + (1,))
            s2_H_all = prefix + g_t_all_k  # shape (d, m)
            s3_H_all = prefix - g_t_all_k  # shape (d, m)

            y = x + 0.5 * dt * (f_t_H0s1 + f_t_H0s2)
            y += backend.dot(g_t_H0s0, I1)
            for k in range(m):
                y += 0.5 * dt_sqrt * g(s2_H_all[:, k], t + dt, *args)[:, k]
                y -= 0.5 * dt_sqrt * g(s3_H_all[:, k], t + dt, *args)[:, k]
            return y

        return int_func


def srk2_weak(f=None, g=None, num_iter=None):
    pass

