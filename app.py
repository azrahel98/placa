from flask import Flask, request, jsonify
from flask_cors import CORS
from db import Database
from placa import verificar
from jsonwebtoken import generate_jwt,token_required

app = Flask(__name__)
app.config['DEBUG'] = True 
CORS(app) 
db = Database()


@app.route('/login',methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    passw = data.get('password')
    if username == None or passw == None:
         return jsonify({'message': 'Campos incorrectos'}), 400
    con = db.get_connection()
    curs = con.cursor()
    curs.execute("select id,cast(aes_decrypt(pass,'olafmves') as char) pass from Usuario where nickname = %s",(username,))
    res = curs.fetchall()
    db.close_connection(con)
    
    if len(res) <1:
        return jsonify({'message': 'Usuario no existe'}), 400
    
    if passw != res[0][1]:
        return jsonify({'message': 'Password Incorrecta'}), 400
    token = generate_jwt(res[0][0])
    
    return jsonify({'token':token})


@app.route('/check',methods=['POST'])
@token_required
def check(current_user):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    resultado = verificar(file)
    for x in resultado:
        db.guardar_fotos(x['placa'],current_user)

    return jsonify(resultado), 200

@app.route('/images',methods=['get'])
@token_required
def images(current_user):
    con = db.get_connection()
    curs = con.cursor()
    curs.execute("select placa from Placa where user = %s",(current_user,))
    res = curs.fetchall()
    db.close_connection(con)

    
    return jsonify(res)






if __name__ == '__main__':
    app.run(debug=True)