# -*- coding: utf-8 -*-
import os
import sys
import time
import subprocess
import requests

sys.stdout.reconfigure(encoding='utf-8')

# 1. Pull file cleanly in binary
with open("exact_cached_photo.jpg", "wb") as f:
    subprocess.run([
        'adb', '-s', 'R5CW82ECF6M', 'exec-out', 'run-as', 'com.example.smart_note_app',
        'cat', 'cache/1be1ebe6-a2c0-4d00-a0f5-7c6c6d28c050/2f9ce55b-cc5f-42f3-9026-f2d20166aa1d-1_all_2579.jpg'
    ], stdout=f)

size = os.path.getsize("exact_cached_photo.jpg")
print(f"Pulled file size: {size} bytes")

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
user_id = 'ErK4vw39LCYupNj0CEhjJJvQ70a2'

url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"
print(f"Uploading to: {url}")
print(f"Preset: {upload_preset}")
print(f"Folder: smart_note/{user_id}/images")

start_t = time.time()
with open("exact_cached_photo.jpg", "rb") as f:
    files = {'file': ('2f9ce55b-cc5f-42f3-9026-f2d20166aa1d-1_all_2579.jpg', f, 'image/jpeg')}
    data = {
        'upload_preset': upload_preset,
        'folder': f'smart_note/{user_id}/images'
    }
    try:
        resp = requests.post(url, files=files, data=data, timeout=30)
        dur = time.time() - start_t
        print(f"Finished in: {dur:.2f} seconds")
        print(f"HTTP Status: {resp.status_code}")
        print(f"Response: {resp.text[:300]}")
    except Exception as e:
        dur = time.time() - start_t
        print(f"Failed after {dur:.2f} seconds with exception: {type(e).__name__}: {e}")
