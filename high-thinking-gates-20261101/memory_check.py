#!/usr/bin/env python3
"""Gate 3 test: search MEMORY.md for a keyword. Exit 0 if found, 1 if not recorded.
Usage: python3 memory_check.py KEYWORD [MEMORY_PATH]"""
import sys, os
def main():
    if len(sys.argv) < 2:
        print("usage: memory_check.py KEYWORD", file=sys.stderr); return 2
    path = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/MEMORY.md")
    text = open(path, errors="ignore").read()
    if sys.argv[1].lower() in text.lower():
        print(f"MEMORY CHECK: PASS found '{sys.argv[1]}'"); return 0
    print(f"MEMORY CHECK: FAIL not recorded '{sys.argv[1]}' — do not guess, ask"); return 1
if __name__ == "__main__":
    sys.exit(main())
