"""Program."""
import math


def gcd(a, b):
    """Gcd."""
    if (a == 0):
        return b
    if (b == 0):
        return a
    if (a == b):
        return a

    if (a > b):
        return gcd(a - b, b)
    return gcd(a, b - a)


def meet_me(pos1, jump_distance1, sleep1, pos2, jump_distance2, sleep2) -> int:
    """Calculate the meeting position of 2 jangurus.

    @:param pos1: position of first janguru
    @:param jump_distance1: jump distance of first janguru
    @:param sleep1: sleep time of first janguru
    @:param pos2: position of second janguru
    @:param jump_distance2: jump distance of second janguru
    @:param sleep2: sleep time of second janguru

    @:return positions where jangurus first meet
    """
    dis1 = pos1
    dis2 = pos2
    difference = dis1 - dis2
    gcd_of_sleep = gcd(sleep1, sleep2)
    lcm_of_sleep = (sleep1 * sleep2) // gcd_of_sleep
    movement1 = lcm_of_sleep // sleep1 * jump_distance1
    movement2 = lcm_of_sleep // sleep2 * jump_distance2
    difference2 = movement2 - movement1
    if difference2 == 0:
        x = 0
    else:
        x = difference / difference2

    if x < 0:
        x = 0
    if x > 0:
        x = math.floor(x)

    time = x * lcm_of_sleep
    dis12 = dis1 + movement1 * x
    dis22 = dis2 + movement2 * x

    if dis12 == dis22 and x > 0:
        return dis12
    dis12 += jump_distance1
    dis22 += jump_distance2
    if dis12 == dis22:
        return dis12

    while time <= (x + 1) * lcm_of_sleep:
        next_jump1 = sleep1 - time % sleep1
        next_jump2 = sleep2 - time % sleep2
        min_jump = min(next_jump1, next_jump2)
        if min_jump - next_jump1 == 0:
            dis12 += jump_distance1
        if min_jump - next_jump2 == 0:
            dis22 += jump_distance2
        if dis12 == dis22:
            return dis12
        time += min_jump
    return -1


if __name__ == "__main__":
    print(meet_me(1, 2, 1, 2, 1, 1))  # => 3
    print(meet_me(1, 2, 3, 4, 5, 5))  # => -1
    print(meet_me(10, 7, 7, 5, 8, 6))  # => 45
    print(meet_me(100, 7, 4, 300, 8, 6))  # => 940
    print(meet_me(1, 7, 1, 15, 5, 1))  # => 50
    print(meet_me(0, 1, 1, 1, 1, 1))  # => -1
