from typing import List, Tuple

class PolylabelError(ValueError): ...

def polylabel_ext(
    exterior: List[Tuple[float, float]], tolerance: float
) -> Tuple[float, float]: ...
