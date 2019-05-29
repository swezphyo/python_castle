#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'funWithAnagrams' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts STRING_ARRAY s as parameter.
#

def funWithAnagrams(s):
    # Write your code here
    s = sorted(s)
    return s

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s_count = int(input().strip())

    s = []

    for _ in range(s_count):
        s_item = input()
        s.append(s_item)

    result = funWithAnagrams(s)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()
