# Montpellier Bike Data Pipeline

A fully automated data pipeline for collecting, processing, and visualizing real-time bike availability data from Montpellier's bike-sharing system.

## Architecture

This project implements an end-to-end data pipeline using Google Cloud Platform and modern data engineering tools:

```
Cloud Scheduler → Cloud Function → GCS → BigQuery → dbt → Power BI
```

### Pipeline Components

1. **Cloud Scheduler**: Triggers the data collection process at regular intervals
2. **Cloud Function**: Fetches bike availability data from the Montpellier bike-sharing API
3. **Google Cloud Storage (GCS)**: Stores raw data files
4. **Scheduled Transfer Service**: Automatically transfers data from GCS to BigQuery
5. **BigQuery**: Data warehouse for storing raw and transformed data
6. **dbt (Data Build Tool)**: Transforms raw data into analytics-ready models
7. **Power BI**: Interactive dashboard for data visualization

## Project Structure

```
.
├── cloud_functions/          # Cloud Function code
│   ├── main.py              # Function entry point
│   └── requirements.txt     # Python dependencies
├── dbt_project/             # dbt transformation project
│   ├── models/
│   │   ├── staging/         # Staging layer
│   │   │   ├── stg_bikes.sql       # Staging view for bike data
│   │   │   └── src_bikes.yml       # Source definitions
│   │   └── marts/           # Analytics layer
│   │       ├── bike_availability.sql  # Mart table for bike availability
│   │       └── marts.yml            # Model documentation
│   ├── macros/
│   │   └── generate_schema_name.sql
│   └── dbt_project.yml      # dbt configuration
└── pyproject.toml           # Python project configuration
```

## Data Flow

### 1. Data Collection

- **Cloud Scheduler** triggers a Cloud Function on a regular schedule
- **Cloud Function** fetches current bike availability data from the Montpellier API
- Raw data is stored in **Google Cloud Storage**

### 2. Data Ingestion

- **Scheduled Transfer Service** automatically loads data from GCS to BigQuery
- Data lands in a raw staging area in BigQuery

### 3. Data Transformation (dbt)

- **Staging Layer** (`stg_bikes`): Creates a cleaned view of raw bike data
  - Standardizes column names
  - Applies data type conversions
  - Handles null values
- **Marts Layer** (`bike_availability`): Creates analytics-ready table
  - Aggregates bike availability metrics
  - Adds business logic
  - Optimized for dashboard queries

### 4. Visualization

- **Power BI** connects to BigQuery mart tables
- Interactive dashboard provides real-time insights into:
  - Current bike availability
  - Station usage patterns
  - Historical trends
  - Geographic distribution

## Setup

### Prerequisites

- Google Cloud Platform account with billing enabled
- Python 3.9+
- dbt installed
- Power BI Desktop

### GCP Configuration

1. Create a GCP project
2. Enable required APIs:
   - Cloud Functions
   - Cloud Scheduler
   - Cloud Storage
   - BigQuery
3. Set up service account with appropriate permissions

### Cloud Function Deployment

```bash
cd cloud_functions
gcloud functions deploy fetch-bike-data \
  --runtime python312 \
  --trigger-http \
  --entry-point name_of_function \
  --region europe-west9
```

### Cloud Scheduler Setup

```bash
gcloud scheduler jobs create http bike-data-job \
  --schedule="*/20 * * * *" \
  --uri="YOUR_FUNCTION_URL" \
  --http-method=GET
```

### dbt Setup

```bash
cd dbt_project
dbt run
dbt test
```

## Development

### Running dbt Locally

```bash
# Navigate to dbt project
cd dbt_project

# Run all models
dbt run

# Run specific models
dbt run --select staging.*
dbt run --select marts.*

# Test data quality
dbt test
```

### Virtual Environment

```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -e .
```

## Monitoring

- Monitor Cloud Function logs in GCP Console
- Check BigQuery transfer jobs status
- Review dbt run results in `dbt_project/logs/`
- Track data freshness in Power BI

## License

This project is licensed under the MIT License.

## Acknowledgments

- Data provided by Montpellier bike-sharing system API
- Built with Google Cloud Platform, dbt, and Power BI
