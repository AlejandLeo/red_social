import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();

  const cerrarSesion = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    navigate('/login');
  };

  const autenticado = !!localStorage.getItem('token');

  return (
    <nav style={{ padding: '10px', borderBottom: '1px solid #ccc' }}>
      {autenticado ? (
        <>
          <Link to="/perfil" style={{ marginRight: '10px' }}>Perfil</Link>
          <Link to="/amigos" style={{ marginRight: '10px' }}>Amigos</Link>
          <Link to="/publicaciones" style={{ marginRight: '10px' }}>Publicaciones</Link>
          <button onClick={cerrarSesion}>Cerrar sesión</button>
        </>
      ) : (
        <>
          <Link to="/login" style={{ marginRight: '10px' }}>Login</Link>
          <Link to="/register">Registro</Link>
        </>
      )}
    </nav>
  );
}

export default Navbar;
