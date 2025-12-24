import numpy as np


class ImplicitEuler:
    def __init__(self, nonlinear_solver):
        self.solver = nonlinear_solver

    def step(self, model, t, y, dt):
        def G(y_next):
            return y_next - y - dt * model.f(t + dt, y_next)

        I = np.eye(len(y))
        def J(y_next):
            return I - dt * model.jacobian(t + dt, y_next)

        # explicit Euler predictor
        y0 = y + dt * model.f(t, y)
        return self.solver.solve(G, J, y0)
