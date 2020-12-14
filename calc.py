from math import pi, sqrt

from conversions import fromRadtoBPM, fromRadtoHz
from frequency_formulas import cutoff, error, wantHPF, wantLPF, get_filter_str

MAX_ORDER = 5
IS_LPF = False

# TODO: Export constants to config file for readability

K = 1000
micro = 10 ** (-6)
nano = 10 ** (-9)
pico = 10 ** (-12)

R = [1.1, 10, 47, 68, 100, 470, K, 1.5 * K, 2.2 * K, 4.7 * K,
     6.8 * K, 10 * K, 20 * K, 47 * K, 68 * K, 100 * K, 200 * K]

# Daegan's available caps
C = [22 * pico, 47 * pico, 470 * pico, nano, 4.7 * nano, 10 * nano, 47 * nano, 10 * micro, 4.7 * micro]
# C = [0.001 * micro, 0.0047 * micro, 0.1 * micro, micro, 4.7 * micro, 10 * micro, 22 * micro, 47 * micro, 220 * micro]


def iterateThruComponents(corner_, high_pass = True, can_print = True):
    """

    :param can_print:
    :param corner_: desired corner frequency of first-order circuit
    :param high_pass: is the circuit a high-pass or low-pass circuit
    :return: tuple containing the best-fitting resistance, capacitance values and the resulting corner frequency
    """
    best_r, best_c = R[0], C[0]
    best_w = cutoff(best_r, best_c)

    # TODO: Replace with a more efficient search using binary search
    for res in R:
        for cap in C:
            approx_corner = cutoff(res, cap)
            meets_reqs = wantHPF(approx_corner, corner_) if high_pass else wantLPF(approx_corner, corner_)
            if meets_reqs and error(approx_corner, corner_) < error(best_w, corner_):
                best_w = approx_corner
                best_r, best_c = res, cap

    if can_print:
        print("For a first-order {}-pass filter:".format("high" if high_pass else "low"))
        print("Resistance: {}, Capacitance: {} with cutoff {} rad/s or {} Hz or {} bpm".format(best_r, best_c, best_w, fromRadtoHz(best_w),
                                                                                            fromRadtoBPM(best_w)))
    return best_r, best_c, best_w


def iterateCascade(corner_, high_pass = True, max_order = MAX_ORDER):
    """

    :param corner_:
    :param high_pass:
    :param max_order:
    """
    # best_r, best_c = R[0], C[0]
    # best_w = cutoff(best_r, best_c)
    best_r, best_c, best_w = iterateThruComponents(corner_, high_pass, False)
    best_n = 1
    for n in range(2, max_order):
        scale = sqrt((2 ** (n ** -1)) - 1)
        # alpha represents the corner frequency of an
        # individual first-order filter in an n-stage cascaded design
        if high_pass:
            alpha = corner_ * scale
        else:
            alpha = corner_ / scale

        # Iterate thru available components to find pair that will
        # approximate desired specs of the single first-order filter
        res, cap, approx_alpha = iterateThruComponents(alpha, high_pass, False)

        # Reverse previous arithmetic to find the propagated error in the full n-order circuit's corner frequency

        approx_corner = 0
        if high_pass:
            approx_corner = approx_alpha / scale
        else:
            approx_corner = approx_alpha * scale
        if error(approx_corner, corner_) < error(best_w, corner_):
            best_w = approx_corner
            best_r, best_c = res, cap
            best_n = n
        print("\nFor an {}-stage {}-pass cascade".format(n, get_filter_str(high_pass)))
        print("we need resistance {} and capacitance {}, for a full corner frequency of {} rad/s or {} Hz".format(res, cap, approx_corner, fromRadtoHz(approx_corner)))

    print("\n\nIn order to achieve a corner frequency of {} rad/s for this {}-pass circuit".format(corner_, get_filter_str(high_pass)))
    print("The best possible cascaded circuit is of order {} with resistance {} and capacitance {}".format(best_n, best_r, best_c))
    print("Giving the full cascaded circuit a corner frequency of {} rad/s or {} Hz or {} BPM".format(best_w, fromRadtoHz(best_w), fromRadtoBPM(best_w)))


if __name__ == "__main__":
    center = 4 * pi  # 12.56 rad/s, or 120 bpm

    # center = 5.423665

    # HPF
    res_high, cap_high, w_high = iterateThruComponents(center)

    iterateCascade(w_high)

    print("\n=========================\n")

    # LPF
    res_low, cap_low, w_low = iterateThruComponents(center, IS_LPF)

    iterateCascade(center, IS_LPF)

