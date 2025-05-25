import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def guardar_cache(clave, valor, ttl=300):
    r.set(clave, json.dumps(valor), ex=ttl)

def obtener_cache(clave):
    valor = r.get(clave)
    if valor:
        return json.loads(valor)
    return None

def eliminar_cache(clave):
    r.delete(clave)