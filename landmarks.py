from enum import IntEnum


class landmark(IntEnum):
    """Enum for hands landmarks."""
    WRIST = 0
    THUMB_TIP = 4
    INDEX_PIP = 6
    INDEX_TIP = 8
    MIDDLE_PIP = 10
    MIDDLE_TIP = 12
    RING_PIP = 14
    RING_TIP = 16
    PINKY_PIP = 18
    PINKY_TIP = 20