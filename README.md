# Warsaw Public Transport Data Platform

A data engineering project built around real-time public transport data from Warsaw.

The goal is to build an end-to-end data pipeline that collects vehicle data from the Warsaw Public Transport API, stores historical snapshots, processes the data in Azure, and makes it available for analysis.

The project is being developed incrementally, starting with a local Python ingestion service and gradually moving the pipeline to Azure.

## Architecture

The planned architecture is:

```text
Warsaw Public Transport API
            |
            v
      Python Ingestion
            |
            v
 Azure Data Lake Storage
            |
            v
   Azure Data Factory
            |
            v
 Azure Databricks / PySpark
            |
            v
        Delta Lake
            |
            v
        Azure SQL
            |
            v
        Power BI
```

Terraform will be used for infrastructure provisioning and GitHub Actions for CI/CD.

## Project Status

### Phase 1 - Local Data Ingestion

Phase 1 is complete.

The current implementation retrieves live vehicle positions from the Warsaw API and stores them locally as timestamped JSON snapshots.

The ingestion layer currently includes:

- API authentication using environment variables
- HTTP timeout handling
- Retry logic for temporary API failures
- API response validation
- Application logging
- Exception handling
- Ingestion metadata
- Partitioned raw JSON storage
- Unit tests with pytest
- Mocked API calls for testing

Current flow:

```text
Warsaw API
    |
    v
Python API Client
    |
    v
Response Validation
    |
    v
Metadata
    |
    v
Raw JSON Storage
```

## Project Structure

```text
warsaw-public-transport-data-platform/
|
├── ingestion/
│   ├── src/
│   │   ├── api_client.py
│   │   ├── logger.py
│   │   └── storage.py
│   │
│   └── tests/
│       ├── test_api_client.py
│       └── test_storage.py
│
├── data/
│   └── raw/
│
├── databricks/
├── docs/
├── monitoring/
├── sql/
├── terraform/
│
├── requirements.txt
├── .gitignore
└── README.md
```

Raw API data, virtual environments, IDE files and environment variables are excluded from version control.

## Data Ingestion

The ingestion service requests current vehicle positions from the Warsaw Public Transport API.

Each successful run creates a new snapshot instead of overwriting the previous one. This allows the project to build a historical dataset from live vehicle data.

Each snapshot contains ingestion metadata and the original API records.

Example:

```json
{
  "metadata": {
    "source": "Warsaw Public Transport API",
    "dataset": "vehicle_positions",
    "vehicle_type": "bus",
    "ingestion_timestamp_utc": "2026-09-24T18:30:00+00:00",
    "record_count": 1000
  },
  "data": [
    {
      "Lines": "190",
      "Lon": "21.0123",
      "VehicleNumber": "1234",
      "Time": "2026-09-24 20:29:00",
      "Lat": "52.2297",
      "Brigade": "1"
    }
  ]
}
```

No transformations are applied at this stage. The raw response is preserved so that cleaning and transformation can be handled separately later in the pipeline.

## Raw Data Storage

Snapshots are organized by ingestion time:

```text
data/raw/vehicle_positions/
└── year=2026/
    └── month=09/
        └── day=24/
            └── hour=20/
                └── vehicles_20260924_203000.json
```

The same general structure will later be used when the raw layer is moved to Azure Data Lake Storage.

## Reliability

The API client uses a timeout so that the ingestion process does not wait indefinitely for a response.

Temporary HTTP errors are handled with retries. The current retry configuration covers:

```text
429
500
502
503
504
```

The response is also validated before anything is written to storage.

This is important because the Warsaw API can return an HTTP 200 response while still containing an API-level error in the response body.

## Tests

Tests are written with `pytest`.

The current tests cover:

- Successful API responses
- HTTP errors
- API-level errors
- Unexpected response formats
- Raw JSON file creation

API requests are mocked during testing, so the test suite does not depend on the external API being available.

Run the tests with:

```bash
pytest ingestion/tests/ -v
```

Current Phase 1 test suite:

```text
5 passed
```

## Running Locally

Clone the repository:

```bash
git clone https://github.com/sallabas/warsaw-public-transport-data-platform.git
cd warsaw-public-transport-data-platform
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
WARSAW_API_KEY=your_api_key_here
```

Run the ingestion:

```bash
python -m ingestion.src.api_client
```

The generated snapshots will be stored under:

```text
data/raw/vehicle_positions/
```

## Roadmap

| Phase | Scope | Status |
|---|---|---|
| 1 | Local Python ingestion | Complete |
| 2 | Azure Data Lake Storage Gen2 | Next |
| 3 | Azure Data Factory | Planned |
| 4 | Databricks, PySpark and Delta Lake | Planned |
| 5 | Azure SQL | Planned |
| 6 | Power BI | Planned |
| 7 | Terraform and GitHub Actions | Planned |
| 8 | Monitoring and documentation | Planned |

## Technology Stack

Current:

- Python
- Requests
- Pytest
- Git

Planned:

- Azure Data Lake Storage Gen2
- Azure Data Factory
- Azure Databricks
- PySpark
- Delta Lake
- Azure SQL
- Power BI
- Terraform
- GitHub Actions
- Azure Monitor

## Next Step

Phase 2 will move the raw storage layer from the local filesystem to Azure Data Lake Storage Gen2.

The current pipeline:

```text
Warsaw API -> Python -> Local Raw Storage
```

will become:

```text
Warsaw API -> Python -> Azure Data Lake Storage Gen2
```

The existing partitioning structure will be kept so that the cloud storage layout remains consistent with the local implementation.