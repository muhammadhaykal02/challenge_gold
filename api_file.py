from flask import Flask, request, jsonify
import pandas as pd
import re
from unidecode import unidecode
import sqlite3

app = Flask(__name__)

def decode(text):
  return unidecode(text)

def _remove_enter(text):
    return re.sub(r"(?<!\\)(\\\\)*\\n|\n", ' ',unidecode(text))

def _remove_emoji(text):
    return re.sub(r"\\x[A-Za-z0-9./]+", "",unidecode(text))

def _remove_punct(text):
    return re.sub(r"[^\w\d\s]+", "",text)

def _remove_spaces(text):
    return re.sub(' +', ' ',text)

@app.route("/clean_file/v1", methods=['POST'])
def file_cleansing():
    file = request.files['file']
    df = pd.read_csv(file, encoding="latin-1")
    
    conn = sqlite3.connect('challenge_gold.db') 
    df.to_sql('input_file_dirty', index=False, con=conn, if_exists='append')
    conn.close()    

    df['clean_tweet'] = df['Tweet'].apply(_remove_emoji)
    df['clean_tweet'] = df['clean_tweet'].apply(_remove_enter)
    df['clean_tweet'] = df['clean_tweet'].apply(_remove_spaces)
    df['clean_tweet'] = df['clean_tweet'].apply(_remove_punct)  
    df_clean = df[["Tweet", "clean_tweet"]]

    conn = sqlite3.connect('challenge_gold.db') 
    df_clean.to_sql('file_clean', index=False, con=conn, if_exists='append')
    conn.close()    

    return jsonify("Successfully saved data to DB")

if __name__ == "__main__":
    app.run(port=2411, debug=True)