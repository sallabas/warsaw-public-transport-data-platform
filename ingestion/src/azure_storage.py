from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

STORAGE_ACCOUNT_NAME = "stwarsawtransportdev"
CONTAINER_NAME = "bronze"

ACCOUNT_URL = (
    "https://stwarsawtransportdev.dfs.core.windows.net"
)

def get_service_client():
    credential = DefaultAzureCredential()
    service_client = DataLakeServiceClient(
        account_url=ACCOUNT_URL,
        credential=credential,
    )

    return service_client

def upload_file_to_adls(local_file_path, remote_file_path):
    service_client = get_service_client()

    file_system_client = service_client.get_file_system_client(
        file_system=CONTAINER_NAME
    )

    file_client = file_system_client.get_file_client(
        remote_file_path
    )

    with open(local_file_path, "rb") as local_file:
        file_client.upload_data(
            local_file,
            overwrite=True
        )

    return remote_file_path

def test_connection():
    service_client = get_service_client()
    file_system_client = service_client.get_file_system_client(
        file_system=CONTAINER_NAME
    )

    properties = file_system_client.get_file_system_properties()


    print("Connected successfully.")
    print(f"Container: {CONTAINER_NAME}")
    print(f"Last modified: {properties['last_modified']}")

if __name__ == "__main__":
    test_connection()