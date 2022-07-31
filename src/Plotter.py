from typing import Tuple
from nltk.probability import FreqDist
from pandas.core.frame import DataFrame

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
import pandas as pd


class Plotter:
    def __init__(self):
        pass

    @staticmethod
    def get_colors_range(colors: list[str], amount: int) -> list[str]:
        """
        Returns a list of rgb colors that are evenly distributed between the two colors.

        :param colors: List of two colors in hexadecimal format.
        :param amount: Amount of colors to be returned.
        """
        colors_as_rgb = [to_rgb(color) for color in colors]
        rgb_diff = [
            (colors_as_rgb[1][0] - colors_as_rgb[0][0]) / amount,
            (colors_as_rgb[1][1] - colors_as_rgb[0][1]) / amount,
            (colors_as_rgb[1][2] - colors_as_rgb[0][2]) / amount
        ]
        colors = [
            (colors_as_rgb[0][0] + i * rgb_diff[0],
             colors_as_rgb[0][1] + i * rgb_diff[1],
             colors_as_rgb[0][2] + i * rgb_diff[2])
            for i in range(amount)
        ]
        return colors

    @staticmethod
    def get_start_end_dates(sentiment_scores: DataFrame) -> dict:
        """
        Returns the start and end dates of the dataframe.

        :param sentiment_scores: Dataframe with the mean sentiment score of tweets.
        """
        return {
            'start': sentiment_scores['date'].min()[:10],
            'end': sentiment_scores['date'].max()[:10]
        }

    def plot_freq_dist(self,
                       fdist: FreqDist,
                       amount: int,
                       colors: list[str],
                       title: str = "Frequency distribution") -> None:
        """
        Plots a frequency distribution.

        :param fdist: Frequency distribution to be plotted.
        :param amount: Amount of words to be plotted.
        :param colors: List of two colors in hexadecimal format.
        :param title: Title of the plot.
        """
        colors = Plotter.get_colors_range(colors, amount)
        title = title.capitalize()
        fdist = fdist.most_common(amount)[1:]

        plt.title(title)
        plt.ylabel("Frequency")
        plt.bar(range(len(fdist)), [item[1]for item in fdist], color=colors)
        plt.xticks(range(len(fdist)), [item[0] for item in fdist], rotation=70)
        plt.tight_layout()
        plt.show()

    def plot_sentiment_scores_by_date(self, sentiment_scores: DataFrame) -> None:
        """
        Plots mean sentiment score by date.

        :param sentiment_scores: Dataframe with mean sentiment score by date.
        """
        dates = Plotter.get_start_end_dates(sentiment_scores[0])
        plt.title("Mean sentiment score between "
                  f"{dates.get('start')} "
                  "and "
                  f"{dates.get('end')}"
                  )
        plt.ylabel("Mean sentiment score")
        plt.xticks([])
        plt.plot(sentiment_scores['date'], sentiment_scores['sentiment_score'])
        plt.tight_layout()
        plt.show()

    def plot_sentiment_scores_comparision(self,
                                          sentiment_scores: list[DataFrame],
                                          legend: list[str],
                                          colors: list[str]) -> None:
        """
        Plots the comparison of mean sentiment scores of each dataframe.

        :param sentiment_scores: List of dataframes with the mean sentiment score of tweets.
        :param legend: List of legends for the plots.
        :param colors: List of two colors in hexadecimal format.
        """
        copied_dataframes = [df.copy() for df in sentiment_scores]
        for sentiment_score in copied_dataframes:
            sentiment_score['date'] = sentiment_score['date'].apply(
                lambda x: x[:10])
            sentiment_score['date'] = pd.to_datetime(sentiment_score['date'])

        dates = Plotter.get_start_end_dates(sentiment_scores[0])
        plt.title("Mean sentiment score between "
                  f"{dates.get('start')} "
                  "and "
                  f"{dates.get('end')}"
                  )

        plt.xticks([])

        for sentiment_scores in copied_dataframes:
            plt.plot(sentiment_scores['date'],
                     sentiment_scores['sentiment_score'],
                     color=colors.pop(0),
                     label=legend.pop(0)
                     )

        plt.ylabel("Mean entiment score")
        plt.legend(loc='upper left')
        plt.tight_layout()
        plt.show()

    def plot_sentiment_scores_comparision_diff(self,
                                               sentiment_scores: Tuple[DataFrame, DataFrame],
                                               colors: list[str]) -> None:
        """
        Plots the difference of mean sentiment scores of each dataframe.

        :param sentiment_scores: List of dataframes with the mean sentiment score of tweets.
        :param colors: List of two colors in hexadecimal format.
        """

        difference = pd.DataFrame(
            sentiment_scores[0]['sentiment_score'] - sentiment_scores[1]['sentiment_score'])
        difference['date'] = sentiment_scores[0]['date']

        dates = Plotter.get_start_end_dates(sentiment_scores[0])
        plt.title("Difference of mean sentiment scores between "
                  f"{dates.get('start')} "
                  "and "
                  f"{dates.get('end')}"
                  )

        plt.xticks([])

        plt.plot(difference['date'],
                 [0] * len(difference),
                 color='black'
                 )
        plt.plot(difference['date'],
                 difference['sentiment_score'],
                 color=colors.pop(0)
                 )

        plt.ylabel("Mean entiment score")
        plt.tight_layout()
        plt.show()
