import datetime
from functools import wraps
from flask import  request, jsonify
import jwt
import os

def generate_jwt(user_id):

    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=23)  
    }
    
    token = jwt.encode(payload, os.environ['DB_PASSWORD'], algorithm='HS256')
    return token



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Bearer' in request.headers:
            token = request.headers['Bearer']
        
        if not token:
            return jsonify({'message': 'No se encuentra el Token'}), 401

        try:
            data = jwt.decode(token, os.environ['DB_PASSWORD'], algorithms=['HS256'])
            current_user = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token ya ah vencido'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token invalido'}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated