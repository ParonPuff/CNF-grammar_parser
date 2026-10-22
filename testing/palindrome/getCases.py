#!/usr/bin/env python3
"""
Generate palindrome test strings for Grammar 2 over {a, b}.
Usage:
    python3 palindrome.py <start> <step> <end>
Prints one palindrome per line for each length in the range.
"""
import sys

def gen_palindrome(start: int, step: int, end: int):
    for length in range(start, end + 1, step):
        if length < 1:
            continue
        half = length // 2
        # build half pattern as alternating 'a','b'
        half_pattern = ''.join('a' if i % 2 == 0 else 'b' for i in range(half))
        if length % 2 == 0:
            pal = half_pattern + half_pattern[::-1]
        else:
            pal = half_pattern + 'a' + half_pattern[::-1]
        print(''.join(pal))

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <start> <step> <end")
        sys.exit(1)
    s, st, e = map(int, sys.argv[1:])
    gen_palindrome(s, st, e)
