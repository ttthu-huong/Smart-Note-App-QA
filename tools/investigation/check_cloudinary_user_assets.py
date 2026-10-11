# -*- coding: utf-8 -*-
import os
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

env_path = r"D:\Workspace\TBDD\Smart-Note-App-QA\.env"
env_vars = {}
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env_vars[k.strip()] = v.strip()

cloud_name = env_vars.get('CLOUDINARY_CLOUD_NAME')
api_key = env_vars.get('CLOUDINARY_API_KEY')
api_secret = env_vars.get('CLOUDINARY_API_SECRET')
user_id = 'ErK4vw39LCYupNj0CEhjJJvQ70a2'

url = f"https://api.cloudinary.com/v1_1/{cloud_name}/resources/image"
params = {
    'prefix': f'smart_note/{user_id}',
    'max_results': 10
}

resp = requests.get(url, params=params, auth=(api_key, api_secret))
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    resources = data.get('resources', [])
    print(f"Found {len(resources)} resources for user {user_id}:")
    for r in resources:
        print(f"  Public ID: {r.get('public_id')} | Created: {r.get('created_at')} | Bytes: {r.get('bytes')}")
else:
    print(f"Error: {resp.text}")
