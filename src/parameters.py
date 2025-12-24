class ModelParameters:
    def __init__(self, b0, alpha, d, m, K, k, F_inf):
        """
        Parameters for the population–fertility ODE model.

        b0     : Baseline birth-rate coefficient (1 / year).
                 Scales the fertility-dependent birth rate b(F) = b0 * F^alpha.

        alpha  : Fertility elasticity exponent (dimensionless).
                 Controls how sensitively the birth rate responds to changes
                 in total fertility F.

        d      : Crude death rate (1 / year).
                 Per-capita mortality rate, assumed constant in time.

        m      : Net migration rate (1 / year).
                 Per-capita net migration (immigration minus emigration).

        K      : Carrying capacity (population units).
                 Environmental/socioeconomic limit that reduces effective
                 birth rates through the logistic factor (1 - N / K).

        k      : Fertility relaxation rate (1 / year).
                 Speed at which fertility F(t) converges toward its long-run
                 equilibrium value F_inf.

        F_inf  : Long-run (equilibrium) fertility level (dimensionless).
                 Asymptotic fertility rate in the absence of transient effects.
        """
        self.b0 = b0
        self.alpha = alpha
        self.d = d
        self.m = m
        self.K = K
        self.k = k
        self.F_inf = F_inf
