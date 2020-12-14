from math import pow


def cutoff(r, c):
    return pow(r * c, -1)


def error(calc, desired):
    return abs(calc - desired)


def wantHPF(w_, center_):
    return w_ < center_


def wantLPF(w_, center_):
    return w_ > center_


def get_filter_str(high_pass : bool):
    return "high" if high_pass else "low"