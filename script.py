#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import probablepeople as pp
import math
import sys

alpha = {}
nonalpha = {}
maxauthors = 0

# L(p), where p is the proportion of scientists
def L(p):
    prob = 1.0

    for i in range(2, maxauthors + 1):
        c = p/math.factorial(i)
        prob *= pow(1 - p + c, alpha[i])
        prob *= pow(p - c, nonalpha[i])
        prob *= math.comb(alpha[i] + nonalpha[i], alpha[i])

    return prob

with open(sys.argv[1]) as f:
    lines = f.readlines()
    for line in lines:
        names = line.strip().split(", ")
        numauthors = len(names)
        maxauthors = max(maxauthors, numauthors)
        surnames = [pp.tag(name, "person")[0]["Surname"] for name in names]

        if all(surnames[i] <= surnames[i+1] for i in range(numauthors-1)):
            if numauthors not in alpha:
                alpha[numauthors] = 1
            else:
                alpha[numauthors] += 1
        else:
            if numauthors not in nonalpha:
                nonalpha[numauthors] = 1
            else:
                nonalpha[numauthors] += 1

for i in range(2, maxauthors + 1):
    alpha[i] = alpha.get(i, 0)
    nonalpha[i] = nonalpha.get(i, 0)
    print("%d: %d %d" % (i, alpha[i], nonalpha[i]))

p = 0.0
step = 0.001
maxp = p
maxlp = L(p)

while p <= 1:
    lp = L(p)
    if lp >= maxlp:
        maxp = p
        maxlp = lp
    p += step

print(maxp)
