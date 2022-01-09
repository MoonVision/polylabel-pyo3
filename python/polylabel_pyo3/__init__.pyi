from typing import Iterable, MutableMapping, Sequence, Tuple, Union

import numpy as np

class PolylabelError(ValueError): ...
class PolylabelShapeError(TypeError): ...

def polylabel_ext(
    exterior: Iterable[
        Union[MutableMapping[int, float], Tuple[float, float]], Sequence[float]
    ],
    tolerance: float,
) -> Tuple[float, float]: ...
def polylabel_ext_np(exterior: np.ndarray, tolerance: float) -> Tuple[float, float]: ...
