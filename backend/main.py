from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import jwt
from neo4j_utils import Neo4jUtils
from redis_utils import guardar_cache, obtener_cache
from auth import auth_bp, SECRET_KEY

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')
CORS(app, supports_credentials=True)
neo4j_utils = Neo4jUtils()

def token_requerido(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            bearer = request.headers.get('Authorization')  # Bearer eyJ...
            token = bearer.split()[1] if len(bearer.split()) > 1 else None
        if not token:
            return jsonify({"error": "Token faltante"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = data['user_id']
        except Exception:
            return jsonify({"error": "Token inválido"}), 401
        return f(user_id, *args, **kwargs)
    return decorator

def sugerencias_por_interes_skill_cache(user_id, ttl=300):
    cache_key = f"sugerencias:{user_id}"
    cached = obtener_cache(cache_key)
    if cached is not None:
        return cached
    sugerencias = neo4j_utils.sugerencias_por_interes_skill(user_id)
    guardar_cache(cache_key, sugerencias, ttl)
    return sugerencias

@app.route('/perfil', methods=['GET', 'POST'])
@token_requerido
def perfil(user_id):
    if request.method == 'POST':
        data = request.json
        interes = data.get('interes')
        skill = data.get('skill')
        if interes:
            neo4j_utils.actualizar_interes(user_id, interes)
        if skill:
            neo4j_utils.actualizar_skill(user_id, skill)
        return jsonify({"msg": "Perfil actualizado"})
    perfil = neo4j_utils.obtener_perfil(user_id)
    return jsonify(perfil)

@app.route('/recomendar', methods=['GET'])
@token_requerido
def recomendar(user_id):
    sugerencias = sugerencias_por_interes_skill_cache(user_id)
    return jsonify(sugerencias)

@app.route('/agregar_amigo/<amigo_id>', methods=['POST'])
@token_requerido
def agregar_amigo(user_id, amigo_id):
    neo4j_utils.agregar_amigo(user_id, amigo_id)
    return jsonify({"msg": "Amigo agregado"})

@app.route('/amigos', methods=['GET'])
@token_requerido
def amigos(user_id):
    amigos = neo4j_utils.obtener_amigos(user_id)
    return jsonify(amigos)

@app.route('/publicaciones', methods=['GET', 'POST'])
@token_requerido
def publicaciones(user_id):
    if request.method == 'POST':
        data = request.json
        texto = data.get('texto')
        imagen_url = data.get('imagen_url')
        neo4j_utils.crear_publicacion(user_id, texto, imagen_url)
        return jsonify({"msg": "Publicación creada"})
    publicaciones = neo4j_utils.obtener_publicaciones_amigos(user_id)
    return jsonify(publicaciones)

@app.route('/buscar_usuarios')
@token_requerido
def buscar_usuarios(user_id):
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    with neo4j_utils.driver.session() as session:
        result = session.run("""
            MATCH (u:Usuario)
            WHERE toLower(u.nombre) CONTAINS toLower($query) OR toLower(u.email) CONTAINS toLower($query)
            RETURN u.id AS id, u.nombre AS nombre, u.email AS email
            LIMIT 10
        """, query=query)
        usuarios = [{"id": r["id"], "nombre": r["nombre"], "email": r["email"]} for r in result]

    # Opcional: excluir al usuario actual de resultados
    usuarios = [u for u in usuarios if u['id'] != user_id]

    return jsonify(usuarios)

@app.route('/mis-publicaciones', methods=['GET'])
@token_requerido
def publicaciones_personales(user_id):
    publicaciones = neo4j_utils.obtener_publicaciones_usuario(user_id)
    return jsonify([dict(p) for p in publicaciones]), 200
    
if __name__ == '__main__':
    app.run(debug=True, port=8800) # cambiar port por algun puerto que no se este usando