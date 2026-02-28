import os
import logging
from flask import Flask, render_template
from analytics_utils import load_data, total_queries, most_common_topics, average_satisfaction

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Resolve CSV path relative to this file so it works regardless of CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "customer_service_interactions.csv")


@app.route("/")
def dashboard():
    """Render the analytics dashboard with current CSV data."""
    try:
        df = load_data(CSV_PATH)
        total = total_queries(df)
        topics = most_common_topics(df)
        avg_rating = average_satisfaction(df)
    except Exception as exc:
        logger.exception("Failed to load analytics data: %s", exc)
        total = 0
        topics = {}
        avg_rating = 0

    return render_template(
        "dashboard.html",
        total=total,
        topics=topics,
        avg_rating=avg_rating,
    )


@app.route("/health")
def health():
    """Simple health-check endpoint."""
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
