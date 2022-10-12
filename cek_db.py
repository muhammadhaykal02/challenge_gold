import sqlite3
import pandas as pd

conn = sqlite3.connect("challenge_gold.db")
sql = "SELECT * FROM input_file;"
df_tweet = pd.read_sql(sql, conn)
conn.close()
df_tweet