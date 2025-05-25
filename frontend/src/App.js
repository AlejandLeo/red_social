import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';

import Login from './pages/Login';
import Register from './pages/Register';
import Perfil from './pages/Perfil';
import Amigos from './pages/Amigos';
import Publicaciones from './pages/Publicaciones';
import Navbar from './components/Navbar';
// import './styles.css';

function PrivateRoute({ children }) {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" />;
}


function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route path="/perfil" element={
          <PrivateRoute><Perfil /></PrivateRoute>
        } />
        <Route path="/amigos" element={
          <PrivateRoute><Amigos /></PrivateRoute>
        } />
        <Route path="/publicaciones" element={
          <PrivateRoute><Publicaciones /></PrivateRoute>
        } />

        {/* Ruta raíz: si está logueado va al perfil, si no al login */}
        <Route path="/" element={
          localStorage.getItem('token') ? <Navigate to="/perfil" /> : <Navigate to="/login" />
        } />
        
        {/* Ruta para 404 */}
        <Route path="*" element={<h2>Página no encontrada</h2>} />
      </Routes>
    </Router>
  );
}

export default App;