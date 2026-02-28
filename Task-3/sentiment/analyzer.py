"""Sentiment analysis using NLTK's VADER lexicon."""

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download lexicon only if missing (avoids repeated network calls)
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon", quiet=True)

sia = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> str:
    """Return 'positive', 'negative', or 'neutral' for the given text."""
    scores = sia.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.3:
        return "positive"
    elif compound <= -0.3:
        return "negative"
    return "neutral"


if __name__ == "__main__":
    # Quick smoke-test (only runs when executed directly)
    print(analyze_sentiment("I'm really disappointed in this service."))
    print(analyze_sentiment("Thanks, it was very helpful!"))


