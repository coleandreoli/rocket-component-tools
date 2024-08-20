import numpy as np


class Nose:
    """Generates line for nose cones

    x = np.ndarray
    radius = Radius
    length = Length

    C = Von Karman constant (0, 1/3, 2/3)
    K = Parabolic constant
    n = Power constant
    """
    @staticmethod
    def parabolic_function(x: np.ndarray, radius, length, K) -> np.ndarray:
        # parabolic nose cone function
        return radius * (2 * (x / length) - K * (x / length) ** 2) / (2 - K)
    @staticmethod
    def power_function(x: np.ndarray, radius, length, n) -> np.ndarray:
        return radius * (x / length) ** n
    @staticmethod
    # LD-Haack (Von Karman) (C=0), LV-Haack (C=1/3), Tangent (C=2/3)
    def von_karman_function(x: np.ndarray, radius, length, C) -> np.ndarray:
        theta = np.arccos(1 - (2 * x / length))
        return (radius / np.sqrt(np.pi)) * np.sqrt(theta - np.sin(2 * theta) / 2) + (C * np.sin(theta) ** 3)
