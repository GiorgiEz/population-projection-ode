import numpy as np
from scipy.optimize import least_squares
from src.model import PopulationFertilityModel
from src.parameters import ModelParameters
from src.ivp import InitialValueProblem
from src.simulation import solve_custom_ivp


class ParameterCalibrator:
    """ Estimate model parameters using multi-year population & fertility data."""

    def __init__(self, df, method, F_inf=1.4, dt=1):
        self.df = df
        self.method = method
        self.F_inf = F_inf
        self.dt = dt
        self.y0 = np.array([df.loc[0, "avg_population"], df.loc[0, "total_fertility_rate"]])
        self.T = df["year"].iloc[-1] - df["year"].iloc[0]

    def _unpack_theta(self, theta):
        b0, alpha, d, m, K, k = theta
        return ModelParameters(b0=b0, alpha=alpha, d=d, m=m, K=K, k=k, F_inf=self.F_inf)

    def _residuals(self, theta):
        params = self._unpack_theta(theta)
        model = PopulationFertilityModel(params)

        ivp = InitialValueProblem(model=model, t0=0, y0=self.y0, T=self.T, dt=self.dt)
        _, y = solve_custom_ivp(ivp, self.method)

        rN, rF = self.compute_residuals(y)

        return np.concatenate([rN, rF])

    def fit(self, theta0, bounds):
        result = least_squares(self._residuals, theta0, bounds=bounds)
        return self._unpack_theta(result.x), result

    def compute_residuals(self, y):
        N_model = y[:, 0]
        F_model = y[:, 1]

        N_data = self.df["avg_population"].values
        F_data = self.df["total_fertility_rate"].values

        rN = (N_model - N_data) / N_data
        rF = (F_model - F_data) / F_data

        return rN, rF
