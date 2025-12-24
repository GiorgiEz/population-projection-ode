import numpy as np
import matplotlib.pyplot as plt


class ProjectionVisualizations:
    def __init__(self, df, y_e, y_rk, start_year, end_year):
        self.df = df
        self.y_e_proj = y_e
        self.y_rk_proj = y_rk
        self.start_year = start_year
        self.end_year = end_year
        self.years = np.arange(start_year, end_year+1)

    def population_plot(self):
        # Population plot
        N_euler = self.y_e_proj[:, 0]
        N_rk = self.y_rk_proj[:, 0]

        plt.figure(figsize=(9, 5))
        plt.plot(self.years, N_euler, label="Implicit Euler")
        plt.plot(self.years, N_rk, label="Implicit RK (Trapezoidal)")

        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.title(f"United Kingdom population (based on birth and death rates): ({self.start_year}-{self.end_year})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(
            "src/visualization/plots/population_projection.png",
            dpi=300,
            bbox_inches="tight"
        )
        plt.show()

    def fertility_plot(self):
        F_euler = self.y_e_proj[:, 1]
        F_rk = self.y_rk_proj[:, 1]

        plt.figure(figsize=(9, 5))
        plt.plot(self.years, F_euler, label="Euler fertility")
        plt.plot(self.years, F_rk, label="RK fertility")

        plt.xlabel("Year")
        plt.ylabel("Total fertility rate")
        plt.title(f"Fertility projection ({self.start_year}-{self.end_year})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(
            "src/visualization/plots/fertility_projection.png",
            dpi=300,
            bbox_inches="tight"
        )
        plt.show()

    def main(self):
        self.population_plot()
        self.fertility_plot()
