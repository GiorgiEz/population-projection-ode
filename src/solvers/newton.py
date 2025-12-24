import numpy as np

class NewtonSolver:
    def solve(self, G, J, y0, tol=1e-8, max_iter=20):
        y = y0.copy()
        for _ in range(max_iter):
            delta = np.linalg.solve(J(y), -G(y))
            y += delta
            if np.linalg.norm(delta) < tol:
                break
        return y
