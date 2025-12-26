import numpy as np

class NewtonSolver:
    def gauss_seidel_solve(self, A, b, tol=1e-8, max_iter=100):
        n = len(b)
        x = np.zeros(n)

        for _ in range(max_iter):
            x_old = x.copy()

            for i in range(n):
                sigma = 0.0
                for j in range(n):
                    if j != i:
                        sigma += A[i, j] * x[j]

                x[i] = (b[i] - sigma) / A[i, i]

            if np.linalg.norm(x - x_old) < tol:
                break

        return x

    def solve(self, G, J, y0, tol=1e-8, max_iter=20):
        y = y0.copy()
        for _ in range(max_iter):
            delta = self.gauss_seidel_solve(J(y), -G(y))
            y += delta
            if np.linalg.norm(delta) < tol:
                break
        return y
