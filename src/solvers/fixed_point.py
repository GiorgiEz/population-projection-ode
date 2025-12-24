class FixedPointSolver:
    def solve(self, phi, y0, tol=1e-8, max_iter=50):
        y = y0.copy()
        for _ in range(max_iter):
            y_new = phi(y)
            if np.linalg.norm(y_new - y) < tol:
                break
            y = y_new
        return y
