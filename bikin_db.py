import sqlite3

conn = sqlite3.connect("challenge_gold.db")
result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for row in result:
    print(row)
conn.close()