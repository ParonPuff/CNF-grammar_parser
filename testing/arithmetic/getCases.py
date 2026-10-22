#!/usr/bin/env python3
"""
Generate arithmetic-like test strings for Grammar 1 (ambiguous arithmetic) using tokens:
  n = num, p = +, m = *
Usage:
    python3 arithmetic.py <start> <step> <end>
Prints one test string per line for each odd length in the range.
"""
import sys

def gen_arithmetic(start: int, step: int, end: int):
    for length in range(start, end + 1, step):
        # only odd lengths >= 1 make sense (must end on 'n')
        if length < 1 or length % 2 == 0:
            continue
        nums = (length + 1) // 2
        ops = (length - 1) // 2
        # alternate p and m for variety
        op_tokens = [('p' if i % 2 == 0 else 'm') for i in range(ops)]
        tokens = []
        for i in range(nums):
            tokens.append('n')
            if i < ops:
                tokens.append(op_tokens[i])
        print(''.join(tokens))

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <start> <step> <end>")
        sys.exit(1)
    s, st, e = map(int, sys.argv[1:])
    #print(s,st,e)
    gen_arithmetic(s, st, e)
