"""Small helpers shared by the Chorrin pack (files starting with _ are not loaded as clip modules).

    sampled(c, t0, t1, fn, step)   key every channel fn(t) returns, every `step` seconds from t0 to t1
    env(t, t0, t1, fade)           0 -> 1 -> 0 envelope: eases in from t0 over `fade`, out to t1
    sn(t, period, phase)           a sine
"""
import math


def smooth(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def env(t, t0, t1, fade):
    if t <= t0 or t >= t1:
        return 0.0
    return min(smooth((t - t0) / fade), smooth((t1 - t) / fade))


def sn(t, period, phase=0.0):
    return math.sin((t / period + phase) * math.tau)


def sampled(c, t0, t1, fn, step=0.1):
    n = max(1, round((t1 - t0) / step))
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        pose = fn(t)
        if pose:
            c.key(t, **{k: tuple(v) for k, v in pose.items()})
    return c


def v(*xs):
    return tuple(float(x) for x in xs)


def scale(pose, k):
    return tuple(x * k for x in pose)
