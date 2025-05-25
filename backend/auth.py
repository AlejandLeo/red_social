from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from neo4j_utils import Neo4jUtils
from redis_utils import guardar_cache

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = 'clave_secreta_12345'

# Simulación simple de DB usuarios en memoria (reemplaza por Neo4j real si quieres)
usuarios = {}
neo4j_utils = Neo4jUtils()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    nombre = data.get('nombre')
    if not email or not password or not nombre:
        return jsonify({"error": "Faltan datos"}), 400
    if email in usuarios:
        return jsonify({"error": "Usuario ya existe"}), 400
    hashed = generate_password_hash(password)
    user_id = f'u_{uuid.uuid4().hex[:8]}'
    
    usuarios[email] = {"id": user_id, "nombre": nombre, "email": email, "password": hashed}
    # Aquí deberías crear usuario en Neo4j también (omito para brevedad)
    
    neo4j_utils.crear_usuario(user_id, nombre, email, hashed)
    guardar_cache(f"user:{user_id}", {"nombre": nombre, "email": email})
    
    return jsonify({"msg": "Usuario creado"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # user = usuarios.get(email)
    user = neo4j_utils.obtener_usuario_por_email(email)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({"token": token, "nombre": user['nombre'], "user_id": user['id']})