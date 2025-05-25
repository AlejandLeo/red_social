import React, { useEffect, useState } from 'react';
import API from '../api';

function Perfil() {
  const [perfil, setPerfil] = useState({});
  const [interes, setInteres] = useState('');
  const [skill, setSkill] = useState('');

  useEffect(() => {
    API.get('/perfil').then(res => setPerfil(res.data));
  }, []);

  const actualizarPerfil = () => {
    API.post('/perfil', { interes, skill }).then(() => {
      alert('Actualizado');
      window.location.reload();
    });
  };

  return (
    <div>
      <h2>Perfil</h2>
      <p>Nombre: {perfil.nombre}</p>
      <p>Email: {perfil.email}</p>
      <p>Intereses: {perfil.intereses?.join(', ')}</p>
      <p>Skills: {perfil.skills?.join(', ')}</p>

      <h3>Actualizar</h3>
      <input placeholder="Nuevo Interés" value={interes} onChange={e => setInteres(e.target.value)} />
      <input placeholder="Nuevo Skill" value={skill} onChange={e => setSkill(e.target.value)} />
      <button onClick={actualizarPerfil}>Guardar</button>
    </div>
  );
}

export default Perfil;
