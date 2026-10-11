import sqlite3

def check(name, db_path):
    print(f"=== {name} ({db_path}) ===")
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT id, title, status, is_synced, updated_at FROM notes WHERE title LIKE '%FN40%'")
        rows = cur.fetchall()
        for r in rows:
            print(f"  id={r[0][:8]}... | title={r[1]} | status={r[2]} | is_synced={r[3]} | updated_at={r[4]}")
        
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        print("  tables:", [t[0] for t in cur.fetchall()])
        conn.close()
    except Exception as e:
        print("  Error:", e)

check("DEV_A", "tools/dev_a.db")
check("DEV_B", "tools/dev_b.db")
