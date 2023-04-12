#!/usr/bin/env python3
import base64
import json

import requests
import os
from datetime import datetime

VICTOR_OPS_API = "Replace with Victor Ops integration URL"

TEMPLATE = """
**scoping_project_id:** {scoping_project_id} '\n'
**started_at:** {started_at} '\n'
**resource_name:** {resource_name} '\n'
**url:** {url}'\n'
**Summary:** {summary}'\n'
"""


def send_victor_ops_notification(event, context):
    print("EVENT=", event) #Prints the event dictionary in to GCP logs for cloud function for debuging purpose 
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message_json = json.loads(pubsub_message)
    incident = message_json["incident"]
    ts = int(incident["started_at"])

    requests.post(
        VICTOR_OPS_API,
        json={
            "message_type": "CRITICAL",
            "entity_display_name": "Subject of the alert",
            "state_message": TEMPLATE.format(
                scoping_project_id=incident["scoping_project_id"],                            
                started_at=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),               
                resource_name=incident["resource_name"],
                url=incident["url"],
                summary=incident["summary"] 
            ),
        },
        
    )
