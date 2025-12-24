from src.model import PopulationFertilityModel
from src.parameters import ModelParameters
from src.ivp import InitialValueProblem
from src.methods.implicit_euler import ImplicitEuler
from src.methods.implicit_rk import TrapezoidalRK
from src.solvers.newton import NewtonSolver
from src.simulation import solve_custom_ivp
import numpy as np
import pandas as pd



if __name__ == '__main__':
    """
    Step 1: Define model parameters (birth rate, death rate, migration, carrying capacity, fertility dynamics, etc.)
    """
    params = ModelParameters()

    """
    Step 2: Create the population–fertility ODE model. This defines the system y'(t) = f(t, y)
    """
    model = PopulationFertilityModel(params)

    """
    Step 3: Define the initial condition for the IVP
    y0 = [N0, F0]. N0 = initial population size. F0 = initial fertility rate.
    - t0 : start time (years)
    - T  : final time (years)
    - dt : time step
    """
    # Load population data
    df = pd.read_csv("data/population_data.csv")

    df = df[["year", "avg_population", "total_fertility_rate"]]  # keep only what we need
    df = df.sort_values("year").reset_index(drop=True)  # ensure sorted by year

    # Extract time span
    year_start = int(df.loc[0, "year"])
    year_end = int(df.loc[df.index[-1], "year"])

    T = year_end - year_start

    # Initial conditions
    N0 = float(str(df.loc[0, "avg_population"]).replace(",", ""))
    F0 = float(str(df.loc[0, "total_fertility_rate"]))

    y0 = np.array([N0, F0])
    ivp = InitialValueProblem(model=model, t0=0, y0=y0, T=T, dt=1)

    """
    Step 4:
    Create a nonlinear solver. Newton's method will be used to solve the implicit equations at each time step
    """
    newton = NewtonSolver()

    """
    Step 5:
    Define the first numerical method: Implicit Euler using Newton iterations.
    Define the second numerical method: Implicit Runge–Kutta (DIRK) using Newton iterations
    """
    euler = ImplicitEuler(newton)
    rk = TrapezoidalRK(newton)

    """
    Step 6: 
    Solve the IVP using Implicit Euler.
    Solve the IVP using Implicit Runge–Kutta
    """
    t1, y1 = solve_custom_ivp(ivp, euler)
    t2, y2 = solve_custom_ivp(ivp, rk)

    """
    Step 7:
    Print final values to compare the two methods
    """
    print("\nFinal results (t = {:.1f} years):".format(ivp.T))
    print("\nImplicit Euler:")
    print(f"  Population N = {y1[-1, 0]:.2f}")
    print(f"  Fertility  F = {y1[-1, 1]:.4f}")

    print("\nImplicit Runge–Kutta:")
    print(f"  Population N = {y2[-1, 0]:.2f}")
    print(f"  Fertility  F = {y2[-1, 1]:.4f}")

    """
    Step 8:
    Print absolute differences between the methods
    """
    diff_N = abs(y1[-1, 0] - y2[-1, 0])
    diff_F = abs(y1[-1, 1] - y2[-1, 1])

    print("\nAbsolute difference (Euler vs RK):")
    print(f"  |ΔN| = {diff_N:.2f}")
    print(f"  |ΔF| = {diff_F:.6f}")
