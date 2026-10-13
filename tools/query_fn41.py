import sqlite3

for name, db_path in [('DEV_A', 'tools/dev_a.db'), ('DEV_B', 'tools/dev_b.db')]:
    print(f"=== {name} ===")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, status, is_synced, updated_at FROM notes WHERE title LIKE '%FN41%' ORDER BY updated_at DESC")
    for r in cur.fetchall():
        print(f"  id={r[0][:8]} | title={r[1]} | status={r[3]} | is_synced={r[4]} | updated_at={r[5]}")
        print(f"    content={r[2]}")
    conn.close()
