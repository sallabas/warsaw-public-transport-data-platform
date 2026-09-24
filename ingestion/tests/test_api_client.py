import pytest
import requests
from unittest.mock import patch, Mock
from ingestion.src.api_client import fetch_vehicle_position

# Successfull data fetching -------->
def test_fetch_vehicle_position_success():

    fake_vehicles = [
        {
            "VehicleNumber": "TEST001",
            "Lines": "100",
            "Lat": 52.2297,
            "Lon": 21.0122
        },
        {
            "VehicleNumber": "TEST002",
            "Lines": "200",
            "Lat": 52.2300,
            "Lon": 21.0150
        }
    ]


    mock_response = Mock()

    mock_response.json.return_value = {
        "result": fake_vehicles
    }

    with patch(
            "ingestion.src.api_client.session.get",
            return_value=mock_response
    ):
        vehicles = fetch_vehicle_position()

    assert len(vehicles) == 2
    assert vehicles == fake_vehicles

# Error code generation test --------->
def test_fetch_vehicle_positions_http_error():

    mock_response = Mock()

    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "500 Server Error"
    )

    with patch(
        "ingestion.src.api_client.session.get",
        return_value=mock_response
    ):
        with pytest.raises(requests.HTTPError):
            fetch_vehicle_position()

# Validations catch the error codes -------->
def test_fetch_vehicle_positions_invalid_format():

    mock_response = Mock()

    mock_response.json.return_value = {
        "result": {
            "message": "invalid format"
        }
    }

    with patch(
        "ingestion.src.api_client.session.get",
        return_value=mock_response
    ):
        with pytest.raises(
            ValueError,
            match="Unexpected API response format"
        ):
            fetch_vehicle_position()

# Success error code but error in the API ------>
def test_fetch_vehicle_positions_api_error():

    mock_response = Mock()

    mock_response.json.return_value = {
        "result": "false",
        "error": "Invalid API key"
    }

    with patch(
        "ingestion.src.api_client.session.get",
        return_value=mock_response
    ):
        with pytest.raises(
            ValueError,
            match="Warsaw API error"
        ):
            fetch_vehicle_position()