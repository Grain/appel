#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import probablepeople as pp
import math
import sys

alpha = {}
nonalpha = {}
maxauthors = 0

STEP = 0.0001

# L(p), where p is the proportion of scientists
def L(p):
    prob = 1.0

    for i in range(2, maxauthors + 1):
        c = p / math.factorial(i)
        prob *= pow(1 - p + c, alpha[i])
        prob *= pow(p - c, nonalpha[i])
        prob *= math.comb(alpha[i] + nonalpha[i], alpha[i])

    if prob < 0:
        print("hm")
    if prob > 1:
        print("hm")
    return prob

# total area under the curve
def area():
    total = 0.0
    i = 0
    while i <= 1:
        total += L(i) * STEP
        i += STEP

    return total

# Only uses given name and surname
def isalphabetical(names):
    for name in names:
        d = pp.tag(name, "person")[0]
        if "Surname" not in d.keys():
            print("Surname not found: " + name)
            exit()

    surnames = [pp.tag(name, "person")[0]["Surname"] for name in names]

    for i in range(len(names) - 1):
        if surnames[i] > surnames[i+1]:
            return False
        elif surnames[i] == surnames[i+1]:
            if pp.tag(names[i], "person")[0]["GivenName"] > pp.tag(names[i+1], "person")[0]["GivenName"]:
                return False
    return True

with open(sys.argv[1]) as f:
    lines = f.readlines()
    for line in lines:
        names = line.strip().split(", ")
        numauthors = len(names)
        maxauthors = max(maxauthors, numauthors)

        if isalphabetical(names):
            alpha[numauthors] = alpha.get(numauthors, 0) + 1
        else:
            nonalpha[numauthors] = nonalpha.get(numauthors, 0) + 1

for i in range(2, maxauthors + 1):
    alpha[i] = alpha.get(i, 0)
    nonalpha[i] = nonalpha.get(i, 0)
    # print("%d: %d %d" % (i, alpha[i], nonalpha[i]))

p = 0.0
maxp = p
maxlp = L(p)

while p <= 1:
    lp = L(p)
    if lp >= maxlp:
        maxp = p
        maxlp = lp
    p += STEP


errorarea = area() / 3

lowp = maxp
area = 0
# second conjunct is for issue where lowp goes below 0 and L(lowp) becomes negative too, going into an infinite loop
while area < errorarea and lowp >= STEP:
    area += L(lowp) * STEP
    lowp -= STEP


highp = maxp
area = 0
while area < errorarea and highp <= 1 - STEP:
    area += L(highp) * STEP
    highp += STEP

print("%s %f %f %f" % (sys.argv[1], maxp, maxp - lowp, highp - maxp))
# print(maxp)
# print(maxp - lowp)
# print(highp - maxp)
