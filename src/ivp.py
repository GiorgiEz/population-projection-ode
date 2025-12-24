class InitialValueProblem:
    def __init__(self, model, t0, y0, T, dt):
        self.model = model
        self.t0 = t0
        self.y0 = y0
        self.T = T
        self.dt = dt
