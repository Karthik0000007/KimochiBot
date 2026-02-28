"""Utility functions for loading and analysing customer-service interaction data."""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def load_data(file: str = "customer_service_interactions.csv") -> pd.DataFrame:
    """Load interaction CSV, coerce satisfaction to numeric, drop invalid rows."""
    try:
        df = pd.read_csv(file)
        df["satisfaction"] = pd.to_numeric(df["satisfaction"], errors="coerce")
        return df.dropna(subset=["satisfaction"])
    except FileNotFoundError:
        logger.error("CSV file not found: %s", file)
        return pd.DataFrame()
    except Exception as exc:
        logger.exception("Error loading data: %s", exc)
        return pd.DataFrame()


def total_queries(df: pd.DataFrame) -> int:
    """Return the total number of logged interactions."""
    return len(df) if not df.empty else 0


def most_common_topics(df: pd.DataFrame, top_n: int = 5) -> dict:
    """Return a dict of the *top_n* most common topics and their counts."""
    if not df.empty and "topic" in df.columns:
        return df["topic"].value_counts().head(top_n).to_dict()
    return {}


def average_satisfaction(df: pd.DataFrame) -> float:
    """Return the mean satisfaction score rounded to two decimals."""
    if not df.empty and "satisfaction" in df.columns:
        return round(df["satisfaction"].mean(), 2)
    return 0.0