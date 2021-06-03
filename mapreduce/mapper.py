#!/usr/bin/python

import sys
import json

def main():
    for line in sys.stdin:
        try:
            covidJSON = json.loads(line.strip())
            for country in covidJSON:
                print(country['country'])

        except Exception as e:
            sys.stderr.write("unable to read covid file: %s" % e)
            continue

if __name__ == "__main__":
    main()