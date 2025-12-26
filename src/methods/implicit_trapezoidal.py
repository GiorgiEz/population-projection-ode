import numpy as np


class TrapezoidalRK:
    def __init__(self, nonlinear_solver):
        self.solver = nonlinear_solver

    def step(self, model, t, y, dt):
        def G(y_next):
            return y_next - y - 0.5 * dt * (model.f(t, y) + model.f(t + dt, y_next))

        I = np.eye(len(y))
        def J(y_next):
            return I - 0.5 * dt * model.jacobian(t + dt, y_next)

        return self.solver.solve(G, J, y)
