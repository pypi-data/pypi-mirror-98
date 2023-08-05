# -*- coding: utf-8 -*-

import math

from integrators import backend
from integrators import profile

__all__ = [
    'euler',
    'milstein',
    'srk1_strong',
    'srk2_strong',
]


def euler(f=None, g=None, scalar_wiener=None, schema=None):
    """
    only valid for Ito SDEs

    This method has have strong orders :math:`(p_d, p_s) = (1.0, 0.5)`.

    """
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def ito_scalar_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            dfdt = f_df(x, t, *args)[0] * dt
            dg = f_dg(x, t, *args)
            dW = backend.normal(0., dt_sqrt, backend.shape(dg))
            dgdW = dg * dW
            return x + dfdt + dgdW

        return int_func

    def ito_vector_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            dfdt = f_df(x, t, *args) * dt
            dg = f_dg(x, t, *args)
            dW = backend.normal(0., dt_sqrt, backend.shape(dg))
            dgdt = backend.sum(dg * dW, axis=-1)
            return x + dfdt + dgdt

        return int_func

    def stra_scalar_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            dfdt = f_df(x, t, *args) * dt
            dg = f_dg(x, t, *args)
            dW = backend.normal(0., dt_sqrt, backend.shape(dg))
            y_bar = x + dg * dW
            dg_bar = f_df(y_bar, t, *args)
            dgdW = 0.5 * (dg + dg_bar) * dW
            y = x + dfdt + dgdW
            return y

        return int_func

    def stra_vector_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            dfdt = f_df(x, t, *args) * dt
            dg = f_dg(x, t, *args)
            dW = backend.normal(0., dt_sqrt, backend.shape(dg))
            y_bar = x + backend.sum(dg * dW, axis=-1)
            dg_bar = f_dg(y_bar, t, *args)
            dgdW = 0.5 * backend.sum((dg + dg_bar) * dW, axis=-1)
            return x + dfdt + dgdW

        return int_func

    if (scalar_wiener is None) and (f is None) and (g is None):
        raise ValueError('Must provide "f" or "g" or "scalar" setting.')

    # scalar Wiener process #
    # --------------------- #
    elif (scalar_wiener is True) or (scalar_wiener is None):
        if f is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda f: ito_scalar_wrapper(f, g)

        elif g is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda g: ito_scalar_wrapper(f, g)

        else:
            assert f is not None
            assert g is not None
            return ito_scalar_wrapper(f, g)

    # vector Wiener process #
    # --------------------- #
    else:
        if f is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda f: ito_vector_wrapper(f, g)

        elif g is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda g: ito_vector_wrapper(f, g)

        else:
            return ito_vector_wrapper(f, g)


def milstein(f=None, g=None, scalar_wiener=None, schema=None):
    dt = profile.get_dt()
    dt_sqrt = dt ** 0.5

    def ito_scalar_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            df = f_df(x, t, *args)
            dg = f_dg(x, t, *args)
            dfdt = df * dt
            dW = backend.normal(0., 1., backend.shape(dg))
            dgdW = dg * dW * dt_sqrt
            df_bar = x + dfdt + dg * dt_sqrt
            dg_bar = f_dg(df_bar, t, *args)
            extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt - dt_sqrt)
            return x + dfdt + dgdW + extra_term

        return int_func

    def ito_vector_wrapper(f_df, f_dg):
        def int_func(x, t, *args):
            df = f_df(x, t, *args)
            dg = backend.sum(f_dg(x, t, *args), axis=-1)
            dW = backend.normal(0., 1., backend.shape(dg))
            dfdt = df * dt
            df_bar = x + dfdt + backend.sum(dg * dt_sqrt, axis=-1)
            dg_bar = f_dg(df_bar, t, *args)
            extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt - dt_sqrt)
            dgdW = dg * dW * dt_sqrt
            return x + dfdt + backend.sum(dgdW + extra_term, axis=-1)

        return int_func

    def stra_scalar_wrapper(f, g):
        def int_func(y0, t, *args):
            df = f(y0, t, *args)
            dg = g(y0, t, *args)
            dW = backend.normal(0., 1., backend.shape(dg))
            dfdt = df * dt
            dgdW = dg * dW * dt_sqrt
            df_bar = y0 + dfdt + dg * dt_sqrt
            dg_bar = g(df_bar, t, *args)
            extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt)
            return y0 + dfdt + dgdW + extra_term

        return int_func

    def stra_vector_wrapper(f, g):
        def int_func(y0, t, *args):
            df = f(y0, t, *args)
            dg = backend.sum(g(y0, t, *args), axis=-1)
            dW = backend.normal(0., 1., backend.shape(dg))
            dfdt = df * dt
            dgdW = dg * dW * dt_sqrt
            df_bar = y0 + dfdt + backend.sum(dg * dt_sqrt, axis=-1)
            dg_bar = g(df_bar, t, *args)
            extra_term = 0.5 * (dg_bar - dg) * (dW * dW * dt_sqrt)
            return y0 + dfdt + backend.sum(dgdW + extra_term, axis=-1)

        return int_func

    if (scalar_wiener is None) and (f is None) and (g is None):
        raise ValueError('Must provide "f" or "g" or "scalar" setting.')

    # scalar Wiener process #
    # --------------------- #
    elif (scalar_wiener is True) or (scalar_wiener is None):
        if f is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda f: ito_scalar_wrapper(f, g)

        elif g is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda g: ito_scalar_wrapper(f, g)

        else:
            assert f is not None
            assert g is not None
            return ito_scalar_wrapper(f, g)

    # vector Wiener process #
    # --------------------- #
    else:
        if f is None:
            assert f is not None, '"f" and "g" cannot be both None.'
            return lambda f: ito_vector_wrapper(f, g)

        elif g is None:
            assert g is not None, '"f" and "g" cannot be both None.'
            return lambda g: ito_vector_wrapper(f, g)

        else:
            return ito_vector_wrapper(f, g)


def srk1_strong(f=None, g=None, num_iter=None, schema=None):
    """Order 1.0 strong SRK methods for Ito SDEs with multi-dimensional Wiener process.

    The Butcher table is:

    .. math::

        \\begin{array}{c|ccc|ccc|ccc|}
            0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            \\hline 0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 1 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & -1 & 0 & 0 & & \\\\
            \\hline & 1 & 0 & 0 & 1 & 0 & 0 & 0 & 1 / 2 & -1 / 2
        \\end{array}

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
            g_t_x = g(x, t, *args)
            noise_shape = backend.shape(g_t_x)
            d, m = backend.shape(g_t_x)

            # single Ito integrals #
            # -------------------- #
            I1 = backend.normal(0., dt_sqrt, noise_shape)

            # double Ito integrals #
            # -------------------- #
            # I^{alpha,beta}(h_n), alpha,beta = 1, 2, …, m
            h = (2.0 / dt) ** 0.5
            A = backend.zeros(shape=(m, m))
            for k in range(1, num_iter + 1):
                X = backend.normal(loc=0.0, scale=1.0, size=m)
                Y = backend.normal(loc=0.0, scale=1.0, size=m) + h * I1
                A += (backend.outer(X, Y) - backend.outer(Y, X)) / k
            A *= (0.5 * dt / math.pi)
            I2 = 0.5 * (backend.outer(I1, I1) - dt * backend.eye(m)) + A

            # numerical integration #
            # --------------------- #

            g_t_H1_k = backend.dot(g_t_x, I2) / dt_sqrt  # shape (d, m)
            prefix = backend.reshape(x, backend.shape(x) + (1,))
            H2 = prefix + g_t_H1_k  # shape (d, m)
            H3 = prefix - g_t_H1_k  # shape (d, m)

            y = x + f(x, t, *args) + backend.dot(g_t_x, I1)  # shape (d, )
            for k in range(m):
                y += 0.5 * dt_sqrt * g(H2[:, k], t, *args)[:, k]
                y -= 0.5 * dt_sqrt * g(H3[:, k], t, *args)[:, k]

        return int_func

    def stra_wrapper(f, g, num_iter):
        def int_func(x, t, *args):
            g_t_x = g(x, t, *args)
            noise_shape = backend.shape(g_t_x)
            d, m = backend.shape(g_t_x)

            # single Ito integrals #
            # -------------------- #
            I1 = backend.normal(0., dt_sqrt, noise_shape)

            # double Ito integrals #
            # -------------------- #
            # I^{alpha,beta}(h_n), alpha,beta = 1, 2, …, m
            h = (2.0 / dt) ** 0.5
            A = backend.zeros(shape=(m, m))
            for k in range(1, num_iter + 1):
                X = backend.normal(loc=0.0, scale=1.0, size=m)
                Y = backend.normal(loc=0.0, scale=1.0, size=m) + h * I1
                A += (backend.outer(X, Y) - backend.outer(Y, X)) / k
            A *= (0.5 * dt / math.pi)
            I2 = 0.5 * backend.outer(I1, I1) + A

            # numerical integration #
            # --------------------- #

            g_t_H1_k = backend.dot(g_t_x, I2) / dt_sqrt  # shape (d, m)
            prefix = backend.reshape(x, backend.shape(x) + (1,))
            H2 = prefix + g_t_H1_k  # shape (d, m)
            H3 = prefix - g_t_H1_k  # shape (d, m)

            y = x + f(x, t, *args) + backend.dot(g_t_x, I1)  # shape (d, )
            for k in range(m):
                y += 0.5 * dt_sqrt * g(H2[:, k], t, *args)[:, k]
                y -= 0.5 * dt_sqrt * g(H3[:, k], t, *args)[:, k]

        return int_func

    num_iter = 10 if num_iter is None else num_iter


def srk2_strong(f=None, g=None, num_iter=None, schema=None):
    """Order 1.0 strong SRK methods for Ito SDEs with multi-dimensional Wiener process.

    The Butcher table is:

    .. math::

        \\begin{array}{c|ccc|ccc|ccc|}
            0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            \\hline 0 & 0 & 0 & 0 & 0 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & 1 & 0 & 0 & & \\\\
            0 & 0 & 0 & 0 & -1 & 0 & 0 & & \\\\
            \\hline & 1 & 0 & 0 & 1 & 0 & 0 & 0 & 1 / 2 & -1 / 2
        \\end{array}

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

    def stra_wrapper(f, g, num_iter):
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
            I2 = 0.5 * backend.outer(I1, I1) + A  # shape (m, m)

            # numerical integration #
            # --------------------- #
            f_t_H0s1 = f(x, t, *args)  # shape (d,)
            s2_H0 = x + f_t_H0s1 * dt  # shape (d,)
            f_t_H0s2 = f(s2_H0, t + dt, *args)  # shape (d,)
            g_t_all_k = backend.dot(g_t_H0s0, I2) / dt_sqrt  # shape (d, m)
            prefix = backend.reshape(s2_H0, (d, 1))
            s2_H_all = prefix + g_t_all_k  # shape (d, m)
            s3_H_all = prefix - g_t_all_k  # shape (d, m)

            y = x + 0.5 * dt * (f_t_H0s1 + f_t_H0s2)
            y += backend.dot(g_t_H0s0, I1)
            for k in range(m):
                y += 0.5 * dt_sqrt * g(s2_H_all[:, k], t + dt)[:, k]
                y -= 0.5 * dt_sqrt * g(s3_H_all[:, k], t + dt)[:, k]
            return y

        return int_func

    num_iter = 10 if num_iter is None else num_iter
