import numpy as np


class Nose:
    """
    Nose cone class.

    x = np.linspace(0, Length, itr)
    R = Radius
    L = Length

    C = Von Karman constant (0, 1/3, 2/3)
    K = Parabolic constant
    n = Power constant
    """
    # parabolic nose cone function
    def parabolic_function(x, R, L, K):
        return R * (2 * (x / L) - K * (x / L) ** 2) / (2 - K)

    def power_function(x, R, L, n):
        return R * (x / L) ** n

    # # LD-Haack (Von Karman) (C=0), LV-Haack (C=1/3), Tangent (C=2/3)
    # def von_karman_function(x, R, L, C=0):
    #     theta = math.acos(1 - (2 * x / L))
    #     y = (R / math.sqrt(math.pi)) * math.sqrt(theta - math.sin(2 * theta) / 2) + (C * math.sin(theta) ** 3)
    #     return y

    # LD-Haack (Von Karman) (C=0), LV-Haack (C=1/3), Tangent (C=2/3)
    def von_karman_function(x, R, L, C):
        theta = np.arccos(1 - (2 * x / L))
        return (R / np.sqrt(np.pi)) * np.sqrt(theta - np.sin(2 * theta) / 2) + (C * np.sin(theta) ** 3)
