#!/bin/bash

chmod +x mapper.py reducer.py

hadoop fs -test -d /results

if [ $? -eq 0 ]
then
    hadoop fs -rm -r /results
fi

mapred streaming -file mapper.py -file reducer.py -mapper mapper.py -reducer reducer.py -input /minadzd/covid.json -output /results
