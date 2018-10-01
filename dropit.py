import os
import re

"""
干掉pip的requirements.txt的版本号
"""

f = open("requirement.txt", "r")
if os.path.exists("drop_requirement.txt"):
    os.remove("drop_requirement.txt")
nf = open("drop_requirement.txt", "a")
for line in f:
    line_drop = re.search(".*==", line).group().replace("==","")
    print(line_drop)
    nf.write(line_drop+"\n")
f.close()
nf.close()