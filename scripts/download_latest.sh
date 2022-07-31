#!/bin/bash

# [c] jodua 20220616

# Download latest tweets using snscrape

# First argument is the hashtag
# Second argument is amount of latest tweets to download


hashtag=$1
amount=$2

if ! command -v snscrape &> /dev/null
then
    echo "Snscrape could not be found"
    exit
fi

echo "Downloading latest tweets with #$hashtag"
snscrape -n $amount --jsonl twitter-hashtag hashtag > "data/latest_$hashtag.json"
echo "Download complete"