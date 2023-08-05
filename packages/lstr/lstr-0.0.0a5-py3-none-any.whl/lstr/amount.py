from enum import Enum


class Amount(Enum):
    """
    Vaguely but truthfully describes an amount.
    """

    NOOP = 0
    NONE = 1
    SOME = 2
    ALL = 4
