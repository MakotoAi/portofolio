import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = MongoClient(os.getenv("MONGO_URI"))  # URI diambil dari file .env
db = client['dbsparta']  # Nama database
messages_collection = db['messages']  # Nama koleksi

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('about.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Simpan data ke MongoDB
    messages_collection.insert_one({
        "name": name,
        "email": email,
        "message": message
    })

    return jsonify({"status": "success", "message": "Message sent successfully"})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True, threaded=False)