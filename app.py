from flask import Flask, jsonify
from db import Database 

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