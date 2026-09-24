import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

def save_raw_data(data, base_directory=None):
    now = datetime.now()

    if base_directory is None:
        base_directory = PROJECT_ROOT / "data" / "raw"

    output_directory = (
            base_directory
            / "vehicle_positions"
            / f"year={now:%Y}"
            / f"month={now:%m}"
            / f"day={now:%d}"
            / f"hour={now:%H}"
    )

    output_directory.mkdir(parents=True, exist_ok=True)

    filename = f"vehicles_{now:%Y%m%d_%H%M%S}.json"

    file_path = output_directory / filename

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    return file_path
