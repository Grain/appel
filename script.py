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

def area():
    total = 0.0
    i = 0
    while i <= 1:
        total += L(i) * STEP
        i += STEP

    return total

with open(sys.argv[1]) as f:
    lines = f.readlines()
    for line in lines:
        names = line.strip().split(", ")
        numauthors = len(names)
        maxauthors = max(maxauthors, numauthors)

        ## For debugging when someone doesn't have a surname assigned...
        # print(names)
        # for name in names:
        #     d = pp.tag(name, "person")[0]
        #     for k, v in d.items():
        #         print(k, v)

        surnames = [pp.tag(name, "person")[0]["Surname"] for name in names]

        # TODO: handle when surnames are equal and we have to look at first name too
        if all(surnames[i] <= surnames[i+1] for i in range(numauthors-1)):
            alpha[numauthors] = alpha.get(numauthors, 0) + 1
        else:
            nonalpha[numauthors] = nonalpha.get(numauthors, 0) + 1
            # print(surnames)

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
# second conjunct is for issue where lowp goes below 0 and this goes into infinite loop.
# TODO: might be needed on highp loop too?
while area < errorarea and lowp >= STEP:
    area += L(lowp) * STEP
    lowp -= STEP


highp = maxp
area = 0
while area < errorarea:
    area += L(highp) * STEP
    highp += STEP

print("%s %f %f %f" % (sys.argv[1], maxp, maxp - lowp, highp - maxp))
# print(maxp)
# print(maxp - lowp)
# print(highp - maxp)
