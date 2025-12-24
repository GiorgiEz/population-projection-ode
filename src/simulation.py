import numpy as np

def solve_custom_ivp(ivp, method):
    t = ivp.t0
    y = ivp.y0.copy()

    ts = [t]
    ys = [y.copy()]

    while t < ivp.T:
        y = method.step(ivp.model, t, y, ivp.dt)
        t += ivp.dt
        ts.append(t)
        ys.append(y.copy())

    return np.array(ts), np.array(ys)
