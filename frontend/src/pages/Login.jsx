// frontend/src/pages/Login.jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera } from 'lucide-react';

export default function Login() {
  const navigate = useNavigate(); // Hook para mudar de página
  const [loading, setLoading] = useState(false);
  const [senha, setSenha] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    setLoading(true);
    // Para testes rápidos, removemos o delay artificial
    setLoading(false);
    navigate('/painel');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-app-dark p-6 text-white">
      <div className="flex flex-col items-center space-y-8 w-full max-w-sm">
        
        {/* Logo / Ícone */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold tracking-wider">CHAMADINHA</h1>
          <div className="bg-app-card p-6 rounded-full inline-block mt-4 shadow-lg border border-gray-800">
            <Camera size={48} className="text-white" />
          </div>
        </div>

        {/* Formulário */}
        <form onSubmit={handleLogin} className="w-full space-y-4">
          <input 
            type="password" 
            placeholder="Senha de Acesso" 
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            className="w-full bg-app-card border border-gray-700 rounded-lg p-4 text-white placeholder-gray-500 focus:outline-none focus:border-app-green transition-colors"
          />
          
          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-app-green hover:bg-green-600 text-white font-bold py-4 rounded-lg uppercase tracking-wide transition-all shadow-md active:scale-95"
          >
            {loading ? 'Entrando...' : 'ENTRAR'}
          </button>
        </form>

        <p className="text-gray-500 text-sm">
          Versão 2.0 Pro
        </p>
      </div>
    </div>
  );
}