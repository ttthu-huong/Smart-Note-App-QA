# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

keywords = ['exception', 'timeout', 'socket', 'handshake', 'failed', 'cloudinary', 'upload', 'error', 'refused', 'reset']

with open("upload_realtime_logcat.txt", "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        lower = line.lower()
        if any(k in lower for k in ['smart_note', 'cloudinary', 'imagepicker', 'photopicker', 'flutter']):
            if any(k in lower for k in ['error', 'fail', 'exception', 'warn', 'upload', 'image', 'response']):
                print(line.strip()[:180])
