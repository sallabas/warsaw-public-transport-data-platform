from unittest.mock import Mock, patch

from ingestion.src.azure_storage import upload_file_to_adls


@patch("ingestion.src.azure_storage.get_service_client")
def test_upload_file_to_adls(mock_get_service_client, tmp_path):
    # Fake local file
    local_file = tmp_path / "test.json"
    local_file.write_text('{"test": true}', encoding="utf-8")

    # Mock Azure clients
    mock_service_client = Mock()
    mock_file_system_client = Mock()
    mock_file_client = Mock()

    mock_get_service_client.return_value = mock_service_client

    mock_service_client.get_file_system_client.return_value = (
        mock_file_system_client
    )

    mock_file_system_client.get_file_client.return_value = (
        mock_file_client
    )

    remote_path = "vehicle_positions/year=2026/test.json"

    result = upload_file_to_adls(
        local_file_path=local_file,
        remote_file_path=remote_path
    )

    mock_service_client.get_file_system_client.assert_called_once_with(
        file_system="bronze"
    )

    mock_file_system_client.get_file_client.assert_called_once_with(
        remote_path
    )

    mock_file_client.upload_data.assert_called_once()

    assert result == remote_path