from flask import Flask, request, jsonify
import re
from unidecode import unidecode
import pandas as pd
import sqlite3
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

swagger_template = dict(
info = {
    'title' : LazyString(lambda: 'Swagger Clean Text'),
    'version' : LazyString(lambda: '1'),
    'description' : LazyString(lambda: 'Clean text from random enters, emojis and punctuations'),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    'headers': [],
    'specs': [
        {
            "endpoint":'docs',
            "route":'/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path":"/flassger_static",
    "swagger_ui": True,
    "specs_route":"/docs/"
}

swagger_text = Swagger(app, template=swagger_template, config=swagger_config)

def _remove_emoji(s):
    s=s.encode('ascii', 'ignore').decode('utf-8')
    return s

def _remove_punct(s):
    return re.sub(r"[^\w\d\s]+", "",s)

def _remove_enter(s):
    return re.sub(r'\n', ' ', s)

def _remove_spaces(s):
    return re.sub(' +', ' ', s)

@swag_from("swagger_config.yml", methods=['POST'])
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

# Swagger for File
def _remove_emoji_file(text):
    return re.sub(r"\\x[A-Za-z0-9./]+", "",unidecode(text))

def _remove_enter_file(text):
    return re.sub(r"(?<!\\)(\\\\)*\\n|\n", ' ',unidecode(text))

def _remove_spaces_file(text):
    return re.sub(' +', ' ',text)

def _remove_punct_file(text):
    return re.sub(r"[^\w\d\s]+", "",text)

@swag_from("swagger_config.yml", methods=['POST'])
@app.route("/clean_file/v1", methods=['POST'])
def file_cleansing():
    file = request.files['file']
    df = pd.read_csv(file, encoding="latin-1")
    
    conn = sqlite3.connect('challenge_gold.db') 
    df.to_sql('input_file_dirty', con=conn, if_exists='append')
    conn.close()    

    df['clean_tweet'] = df['Tweet'].apply(_remove_emoji_file)
    df['clean_tweet'] = df['clean_tweet'].apply(_remove_enter_file)
    df['clean_tweet'] = df['clean_tweet'].apply(_remove_spaces_file)
    df['clean_tweet'] = df['clean_tweet'].apply(_remove_punct_file)  
    df_clean = df[["Tweet", "clean_tweet"]]

    conn = sqlite3.connect('challenge_gold.db') 
    df_clean.to_sql('file_clean', con=conn, if_exists='append')
    conn.close()    

    return jsonify("Successfully saved data to DB")

if __name__ == "__main__":
    app.run(port=2410, debug=True)