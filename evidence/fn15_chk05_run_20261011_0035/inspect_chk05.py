import subprocess
import sqlite3
import json

db_path = 'evidence/fn15_chk05_run_20261011_0035/smart_note_chk05.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(notes)")
cols = [col[1] for col in cursor.fetchall()]
print("Columns in notes:", cols)

query = f"SELECT id, title, content, is_synced, updated_at FROM notes WHERE title = 'FN15_CHK05_Verify_Delete_Item'"
cursor.execute(query)
row = cursor.fetchone()

if row:
    print("NOTE FOUND:")
    print("ID:", row[0])
    print("Title:", row[1])
    print("Content JSON:", row[2])
    print("is_synced:", row[3])
    print("updated_at:", row[4])
    parsed = json.loads(row[2])
    print("Parsed checklist count:", len(parsed.get('items', [])))
    for i, it in enumerate(parsed.get('items', [])):
        print(f"  Item {i}: id={it.get('id')}, text='{it.get('text')}', checked={it.get('checked')}")
else:
    print("NOT FOUND")

conn.close()
