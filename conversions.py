from math import pi


def fromRadtoBPM(w):
    return 60 * fromRadtoHz(w)


def fromRadtoHz(w):
    return w / (2 * pi)
