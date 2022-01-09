import math


def interpolation(min_degree: float, max_degree: float, dawn: float = 5, peak: float = 15):
    """
    Return an interpolate function which users can get the temperature based on the time input
    :param min_degree: lowest temperature of the day
    :param max_degree: highest temperature of the day
    :param dawn: time when lowest temperature happens. By default set as 5:00 AM
    :param peak: time when highest temperature happens. By default set as 3:00 PM
    :return:
    """
    return lambda t: (
        (max_degree+min_degree)/2-(max_degree-min_degree)/2*math.cos(math.pi*(dawn-t)/(24+dawn-peak))
        if t < dawn else
        (max_degree+min_degree)/2+(max_degree-min_degree)/2*math.cos(math.pi*(peak-t)/(peak-dawn))
        if t < peak else
        (max_degree+min_degree)/2-(max_degree-min_degree)/2*math.cos(math.pi*(24+dawn-t)/(24+dawn-peak)))
