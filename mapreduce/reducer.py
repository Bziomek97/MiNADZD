#!/usr/bin/env python3
"""reducer.py"""

import sys
import json
from itertools import islice

def main():

    covid_holder = dict()

    for line in sys.stdin:
        try:
            key_val = line.split('\t')
            key = key_val[0]
            data = json.loads(key_val[1])

            if not key in covid_holder: 
                covid_holder[key] = data
            else:
                continue

        except Exception as e:
            sys.stderr.write("unable to parse reducer input: %s" % e)
            continue


    # Operation section - f.e grab 15 countries with highest per 1000 people total cases
    result_list = dict()

    tmp = dict()
    for key, value in covid_holder.items():
        tmp[key] = value['total_cases']
    
    result_list['total_cases_per_1000'] = dict(islice(dict(sorted(tmp.items(), reverse=True, key=lambda item: item[1])).items(), 15))



    for key, value in result_list.items():
        try:
            result_dumps = json.dumps(value)
            print("%s\t%s" % (key, result_dumps))

        except Exception as e:
            sys.stderr.write("unable to parse reducer output: %s" % e)
            continue

if __name__ == "__main__":
    main()