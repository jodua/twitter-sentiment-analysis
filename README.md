# twitter-sentiment-analysis

Twitter sentiment analysis project build in python.

## Features

- Calculating and plotting sentiment scores for tweets downloaded from snscrape.
- Obtaining and plotting frequency distribution of words used in tweets. 

## Requirements

- python3
- requirements.txt
- snscrape

## Example usage

Sentiment analysis of tweets from **csharp** and **java** hashtags. 

It contains:
- Frequency distribution of words used in tweets. (both positive and negative)
- Sentiment score comparision over time.
- Statistics about tweets.

`pip install -r requirements.txt`

`pip install snscrape`

Windows
```
./scripts/download_latests.ps1 csharp 10000
./scripts/download_range.ps1 csharp 100 2016-01-01 2022-06-01 30
./scripts/download_latests.ps1 java 10000
./scripts/download_range.ps1 java 100 2016-01-01 2022-06-01 30

python ./main.py
```

Linux
```
./scripts/download_latests.sh csharp 10000
./scripts/download_range.sh csharp 100 2016-01-01 2022-06-01 30
./scripts/download_latests.sh java 10000
./scripts/download_range.sh java 100 2016-01-01 2022-06-01 30

python ./main.py
```