import sqlite3

conn = sqlite3.connect("challenge_gold.db")
conn.execute('CREATE TABLE input_text (index int AUTO INCREMENT NOT NULL, text_input varchar(50000), clean_text varchar(50000));')
conn.execute('CREATE TABLE input_file (index int AUTO INCREMENT NOT NULL, Tweet varchar(50000), clean_tweet varchar(50000));')
result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for row in result:
    print(row)
conn.close()