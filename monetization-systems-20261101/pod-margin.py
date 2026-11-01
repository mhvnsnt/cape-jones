#!/usr/bin/env python3
"""POD margin calculator. margin = retail - base_cost - platform_fee.
Refuses negative margin. No store, no purchase, no price set for Mars.
Usage: python3 pod-margin.py retail base_cost platform_fee"""
import sys
def main():
    if len(sys.argv) != 4:
        print("usage: pod-margin.py retail base_cost platform_fee", file=sys.stderr); return 2
    retail, base, fee = map(float, sys.argv[1:])
    margin = retail - base - fee
    print(f"retail={retail} base={base} fee={fee} margin={margin}")
    if margin < 0:
        print("FAIL: negative margin, do not list at this price"); return 1
    print("PASS: margin non-negative"); return 0
if __name__ == "__main__":
    sys.exit(main())
