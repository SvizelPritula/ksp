from typing import Callable, List, Tuple
from bisect import bisect_right


def keyframes(keyframes: List[Tuple[float, float]]) -> Callable[[float], float]:
    keyframes = sorted(keyframes, key=lambda t: t[0])

    if len(keyframes) == 0:
        raise ValueError("No keyframes given")

    keyframes_x = [x for x, y in keyframes]
    keyframes_y = [y for x, y in keyframes]

    def keyframed_function(x: float) -> float:
        right = bisect_right(keyframes_x, x)
        left = right - 1

        right = min(right, len(keyframes) - 1)
        left = max(left, 0)

        length = keyframes_x[right] - keyframes_x[left]

        if length == 0:
            return keyframes_y[left]

        position = x - keyframes_x[left]
        height = keyframes_y[right] - keyframes_y[left]

        return keyframes_y[left] + height * (position / length)

    return keyframed_function


__all__ = keyframes
