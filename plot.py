#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt

labels = []
p = []
pl = []
ph = []

with open(sys.argv[1]) as f:
    lines = f.readlines()
    lines.reverse()

    for line in lines:
        [a, b, c, d] = line.split()
        labels.append(a)
        p.append(float(b))
        pl.append(float(c))
        ph.append(float(d))

# fig, ax = plt.subplots()
plt.errorbar(p, labels, None, [pl, ph], "o")
plt.axis([0, 1, -1, len(p) + 1])

plt.show()
