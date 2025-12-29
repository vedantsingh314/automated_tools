import math

def maintainability_index(volume, complexity, loc):
    if loc == 0:
        return 100
    mi = 171 - 5.2 * math.log(volume + 1) \
             - 0.23 * complexity \
             - 16.2 * math.log(loc)
    return round(max(0, min(100, mi)), 2)
