import json

from ingestion.src.storage import save_raw_data

def test_save_raw_data_creates_json_file(tmp_path):

    test_data = {
        "metadata": {
            "source": "test",
            "record_count": 1
        },
        "data": [
            {
                "VehicleNumber": "TEST001",
                "Lines": "100"
            }
        ]
    }

    file_path = save_raw_data(
        test_data,
        base_directory=tmp_path
    )

    assert file_path.exists()
    assert file_path.suffix == ".json"

    with open(file_path, "r", encoding="utf-8") as file:
        saved_data = json.load(file)

    assert saved_data == test_data