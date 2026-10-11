# -*- coding: utf-8 -*-
import subprocess
import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("smart_note_clean.db", "wb") as f:
    subprocess.run(['adb', '-s', 'R5CW82ECF6M', 'exec-out', 'run-as', 'com.example.smart_note_app', 'cat', 'databases/smart_note.db'], stdout=f)

conn = sqlite3.connect("smart_note_clean.db")
c = conn.cursor()

print("--- SCHEMA OF notes ---")
for row in c.execute("PRAGMA table_info(notes);"):
    print(row)

print("\n--- ALL NOTES IN DB ---")
for row in c.execute("SELECT id, title, is_pinned, is_archived, in_trash, tags, image_urls, audio_urls, content FROM notes;"):
    print(f"ID: {row[0]}")
    print(f"  Title: {row[1]}")
    print(f"  Pinned: {row[2]} | Archived: {row[3]} | Trash: {row[4]}")
    print(f"  Tags: {row[5]}")
    print(f"  Images: {row[6]}")
    print(f"  Audios: {row[7]}")
    print(f"  Content: {row[8][:50]}...")
    print("-" * 40)
