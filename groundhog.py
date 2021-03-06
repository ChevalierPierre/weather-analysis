#!/bin/python3

from stats import Stats
import sys

def display_usage():
    print("SYNOPSIS")
    print("\t./groundhog period\n")
    print("DESCRIPTION")
    print("\tperiod\t\tthe number of days defining a period")

def check_args(length):
    if length < 2:
        display_usage()
        exit(84)
    if sys.argv[1] == "-h":
        display_usage()
        exit(0)

if __name__ == "__main__":
    length = len(sys.argv)
    check_args(length)

    period = sys.argv[1]
    stats = Stats()

    try:
        stats.setPeriod(int(period))
    except:
        print(period + " is not a strictly positive integer", file=sys.stderr)
        exit(84)

    stats.start()
    exit(0)
