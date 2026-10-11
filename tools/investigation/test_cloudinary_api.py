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
upload_preset = env_vars.get('CLOUDINARY_UPLOAD_PRESET')

print(f"Testing Cloudinary Direct API:")
print(f"Cloud Name: {cloud_name}")
print(f"Upload Preset: {upload_preset}")
print(f"URL: https://api.cloudinary.com/v1_1/{cloud_name}/image/upload")

url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"

# Create a tiny 1x1 png in memory
import base64
tiny_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")

files = {'file': ('test.png', tiny_png, 'image/png')}
data = {
    'upload_preset': upload_preset,
    'folder': 'smart_note/test_user/images'
}

try:
    resp = requests.post(url, files=files, data=data, timeout=15)
    print(f"\nResponse HTTP Status: {resp.status_code}")
    print(f"Response Body: {resp.text}")
except Exception as e:
    print(f"\nRequest failed with exception: {e}")
