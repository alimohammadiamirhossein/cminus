import math
import numpy as np
# degree 1 polynomial
# a*x + b

# set a & b

a = 2
b = 3


def pol_one(x1, y1):
    ss1 = [[0, 0], [0, 0]]
    dd1 = [[0],[0]]
    for i in range(len(x1)):
        ss1[0][0] += 1
        ss1[0][1] += x1[i]
        ss1[1][0] += x1[i]
        ss1[1][1] += x1[i] * x1[i]
        dd1[0][0] += y1[i]
        dd1[1][0] += y1[i] * x1[i]
    return ss1, dd1

# degree 2 polynomial

# q*x^2 + e*x + r

# set q & e & r

q = 3
e = 4
r = 6



def pol_two(x2, y2):
    s2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    d2 = [[0], [0], [0]]
    for i in range(len(x2)):
        s2[0][0] += 1
        s2[0][1] += x2[i]
        s2[0][2] += x2[i] ** 2
        s2[1][0] += x2[i]
        s2[1][1] += x2[i] ** 2
        s2[1][2] += x2[i] ** 3
        s2[2][0] += x2[i] ** 2
        s2[2][1] += x2[i] ** 3
        s2[2][2] += x2[i] ** 4
        d2[0][0] += y2[i]
        d2[1][0] += y2[i] * x2[i]
        d2[2][0] += y2[i] * x2[i] * x2[i]
    return s2, d2

# f(x) = m/x + n

# set m & n

m = 10
n = 1

def f1(x3):
    return m/x3 + n


# f(x) = s*ln(x) + d

# set s & d

s = 11
d = 12


def f2(x4):
    return s * math.log(x4, base=math.e) + d

# f(x) = 1 / (cx + v)

# set c & v

c = 12
v = 15


def f2(x5):
    return 1 / (c*x + v)


x = list(map(int, input().split()))
y = list(map(int, input().split()))
r1, o1 = pol_one(x, y)
print(np.linalg.inv(r1).dot(o1))
r2, o2 = pol_two(x, y)
print(r2)
print(np.linalg.inv(r2).dot(o2))
