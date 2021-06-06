#!/usr/bin/env python3
"""mapper.py"""

import sys
import json

def main():
    
    # loop through each line of stdin
    for line in sys.stdin:
        try:
            # read JSON
            j = json.loads(line)

            output = list()

            for entry in j:
                tmp_data = {
                    'total_cases': entry['total_cases']/1000,
                    'new_cases': entry['new_cases']/1000,
                    'total_deaths': entry['total_deaths']/1000,
                    'new_deaths': entry['new_deaths']/1000,
                    'total_recovered': entry['total_recovered']/1000,
                    'active_cases': entry['active_cases']/1000,
                    'serious_cases': entry['serious_cases']/1000,
                    'total_tests': entry['total_tests']/1000
                }
                output.append((entry['country'], json.dumps(tmp_data)))


            for entry in output:
                print("%s\t%s" % (entry[0], entry[1]))

        except Exception as e:
            sys.stderr.write("unable to read covid file: %s" % e)
            continue

if __name__ == "__main__":
    main()