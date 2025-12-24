import numpy as np


class PopulationFertilityModel:
    def __init__(self, params):
        self.p = params

    def birth_rate(self, F):
        """ b(F) = b0 * F^alpha """
        return self.p.b0 * F**self.p.alpha

    def f(self, t, y):
        """ Right-hand side f(t, y). y = [N, F] """
        N, F = y

        bF = self.birth_rate(F)
        dNdt = (
                bF * N * (1 - N / self.p.K)
                - self.p.d * N
                + N * self.p.m
        )
        dFdt = -self.p.k * (F - self.p.F_inf)

        return np.array([dNdt, dFdt])

    def jacobian(self, t, y):
        N, F = y

        bF = self.birth_rate(F)
        dbdF = self.p.b0 * self.p.alpha * F ** (self.p.alpha - 1)

        dfdN = bF * (1 - 2 * N / self.p.K) - self.p.d + self.p.m
        dfdF = dbdF * N * (1 - N / self.p.K)

        dgdF = -self.p.k

        return np.array([
            [dfdN, dfdF],
            [0.0, dgdF]
        ])
