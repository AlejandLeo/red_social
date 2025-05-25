import React, { useEffect, useState } from 'react';
import api from '../api';

function Amigos() {
  const [amigos, setAmigos] = useState([]);
  const [sugerencias, setSugerencias] = useState([]);
  const [busqueda, setBusqueda] = useState('');
  const [resultadosBusqueda, setResultadosBusqueda] = useState([]);

  useEffect(() => {
    cargarAmigos();
    cargarSugerencias();
  }, []);

  const cargarAmigos = async () => {
    try {
      const res = await api.get('/amigos');
      setAmigos(res.data);
    } catch (error) {
      alert('Error al cargar amigos');
    }
  };

  const cargarSugerencias = async () => {
    try {
      const res = await api.get('/recomendar');
      setSugerencias(res.data);
    } catch (error) {
      alert('Error al cargar sugerencias');
    }
  };

  const agregarAmigo = async (amigo_id) => {
    try {
      await api.post(`/agregar_amigo/${amigo_id}`);
      cargarAmigos(); // Actualiza la lista de amigos
      cargarSugerencias(); // Actualiza sugerencias
    } catch (error) {
      alert('Error al agregar amigo');
    }
  };

  const buscarUsuarios = async () => {
  try {
    const res = await api.get(`/buscar_usuarios?query=${busqueda}`);
    setResultadosBusqueda(res.data);
  } catch (error) {
    alert('Error al buscar usuarios');
  }
  };

  return (
    <div>
      <h2>Mis amigos</h2>
      <ul>
        {amigos.map((amigo) => (
          <li key={amigo.id}>{amigo.nombre}</li>
        ))}
      </ul>

      <h2>Sugerencias de amistad</h2>
      <ul>
        {sugerencias.map((s) => (
          <li key={s.id}>
            {s.nombre}
            <button onClick={() => agregarAmigo(s.id)}>Agregar</button>
          </li>
        ))}
      </ul>
      
      <h2>Buscar usuarios</h2>
      <input
        type="text"
        placeholder="Nombre o email"
        value={busqueda}
        onChange={e => setBusqueda(e.target.value)}
      />
      <button onClick={buscarUsuarios}>Buscar</button>

      <ul>
        {resultadosBusqueda.map(u => (
          <li key={u.id}>
            {u.nombre} ({u.email})
            <button onClick={() => agregarAmigo(u.id)}>Agregar</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Amigos;
