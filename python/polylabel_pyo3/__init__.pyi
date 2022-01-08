from typing import List, Tuple

class PolylabelException(ValueError): ...

def polylabel_ext(
    exterior: List[Tuple[float, float]], tolerance: float
) -> Tuple[float, float]: ...
