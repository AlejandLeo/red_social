import React, { useEffect, useState } from 'react';
import api from '../api';

function Publicaciones() {
  const [publicaciones, setPublicaciones] = useState([]);
  const [texto, setTexto] = useState('');
  const [imagen_url, setImagenUrl] = useState('');
  const [mias, setMias] = useState([]);

  useEffect(() => {
  api.get('/publicaciones').then(res => setPublicaciones(res.data));
  api.get('/mis-publicaciones').then(res => setMias(res.data));
}, []);

  const crearPublicacion = () => {
    api.post('/publicaciones', { texto }).then(() => {
      alert('Publicación creada');
      window.location.reload();
    });
  };

  return (
    <div>
      <h2>Mis Publicaciones</h2>
      <ul>
        {mias.map((p) => (
          <li key={p.id}>
            <strong>{p.autor}:</strong> {p.texto}
            {p.imagen_url && <img src={p.imagen_url} alt="" width="100" />}
          </li>
        ))}
      </ul>

      <h2>Publicaciones de tus amigos</h2>
      <ul>
        {publicaciones.map((p) => (
          <li key={p.id}>
            <strong>{p.autor}:</strong> {p.texto}
            {p.imagen_url && <img src={p.imagen_url} alt="" width="100" />}
          </li>
        ))}
      </ul>

      <h3>Crear Publicación</h3>
      <input placeholder="Texto" value={texto} onChange={e => setTexto(e.target.value)} />
      <input placeholder="URL de imagen" value={imagen_url} onChange={e => setImagenUrl(e.target.value)} />
      <button onClick={crearPublicacion}>Publicar</button>
    </div>
  );
}

export default Publicaciones;
