from src.model import PopulationFertilityModel
from src.ivp import InitialValueProblem
from src.methods.implicit_euler import ImplicitEuler
from src.methods.implicit_trapezoidal import TrapezoidalRK
from src.solvers.newton import NewtonSolver
from src.simulation import solve_custom_ivp
from src.calibrator import ParameterCalibrator
from src.visualization.Visualizations import Visualizations
from src.visualization.ProjectionVisualizations import ProjectionVisualizations
import numpy as np
import pandas as pd



if __name__ == '__main__':
    """
    Step 1: Loading data and calibrating the parameters based on all the available data
    """
    df = pd.read_csv("data/population_data.csv")
    df = df[["year", "avg_population", "total_fertility_rate"]]
    df = df.sort_values("year").reset_index(drop=True)

    df["avg_population"] = (df["avg_population"].astype(str).str.replace(",", "").astype(float))

    newton = NewtonSolver()

    calibrator = ParameterCalibrator(df=df,method=TrapezoidalRK(newton),F_inf=1.4,dt=1)
    theta0 = [0.02, 0.6, 0.02, 0.004, 5e7, 0.05]
    bounds = ([0, 0, 0, 0, 1e6, 0], [1, 2, 0.1, 0.1, 2e8, 1])
    params_opt, opt_info = calibrator.fit(theta0, bounds)

    """
    Step 2: Create the population–fertility ODE model. This defines the system y'(t) = f(t, y)
    Define the initial condition for the IVP
    y0 = [N0, F0]. N0 = initial population size. F0 = initial fertility rate.
    - t0 : start time (years)
    - T  : final time (years)
    - dt : time step
    """
    model = PopulationFertilityModel(params_opt)

    y0 = np.array([df.loc[0, "avg_population"], df.loc[0, "total_fertility_rate"]])
    T = df["year"].iloc[-1] - df["year"].iloc[0]

    ivp = InitialValueProblem(model=model, t0=0, y0=y0, T=T, dt=1)

    """
    Step 3:
    Define the first numerical method: Implicit Euler using Newton iterations.
    Define the second numerical method: Implicit Runge–Kutta (DIRK) using Newton iterations
    """
    euler = ImplicitEuler(newton)
    rk = TrapezoidalRK(newton)

    """ Step 4: Solve the IVP using Implicit Euler. Solve the IVP using Implicit Trapezoidal Runge–Kutta """
    t_e, y_e = solve_custom_ivp(ivp, euler)
    t_rk, y_rk = solve_custom_ivp(ivp, rk)

    """ Step 5: Visualize final values to compare the two methods"""
    visualizations = Visualizations(df, y_e, y_rk)
    visualizations.main()

    rN_euler, rF_euler = calibrator.compute_residuals(y_e)
    rN_rk, rF_rk = calibrator.compute_residuals(y_rk)

    rmse_N_euler = np.sqrt(np.mean(rN_euler ** 2))
    rmse_F_euler = np.sqrt(np.mean(rF_euler ** 2))

    rmse_N_rk = np.sqrt(np.mean(rN_rk ** 2))
    rmse_F_rk = np.sqrt(np.mean(rF_rk ** 2))

    print("\nTrajectory RMSE (relative):")
    print(f"Implicit Euler  - Population RMSE: {rmse_N_euler:.4e}")
    print(f"Implicit Euler  - Fertility  RMSE: {rmse_F_euler:.4e}")
    print(f"Trapezoidal RK - Population RMSE: {rmse_N_rk:.4e}")
    print(f"Trapezoidal RK - Fertility  RMSE: {rmse_F_rk:.4e}")

    """ Step 6: Let model run to some year in the future to conduct a scenario """
    start_year, end_year = 2023, 2050
    start_year_i = -1 - (2023 - start_year)
    y0_proj = np.array([df.loc[df.index[start_year_i], "avg_population"],
                        df.loc[df.index[start_year_i], "total_fertility_rate"]])

    ivp_proj = InitialValueProblem(model=model,t0=0,y0=y0_proj,T=end_year - start_year,dt=1)

    t_e_proj, y_e_proj = solve_custom_ivp(ivp_proj, euler)
    t_rk_proj, y_rk_proj = solve_custom_ivp(ivp_proj, rk)

    proj_visualizations = ProjectionVisualizations(df, y_e_proj, y_rk_proj, start_year, end_year)
    proj_visualizations.main()
