from flask import Flask, request, jsonify
import re
from unidecode import unidecode
import sqlite3

app = Flask(__name__)

def _remove_emoji(s):
    s=s.encode('ascii', 'ignore').decode('utf-8')
    return s

def _remove_punct(s):
    return re.sub(r"[^\w\d\s]+", "",s)

def _remove_enter(s):
    return re.sub(r'\n', ' ', s)

def _remove_spaces(s):
    return re.sub(' +', ' ', s)


@app.route("/clean_text/v1", methods=['POST'])
def text_cleansing():
    s = request.get_json()

    non_emoji = _remove_emoji(s['text'])
    non_punct = _remove_punct(non_emoji)
    no_new_line = _remove_enter(non_punct)
    remove_space = _remove_spaces(no_new_line)

    conn = sqlite3.connect("challenge_gold.db")
    conn.execute("INSERT INTO input_text (text_input, clean_text) values (?, ?)", (s['text'], remove_space))
    conn.commit()
    conn.close()

    return jsonify({"hasil_bersih":remove_space})

if __name__ == "__main__":
    app.run(port=2410, debug=True)