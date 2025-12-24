import numpy as np


class PopulationFertilityModel:
    def __init__(self, params):
        self.p = params

    def birth_rate(self, F):
        """
        b(F) = b0 * F^alpha
        """
        return self.p.b0 * F**self.p.alpha

    def f(self, t, y):
        """
        Right-hand side f(t, y)
        y = [N, F]
        """
        N, F = y

        bF = self.birth_rate(F)

        dNdt = (bF - self.p.d + self.p.m) * N * (1.0 - N / self.p.K)
        dFdt = -self.p.k * (F - self.p.F_inf)

        return np.array([dNdt, dFdt])

    def jacobian(self, t, y):
        """
        Jacobian matrix df/dy for Newton iterations
        """
        N, F = y
        bF = self.birth_rate(F)

        # partial derivatives
        dfdN = (bF - self.p.d + self.p.m) * (1 - 2 * N / self.p.K)
        dbdF = self.p.b0 * self.p.alpha * F**(self.p.alpha - 1)
        dfdF = dbdF * N * (1 - N / self.p.K)

        dgdF = -self.p.k

        return np.array([
            [dfdN, dfdF],
            [0.0,  dgdF]
        ])
