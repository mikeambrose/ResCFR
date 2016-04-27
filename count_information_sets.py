"""Simple code for counting the number of information sets that the full game of The Resistance has"""
s = (("PV"*5)+"R")*5
d = {"P":10, "V":32, "R":2}
s = s[:-1]
num = 0
for i in range(len(s)):
    subnum = 1
    for j in range(i+1):
        subnum *= d[s[j]]
    num += subnum
    print i, subnum
from math import log
tenx = log(num,10)
