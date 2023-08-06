from numbers import Number
from statistics import geometric_mean, mean, median
from typing import Iterable, Tuple


def _step(nums: Iterable[Number]) -> Tuple[float]:
    return (mean(nums), geometric_mean(nums), median(nums))


def geothmetic_meandian(nums: Iterable[Number], error: float = 0.001) -> float:
    while max(nums) - min(nums) > error:
        nums = _step(nums)
    return median(nums)
