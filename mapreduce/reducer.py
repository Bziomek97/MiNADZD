#!/usr/bin/env python3
"""reducer.py"""

import sys
import json

def get_max_15_values(data, stat):
    tmp = dict()
    for key, value in data.items():
        tmp[key] = value[stat]

    return dict(sorted(tmp.items(), key=lambda x: x[1], reverse=True)[:10])

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
    statistics = {
        'total_cases_highest_countries': 'total_cases',
        'new_cases_highest_countries': 'new_cases',
        'total_deaths_highest_countries': 'total_deaths',
        'new_deaths_highest_countries': 'new_deaths',
        'total_recovered_highest_countries': 'total_recovered',
        'active_cases_highest_countries': 'active_cases',
        'serious_cases_highest_countries': 'serious_cases',
        'total_tests_highest_countries': 'total_tests'
    }

    for key, value in statistics.items():
        result_list[key] = get_max_15_values(covid_holder, value)

    for key in result_list.keys():
        result_list[key]['Total'] = sum(result_list[key].values())

    for key, value in result_list.items():
        try:
            result_dumps = json.dumps(value)
            print("%s\t%s" % (key, result_dumps))

        except Exception as e:
            sys.stderr.write("unable to parse reducer output: %s" % e)
            continue

if __name__ == "__main__":
    main()