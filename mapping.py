

def clamp(value, low, high):
    return max(low, min(value, high))

def mapAxis(v, margin, screen_size):
    """v: normalized hand position (0..1). Returns a screen coordinate in [1, size-2]."""
    v = (v - margin) / (1 - 2 * margin)   # stretch active region to 0..1
    v = clamp(v, 0.0, 1.0)                # hand outside the region -> saturate
    return 1 + v * (screen_size - 3)      # land inside the failsafe-safe range
