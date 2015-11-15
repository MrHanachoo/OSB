import re

temp = "@"

lists = ["abc", "123.35", "med@rosafi.com", "AND+"]

for list in lists:
    if re.search(list, temp, re.I):
        print "The %s is within %s." % (list, temp)



