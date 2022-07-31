# [c] jodua 20220616

from src.Plotter import Plotter
from src.Tweets import Tweets, TweetsCollection
from src.utils import load_nltk_modules, get_plot_title


def main() -> None:
    NLTK_MODULES = ['stopwords', 'wordnet', 'vader_lexicon', 'punkt']
    DATASET_COLUMNS = ['content', 'date']
    DATASET_FILENAMES = ['./data/csharp.json', './data/java.json']
    DATASET_PREFIXES = ['csharp', 'java']
    COLORS = [['#682876', '#B366AB'], ['#5382A1', '#F89820']]
    COMPARISION_COLORS = ['#B366AB', '#F89820']

    load_nltk_modules(NLTK_MODULES)
    plotter = Plotter()

    for filename, colors in zip(DATASET_FILENAMES, COLORS):
        tweets = Tweets(filename, DATASET_COLUMNS)
        tweets.preprocess_data(tweets.tweets, 'content')
        tweets.calculate_sentiment_scores('content')
        fdist = tweets.get_frequency_distribution('content')

        plot_title = get_plot_title(filename)

        plotter.plot_freq_dist(
            fdist=fdist,
            amount=20,
            colors=colors,
            title=plot_title
        )

        positive_freqdist = tweets.get_frequency_distribution_by_sentiment_score(
            negative=False,
            column='content'
        )

        negative_freqdist = tweets.get_frequency_distribution_by_sentiment_score(
            negative=True,
            column='content'
        )

        plotter.plot_freq_dist(
            fdist=positive_freqdist,
            amount=20,
            colors=colors,
            title=f"Positive sentences frequency distribution"
        )

        plotter.plot_freq_dist(
            fdist=negative_freqdist,
            amount=20,
            colors=colors,
            title=f"Negative sentences frequency distribution"
        )

        tweets.print_most_negative_tweets(5)
        tweets.print_most_positive_tweets(5)
        tweets.print_statistics_about_sentiment_score()

    sentiment_scores = []

    for prefix in DATASET_PREFIXES:
        tweetsCollection = TweetsCollection(prefix, DATASET_COLUMNS)
        tweetsCollection.preprocess_collection('content')
        tweetsCollection.calculate_sentiment_scores('content')
        sentiment_scores.append(
            tweetsCollection.get_mean_sentiment_scores_with_date())

    plotter.plot_sentiment_scores_comparision(
        sentiment_scores=sentiment_scores,
        colors=COMPARISION_COLORS.copy(),
        legend=DATASET_PREFIXES
    )

    plotter.plot_sentiment_scores_comparision_diff(
        sentiment_scores=tuple(sentiment_scores),
        colors=COMPARISION_COLORS.copy(),
    )


if __name__ == '__main__':
    main()
