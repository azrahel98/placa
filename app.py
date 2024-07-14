from flask import Flask, request, jsonify
from db import Database 
import os
from placa import verificar
import io
import numpy as np
import cv2

app = Flask(__name__)

db = Database()


@app.route('/login',methods=["POST"])
def login():
    con = db.get_connection()
    curs = con.cursor()
    curs.execute("Select nickname from Usuario")
    res = curs.fetchall()
    db.close_connection(con)
    db.query("select * from Usuario")
    return jsonify(res)


@app.route('/check',methods=['POST'])
def check():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    verificar(file)

    return jsonify({'message': 'File uploaded successfully'}), 200


@app.route('/test', methods=['GET'])
def test_connection():
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Placas")
    results = cursor.fetchall()
    db.close_connection(connection)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)