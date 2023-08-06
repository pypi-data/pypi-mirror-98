from pandas import Series
import numpy as np

class Profit:
    @staticmethod
    def get(series: Series) -> np.float64:
        series += 1
        return series.prod() - 1

    @staticmethod
    def get_cum_prod(series: Series) -> Series:
        series += 1
        return series.cumprod() - 1

