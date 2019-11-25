#!/usr/bin/env python

import subprocess as sp
sub_res = sp.Popen(["./yoloBash.sh"], stdout=sp.PIPE)
output = sub_res.communicate()[0]
print(output)
split = output.splitlines()
#print(split)
size = len(split)
#print(size)
#print(split[size-1])
final1 = split[size-1].decode("utf-8")
print(final1)
final2 = final1.split()
print(final2)
floats = [float(n) for n in final2]
ints = [int(n) for n in floats]
print(ints)
#ints contains the values for the top right and bottom left vertex of the bounding box
