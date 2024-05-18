import math

def average_speed_m_s(distance,time):
    """ Compute average speed in meters / seconds. Args:Distance in meters and time in seconds """
    if time != 0:
        return distance/time
    else:
        return 0

def average_speed_m_k(average_speed_m_s):
    """ Converts the average speed in meters/seg arg to min/km """
    if average_speed_m_s != 0:
        return 1/(0.06*average_speed_m_s)
    else:
        return 0

def average_speed_m_s_txt(average_speed_m_k):
    """ Returns average speed in min/km expression text """
    frac, whole = math.modf(average_speed_m_k)
    min=int(whole)
    sec = round(frac*60)
    return  str(min) + ':' + str(sec) + ' min/km'

def average_speed2_m_k(average_speed_m_s):
    """ Converts the average speed in meters/seg arg to min/km (second version of average_speed_m_k function ) """
    if average_speed_m_s != 0:
        average = 1/(0.06*average_speed_m_s)
        float_time = average  # in minutes
        hours, seconds = divmod(float_time * 60, 3600)  # split to hours and seconds
        minutes, seconds = divmod(seconds, 60)
        result = "{:02.0f}:{:02}".format( minutes, int(seconds))
        return result 
    else:
        return 0