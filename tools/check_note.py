import subprocess
import sqlite3
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

cmd = ['adb', '-s', 'R5CW82ECF6M', 'exec-out', 'run-as', 'com.example.smart_note_app', 'cat', '/data/data/com.example.smart_note_app/databases/smart_note.db']
with open('evidence/fn13_14_21_22_run_20261011_0055/smart_note.db', 'wb') as f:
    subprocess.run(cmd, stdout=f)

conn = sqlite3.connect('evidence/fn13_14_21_22_run_20261011_0055/smart_note.db')
cur = conn.cursor()

title_filter = sys.argv[1] if len(sys.argv) > 1 else 'NOTE_TAG_TEST'
cur.execute(f"SELECT id, title, status, tags, image_urls, reminder FROM notes WHERE title LIKE '%{title_filter}%'")
rows = cur.fetchall()
for r in rows:
    print(f"ID: {r[0]} | Title: {r[1]} | Status: {r[2]} | Tags: {r[3]} | Images: {r[4]} | Reminder: {r[5]}")

conn.close()
