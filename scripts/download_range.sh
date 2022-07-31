#!/bin/bash

# [c] jodua 20220616

# Download tweets between two dates

# First argument is the hashtag
# Second argument is amount of tweets to download
# Third argument is the start date
# Fourth argument is the end date
# Fifth argument is the interval between tweets in days


hashtag=$1
amount=$2
inputStartDate=$3
inputEndDate=$4
interval=$5

if ! command -v snscrape &> /dev/null
then
    echo "Snscrape could not be found"
    exit
fi

startDate=$(date -I -d "$inputStartDate") || exit -1
endDate=$(date -I -d "$inputEndDate")     || exit -1

sd="$startDate"
ed=$(date -I -d "$sd + $interval day")

while [[ "$sd" < "$endDate" ]]
do
    echo "=========================================================="
    echo "Downloading tweets from $sd to $ed"

    snscrape -n $amount --since $sd --jsonl twitter-search "#$hashtag until:$ed" > "data/${sd}_${ed}_$hashtag.json"

    echo "Tweets downloaded"
    echo "=========================================================="

    sd=$(date -I -d "$sd + $interval day")
    ed=$(date -I -d "$sd + $interval day")
    
done