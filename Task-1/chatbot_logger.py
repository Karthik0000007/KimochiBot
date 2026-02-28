"""Logger for customer-service chatbot interactions, writing rows to a CSV file."""

import csv
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

LOG_FILE = "customer_service_interactions.csv"
_HEADER = ["timestamp", "user_id", "message", "response", "topic", "satisfaction"]


def log_interaction(
    user_id: str,
    message: str,
    response: str,
    topic: str,
    satisfaction: int | None = None,
) -> None:
    """Append a single interaction row to the CSV log file.

    Creates the file with a header row if it does not already exist.
    """
    log_exists = os.path.exists(LOG_FILE)
    try:
        with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not log_exists:
                writer.writerow(_HEADER)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                user_id,
                message,
                response,
                topic,
                satisfaction,
            ])
    except OSError as exc:
        logger.error("Failed to write interaction log: %s", exc)
