import sqlite3

conn = sqlite3.connect("challenge_gold.db")
conn.execute('CREATE TABLE input_text (text_input varchar(50000), clean_text varchar(50000));')
conn.execute('CREATE TABLE input_file_dirty (Tweet varchar(50000), HS int,Abusive int, HS_Individual int, HS_Group int, HS_Religion int, HS_Race int, HS_Physical int, HS_Gender int, HS_Other int, HS_Weak int, HS_Moderate int, HS_Strong int, clean_tweet varchar(50000));')
conn.execute('CREATE TABLE file_clean (Tweet varchar(50000), clean_tweet varchar(50000));')
result = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for row in result:
    print(row)
conn.close()