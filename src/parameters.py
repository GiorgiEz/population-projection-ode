class ModelParameters:
    def __init__(self):
        self.d = 0.02185
        self.m = 0.0047
        self.alpha = 0.6

        b_obs = 492_574 / 15_514_255
        self.b0 = b_obs / (4.93 ** self.alpha)

        self.F_inf = 1.4
        self.k = 0.05

        r_obs = 0.0146
        self.K = 15_514_255 / (1 - (r_obs + self.d - self.m) / b_obs)
