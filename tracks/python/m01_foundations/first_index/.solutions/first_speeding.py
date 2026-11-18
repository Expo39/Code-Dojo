def first_speeding(speeds, limit):
    for i, speed in enumerate(speeds):
        if speed > limit:
            return i
    return -1
