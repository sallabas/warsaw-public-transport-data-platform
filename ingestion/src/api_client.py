import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from ingestion.src.storage import save_raw_data

from datetime import datetime, timezone

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ingestion.src.logger import get_logger


# Configuration ------>
logger = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)

API_KEY = os.getenv("WARSAW_API_KEY")
API_URL = "https://api.um.warszawa.pl/api/action/busestrams_get"

params = {
    "resource_id": "f2e5503e-927d-4ad3-9500-4ab9e55deb59",
    "apikey": API_KEY,
    "type": 1
}

# Retry Strategy ----------->
retry_strategy = Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"],
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)

# 1. function for Data Fetching from API ---------->

def fetch_vehicle_position():
    logger.info("Starting Warsaw Transport Ingestion")


    response = session.get(
        API_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if data.get("result") == "false":
        error_message = data.get("error", "Unknown API error")
        raise ValueError(f"Warsaw API error: {error_message}")

    vehicles = data["result"]

    if not isinstance(vehicles, list):
        raise ValueError(f"Unexpected API response format: 'result' is not a list")

    return vehicles

# 2. function Run Ingestion ---------->

def run_ingestion():
    logger.info("Starting Warsaw Transport Ingestion")
    vehicles = fetch_vehicle_position()

    logger.info("Number of vehicles: %s", len(vehicles))

    if vehicles:
        logger.info("First vehicle: %s", vehicles[0])
    else:
        logger.info("No vehicles returned")

    raw_snapshot = {
        "metadata": {
            "source": "Warsaw Public Transport API",
            "dataset": "vehicle_positions",
            "vehicle_type": "bus",
            "ingestion_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "record_count": len(vehicles),
        },
        "data": vehicles
    }

    file_path = save_raw_data(raw_snapshot)

    logger.info("Raw data saved to: %s", file_path)
    logger.info("Ingestion completed successfully")

# Application Entry Point --------->
if __name__ == "__main__":
    try:
        run_ingestion()

    except requests.RequestException as exc:
        logger.error("HTTP request failed: %s", exc)

    except ValueError as exc:
        logger.error("Data validation failed: %s", exc)

    except Exception as exc:
        logger.exception("Unexpected error: %s", exc)