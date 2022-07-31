from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from pandas.core.frame import DataFrame
import json
import re
import glob


class Tweets:
    def __init__(self, filename: str, columns: list[str]):
        self.tweets = self.load_columns_to_dataframe(filename, columns)
        self.sentiment_scores = self.load_columns_to_dataframe(
            filename, columns)

    # Data import

    def load_columns_to_dataframe(self, filename: str, columns: list[str]) -> DataFrame:
        """
        Load the given columns from the given file to a dataframe.

        :param filename: The file to load the columns from.
        :param columns: The columns to load.
        """
        data = []
        with open(filename) as file_handler:
            for line in file_handler:
                line_as_json = json.loads(line)
                fields = [line_as_json[column] for column in columns]
                data.append(fields)
        return pd.DataFrame(data, columns=columns)

    # Preprocessing data

    def remove_unnecessary_characters(self, dataframe: DataFrame, column: str) -> None:
        """
        Remove unnecessary characters from the data in the given column.

        Every string is converted to lowercase.
        Every twitter username is removed.
        Every link is removed.
        Every character is removed except for letters and numbers.

        :param column: The column to remove unnecessary characters from.
        """
        regex_pattern = re.compile('@[a-z0-9_]+|\w+:\/\/\S+|[^a-z0-9]+')

        dataframe[column] = (
            dataframe[column].apply(str.lower)
            .apply(lambda e: regex_pattern.sub(r' ', e))
            .apply(str.strip)
        )

    def tokenize_data(self, dataframe: DataFrame, column: str) -> None:
        """
        Tokenize the data in the given column using word_tokenize.
        Also it removes words with length less than 3.

        :param column: The column to tokenize.
        """
        dataframe[column] = (
            dataframe[column].apply(word_tokenize)
            .apply(lambda x: [word for word in x if len(word) > 2])
        )

    def remove_stop_words(self, dataframe: DataFrame, column: str) -> None:
        """
        Remove stop words from the data in the given column using stopwords from nltk.

        :param column: The column to remove stop words from.
        """
        stop_words = set(stopwords.words('english'))
        dataframe[column] = dataframe[column].apply(
            lambda x: [word for word in x if word not in stop_words]
        )

    def lemmatize_column_in_dataframe(self, dataframe: DataFrame, column: str) -> None:
        """
        Lemmatize the data in the given column using WordNetLemmatizer.

        :param column: The column to lemmatize.
        """
        lemmatizer = WordNetLemmatizer()
        dataframe[column] = dataframe[column].apply(
            lambda x: [lemmatizer.lemmatize(word) for word in x]
        )

    def preprocess_data(self, dataframe: DataFrame, column: str) -> None:
        """
        Preprocess the data in the given column.

        :param column: The column to preprocess.
        """
        self.remove_unnecessary_characters(dataframe, column)
        self.tokenize_data(dataframe, column)
        self.remove_stop_words(dataframe, column)
        self.lemmatize_column_in_dataframe(dataframe, column)

    # Data analysis

    def get_frequency_distribution(self, column: str) -> FreqDist:
        """
        Returns the frequency distribution of the data in the given column.

        :param column: The column to get the frequency distribution from.
        """
        words = self.tweets[column].values.tolist()
        words = [word for sublist in words for word in sublist]
        fdist = FreqDist(words)
        return fdist

    def get_frequency_distribution_by_sentiment_score(self, negative: bool, column: str) -> FreqDist:
        """
        Returns the frequency distribution of the dataframe.

        :param negative: If true, get negative tweets, otherwise get positive tweets.
        """
        sentiment_scores_copy = self.sentiment_scores.copy()
        self.preprocess_data(sentiment_scores_copy, 'content')
        words = sentiment_scores_copy.query(
            'sentiment_score < 0' if negative else 'sentiment_score > 0')[column].values.tolist()
        words = [word for sublist in words for word in sublist]
        fdist = FreqDist(words)
        return fdist

    def calculate_sentiment_scores(self, column: str) -> None:
        """
        Calculate the sentiment score for each tweet in the given column.

        :param column: The column to calculate the sentiment score for.
        """
        sid = SentimentIntensityAnalyzer()
        self.sentiment_scores["sentiment_score"] = self.sentiment_scores.apply(
            lambda x: sid.polarity_scores(x[column])['compound'], axis=1
        )

    def get_tweets_by_sentiment_score(self, amount: int, negative: bool) -> DataFrame:
        """
        Returns positive or negative tweets from the dataframe.

        :param amount: The amount of tweets to get.
        :param negative: If true, get negative tweets, otherwise get positive tweets.
        """
        return (self.sentiment_scores
                .query('sentiment_score < 0' if negative else 'sentiment_score > 0')
                .sort_values('sentiment_score', ascending=False)
                .head(amount)
                )

    def get_mean_sentiment_score(self) -> float:
        """
        Returns the mean sentiment score of the dataframe.
        """
        return self.sentiment_scores['sentiment_score'].mean()

    def get_start_date(self) -> str:
        """
        Returns the start and end date of the dataframe.
        """
        return self.tweets['date'].max()

    # Output

    def print_tweets(self, df: DataFrame) -> DataFrame:
        for i, tweet in df.iterrows():
            print("==========================")
            print(f"Tweet {i}, sentiment score: {tweet['sentiment_score']}")
            print(tweet['content'])
            print("==========================")

    def print_most_positive_tweets(self, amount: int) -> None:
        df = self.get_tweets_by_sentiment_score(amount, negative=False)
        print("Most positive tweets:")
        self.print_tweets(df)

    def print_most_negative_tweets(self, amount: int) -> None:
        df = self.get_tweets_by_sentiment_score(amount, negative=True)
        print("Most negative tweets:")
        self.print_tweets(df)

    def print_statistics_about_sentiment_score(self) -> None:
        positive_tweets = self.sentiment_scores.query('sentiment_score > 0')
        negative_tweets = self.sentiment_scores.query('sentiment_score < 0')

        stats = {
            'positive_tweets': positive_tweets.shape[0],
            'negative_tweets': negative_tweets.shape[0],
            'tweets_count': self.sentiment_scores.shape[0],
            'pos_tweets_percentage': positive_tweets.shape[0] / self.sentiment_scores.shape[0],
            'neg_tweets_percentage': negative_tweets.shape[0] / self.sentiment_scores.shape[0],
            'tweets_statistics': self.sentiment_scores.describe()
        }

        print("Tweets statistics:")
        print("==========================")
        print(stats.get('tweets_statistics'))
        print(f"Amount of positive tweets: {stats.get('positive_tweets')}")
        print(f"Percentage: {stats.get('pos_tweets_percentage')}")
        print(f"Amount of negative tweets: {stats.get('negative_tweets')}")
        print(f"Percentage: {stats.get('neg_tweets_percentage')}")
        print("==========================")


class TweetsCollection:
    def __init__(self, filename_suffix: str, columns: list[str]) -> None:
        self.tweets = [
            Tweets(filename, columns) for filename in glob.glob(f'data/*_{filename_suffix}.json')
        ]

    def preprocess_collection(self, column: str) -> None:
        """
        Preprocess the collection of tweets.
        """
        for tweets in self.tweets:
            tweets.preprocess_data(tweets.tweets, column)

    def calculate_sentiment_scores(self, column: str) -> None:
        """
        Calculate the sentiment score for each tweets in the collection.
        """
        for tweets in self.tweets:
            tweets.calculate_sentiment_scores(column)

    def get_mean_sentiment_scores_with_date(self) -> DataFrame:
        """
        Returns the mean sentiment score of the collection with dates.
        """
        sentiment_scores = pd.DataFrame(columns=['date', 'sentiment_score'])
        for i, tweets in enumerate(self.tweets):
            sentiment_scores.loc[i] = [
                tweets.get_start_date(),
                tweets.get_mean_sentiment_score()
            ]
        return sentiment_scores
