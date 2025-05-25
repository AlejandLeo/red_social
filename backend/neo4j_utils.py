from neo4j import GraphDatabase

class Neo4jUtils:
    def __init__(self):
        uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))

    def crear_usuario(self, user_id, nombre, email, password):
        with self.driver.session() as session:
            session.run("MERGE (u:Usuario {id: $id, nombre: $nombre, email: $email, password: $password})",
                        id=user_id, nombre=nombre, email=email, password=password)

    def obtener_usuario_por_email(self, email):
        with self.driver.session() as session:
            result = session.run("""
            MATCH (u:Usuario {email: $email})
            RETURN u.id AS id, u.nombre AS nombre, u.email AS email, u.password AS password
            """, email=email).data()
        return result[0] if result else None

    def actualizar_interes(self, user_id, interes):
        with self.driver.session() as session:
            session.run("MERGE (i:Interes {nombre: $interes})", interes=interes)
            session.run("""
                MATCH (u:Usuario {id: $user_id}), (i:Interes {nombre: $interes})
                MERGE (u)-[:TIENE_INTERES]->(i)
            """, user_id=user_id, interes=interes)

    def actualizar_skill(self, user_id, skill):
        with self.driver.session() as session:
            session.run("MERGE (s:Skill {nombre: $skill})", skill=skill)
            session.run("""
                MATCH (u:Usuario {id: $user_id}), (s:Skill {nombre: $skill})
                MERGE (u)-[:TIENE_SKILL]->(s)
            """, user_id=user_id, skill=skill)

    def obtener_perfil(self, user_id):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:Usuario {id: $user_id})
                OPTIONAL MATCH (u)-[:TIENE_INTERES]->(i:Interes)
                OPTIONAL MATCH (u)-[:TIENE_SKILL]->(s:Skill)
                RETURN u.nombre AS nombre, u.email AS email,
                collect(DISTINCT i.nombre) AS intereses,
                collect(DISTINCT s.nombre) AS skills
            """, user_id=user_id)
            record = result.single()
            if record:
                return {
                    "nombre": record["nombre"],
                    "email": record["email"],
                    "intereses": record["intereses"],
                    "skills": record["skills"]
                }
            return {}

    def sugerencias_por_interes_skill(self, user_id):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u1:Usuario {id: $user_id})-[:TIENE_INTERES|TIENE_SKILL]->(x)<-[:TIENE_INTERES|TIENE_SKILL]-(u2:Usuario)
                WHERE u1 <> u2 AND NOT (u1)-[:CONOCE]->(u2)
                RETURN DISTINCT u2.nombre AS nombre, u2.id AS id
                LIMIT 10
            """, user_id=user_id)
            return [{"id": record["id"], "nombre": record["nombre"]} for record in result]

    def agregar_amigo(self, user_id, amigo_id):
        with self.driver.session() as session:
            session.run("""
                MATCH (u1:Usuario {id: $user_id}), (u2:Usuario {id: $amigo_id})
                MERGE (u1)-[:CONOCE]->(u2)
            """, user_id=user_id, amigo_id=amigo_id)

    def obtener_amigos(self, user_id):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:Usuario {id: $user_id})-[:CONOCE]->(a:Usuario)
                RETURN a.id AS id, a.nombre AS nombre
            """, user_id=user_id)
            return [{"id": record["id"], "nombre": record["nombre"]} for record in result]

    def crear_publicacion(self, user_id, texto, imagen_url):
        fecha = datetime.datetime.utcnow().isoformat()
        with self.driver.session() as session:
            session.run("""
                            MATCH (u:Usuario {id: $user_id})
            CREATE (p:Publicacion {id: randomUUID(), texto: $texto, imagen_url: $imagen_url, fecha: $fecha})
            CREATE (u)-[:HIZO_PUBLICACION]->(p)
            """, user_id=user_id, texto=texto or "", imagen_url=imagen_url or "")

    def obtener_publicaciones_amigos(self, user_id):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:Usuario {id: $user_id})-[:CONOCE]->(a:Usuario)-[:HIZO_PUBLICACION]->(p:Publicacion)
                RETURN a.nombre AS autor, p.texto AS texto, p.imagen_url AS imagen_url, p.id AS id
                ORDER BY p.id DESC
            """, user_id=user_id)
            return [{
                "id": record["id"],
                "autor": record["autor"],
                "texto": record["texto"],
                "imagen_url": record["imagen_url"]
            } for record in result]

    def obtener_publicaciones_usuario(self,usuario_id):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:Usuario {id: $usuario_id})-[:HIZO_PUBLICACION]->(p:Publicacion)
                RETURN p ORDER BY p.fecha DESC
                """,usuario_id=usuario_id)
        return [record["p"] for record in result]
