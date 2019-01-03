import math


def diff(a, b):
    return b[0] - a[0], b[1] - a[1]


def length(x, y):
    return math.sqrt((x ** 2) + (y ** 2))


def dot(a, b):
    return sum(i * j for i, j in zip(a, b))


def angle_between(a, b):
    '''a*b = |a|*|b|*cos(alpha)'''
    angle = math.degrees(math.acos(dot(a, b) / (length(*a) * length(*b))))
    return angle

def angle_between_plot(b,a):
    '''a*b = |a|*|b|*cos(alpha)'''
    x1, y1 = a
    x2, y2 = b
    dot = x1 * x2 + y1 * y2  # dot product between a and b
    det = x1 * y2 - y1 * x2  # determinant
    angle = math.degrees(math.atan2(det, dot))
    return angle


def limit_length(vector, max_length, min_length=0.0):
    length_current = length(*vector)#+0.0000001
    if length_current > max_length:
        normalizing_factor = max_length / length_current
    elif length_current < min_length:
        normalizing_factor = min_length / length_current
    else:
        return vector
    return [value * normalizing_factor for value in vector]
