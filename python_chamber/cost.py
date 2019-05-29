#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'minPrice' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY cost as parameter.
#

def minPrice(cost):
    # Write your code here

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    cost_rows = int(input().strip())
    cost_columns = int(input().strip())

    cost = []

    for _ in range(cost_rows):
        cost.append(list(map(int, input().rstrip().split())))

    result = minPrice(cost)

    fptr.write(str(result) + '\n')

    fptr.close()
