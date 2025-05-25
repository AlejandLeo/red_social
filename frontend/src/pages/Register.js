import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';

function Register() {
  const [email, setEmail] = useState('');
  const [nombre, setNombre] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const register = async () => {
    try {
      await API.post('/auth/register', { email, password, nombre });
      alert('Registrado con éxito');
      navigate('/login');
    } catch (err){
      alert('Error al registrar');
    }
  };

  return (
    <div>
      <h2>Registro</h2>
      <input placeholder="Nombre" value={nombre} onChange={e => setNombre(e.target.value)} />
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" placeholder="Contraseña" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={register}>Registrar</button>
    </div>
  );
}

export default Register;
