import requests
import functions_framework
from google.cloud import storage
import pandas as pd
import datetime
import os
import io

def json_to_parquet(data) -> io.BytesIO:
    df = pd.json_normalize(data, sep="_")
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    return buffer

def upload_to_gcs(project_name, bucket_name, blob_name, buffer):
    storage_client = storage.Client(project=project_name)
    bucket = storage_client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(buffer)
    return
    

@functions_framework.http
def export_and_load(request):
    limit = os.getenv("BIKE_API_LIMIT", "50") 
    url = f'https://portail-api-data.montpellier3m.fr/bikestation?limit={limit}'
    project_name = os.getenv("PROJECT_NAME", "montpellier-bike-data-pipeline")
    bucket_name = os.getenv("BUCKET_NAME", "montpellier-bike-data")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
        parquet = json_to_parquet(data)
        
        now = datetime.datetime.now()
        blob_name = f"raw-bikes/{now.strftime('%Y/%m/%d')}/bikes_{now.strftime('%H%M')}.parquet"
        
        upload_to_gcs(project_name, bucket_name, blob_name, parquet)
        
        return f"Success: {blob_name}", 200
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return f"API Connection Error", 502
    
    except Exception as exc:
        return f"Error: {str(exc)}", 500
    
    
