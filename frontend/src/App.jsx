// frontend/src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Painel from './pages/Painel';
import './App.css'; // Mantenha se quiser, ou pode limpar

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rota inicial: Login */}
        <Route path="/" element={<Login />} />
        
        {/* Rota do Painel */}
        <Route path="/painel" element={<Painel />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;