import subprocess, base64, json, sqlite3

proc = subprocess.Popen(['adb', '-s', 'R5CW82ECF6M', 'exec-out', 'run-as', 'com.example.smart_note_app', 'base64', 'databases/smart_note.db'], stdout=subprocess.PIPE)
data, _ = proc.communicate()
open('tools/chk_dev_a.db', 'wb').write(base64.b64decode(data))

conn = sqlite3.connect('tools/chk_dev_a.db')
cur = conn.cursor()
cur.execute("SELECT id, title, content, is_synced, updated_at FROM notes WHERE title LIKE '%checklist%' ORDER BY updated_at DESC LIMIT 1")
row = cur.fetchone()
if row:
    print('ID:', row[0])
    print('Title:', row[1])
    print('Content JSON:', row[2])
    print('Is Synced:', row[3])
conn.close()
