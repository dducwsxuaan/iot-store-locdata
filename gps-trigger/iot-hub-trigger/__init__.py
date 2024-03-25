from typing import List
import logging

import azure.functions as func
import json
import os
import uuid
from azure.storage.blob import BlobServiceClient, PublicAccess
app = func.FunctionApp()

def main(event: func.EventHubEvent, outputblob: func.Out[str]):
    logging.info('Python EventHub trigger processed an event: %s',
                 event.get_body().decode('utf-8'))
    
    device_id = event.iothub_metadata['connection-device-id']
    blob_name = f'{device_id}/{str(uuid.uuid1())}.json'
    event_body = json.loads(event.get_body().decode('utf-8'))
    blob_body = {
    'device_id' : device_id,
    'timestamp' : event.iothub_metadata['enqueuedtime'],
    'gps': event_body['gps']
}
    logging.info(f'Writing blob to {blob_name} - {blob_body}')
    outputblob.set(json.dumps(blob_body).encode('utf-8'))
    
