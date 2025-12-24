import matplotlib.pyplot as plt


class Visualizations:
    def __init__(self, df, y_e, y_rk):
        self.df = df
        self.y_e = y_e
        self.y_rk = y_rk
        self.years = self.df["year"].values

    def actual_vs_modeled_population(self):
        # Population plot
        N_data = self.df["avg_population"].values
        N_euler = self.y_e[:, 0]
        N_rk = self.y_rk[:, 0]

        plt.figure(figsize=(9, 5))
        plt.plot(self.years, N_data, "k--", linewidth=2, label="Observed population")
        plt.plot(self.years, N_euler, label="Implicit Euler")
        plt.plot(self.years, N_rk, label="Implicit RK (Trapezoidal)")

        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.title("United Kingdom population: model vs data (1839–2023)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def actual_vs_modeled_fertility(self):
        # Fertility plot
        F_data = self.df["total_fertility_rate"].values
        F_euler = self.y_e[:, 1]
        F_rk = self.y_rk[:, 1]

        plt.figure(figsize=(9, 5))
        plt.plot(self.years, F_data, "k--", linewidth=2, label="Observed fertility")
        plt.plot(self.years, F_euler, label="Implicit Euler")
        plt.plot(self.years, F_rk, label="Implicit RK (Trapezoidal)")

        plt.xlabel("Year")
        plt.ylabel("Total fertility rate")
        plt.title("United Kingdom fertility rate: model vs data (1839–2023)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def main(self):
        self.actual_vs_modeled_population()
        self.actual_vs_modeled_fertility()
