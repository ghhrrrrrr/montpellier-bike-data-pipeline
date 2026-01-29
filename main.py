import requests
import functions_framework
from google.cloud import storage
import json 
import datetime
import os

@functions_framework.http
def export_and_load(request):
    limit = os.getenv("BIKE_API_LIMIT", "50") 
    url = f'https://portail-api-data.montpellier3m.fr/bikestation?limit={limit}'
    bucket_name = os.getenv("BUCKET_NAME", "montpellier-bike-data")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        data = response.json()
        
    except Exception as exc:
        return f"Failed to retrieve data: {exc}", 500

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        now = datetime.datetime.now()
        blob_name = f"raw-bikes/{now.strftime('%Y/%m/%d')}/bikes_{now.strftime('%H%M')}.json"
        blob = bucket.blob(blob_name)

        with blob.open("w", encoding='utf-8') as f:
            for entry in data:
                f.write(json.dumps(entry) + '\n')

        return f"Created: {blob_name}", 200

    except Exception as exc:
        return f"Storage Error: {exc}", 500