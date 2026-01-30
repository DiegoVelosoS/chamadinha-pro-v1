// frontend/src/pages/Painel.jsx
import { useState } from 'react';
import { Users, FileText, UserPlus, CheckCircle, XCircle, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Painel() {
  const navigate = useNavigate();
  const [chamadaAtiva, setChamadaAtiva] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [loading, setLoading] = useState(false);

  // Função que envia a foto para o Python
  async function processarChamada(event) {
    const arquivo = event.target.files[0];
    if (!arquivo) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('foto', arquivo);

    try {
      // Conecta com seu Backend rodando na porta 8000
      const response = await fetch('http://127.0.0.1:8000/chamada/reconhecer', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      
      // Guarda a lista de alunos encontrados
      setResultado(data.alunos || []); 
    } catch (error) {
      alert("Erro ao conectar com servidor. O Backend está rodando?");
    } finally {
      setLoading(false);
      setChamadaAtiva(true);
    }
  }

  return (
    <div className="min-h-screen bg-app-dark text-white p-6 pb-20">
      <div className="max-w-md mx-auto space-y-8">
        
        {/* Header */}
        <div className="flex justify-between items-center pt-4">
          <div>
            <h1 className="text-xl font-bold text-gray-400">Olá, Professor</h1>
            <h2 className="text-2xl font-bold">Painel de Controle</h2>
          </div>
          <button onClick={() => navigate('/')} className="p-2 bg-app-card rounded-full text-red-400">
            <LogOut size={20} />
          </button>
        </div>

        {/* Botões de Ação */}
        <div className="space-y-4">
          
          {/* BOTÃO 1: Fazer Chamada (Com input de arquivo escondido) */}
          <label className="block w-full cursor-pointer group">
            <input 
                type="file" 
                accept="image/*" 
                capture="environment" 
                className="hidden" 
                onChange={processarChamada}
                disabled={loading}
            />
            <div className={`h-24 rounded-2xl flex items-center justify-center shadow-lg transition-all active:scale-95 border border-transparent hover:border-app-green ${loading ? 'bg-gray-800' : 'bg-app-card'}`}>
                {loading ? (
                    <div className="flex flex-col items-center animate-pulse">
                        <span className="text-app-green font-bold">PROCESSANDO IA...</span>
                    </div>
                ) : (
                    <div className="flex flex-col items-center gap-1">
                        <Users size={32} className="text-app-green" />
                        <span className="font-bold text-lg uppercase">FAZER CHAMADA</span>
                    </div>
                )}
            </div>
          </label>

          {/* Outros botões (Visuais por enquanto) */}
          <button className="w-full h-24 bg-app-card rounded-2xl flex flex-col items-center justify-center shadow-lg active:scale-95 border border-transparent hover:border-gray-600">
             <FileText size={32} className="text-blue-400 mb-1" />
             <span className="font-bold text-lg uppercase">RELATÓRIOS</span>
          </button>

          <button className="w-full h-24 bg-app-card rounded-2xl flex flex-col items-center justify-center shadow-lg active:scale-95 border border-transparent hover:border-gray-600">
             <UserPlus size={32} className="text-app-gold mb-1" />
             <span className="font-bold text-lg uppercase">NOVO ALUNO</span>
          </button>
        </div>

        {/* MODAL DE RESULTADO (Aparece após a foto) */}
        {chamadaAtiva && (
            <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-end sm:items-center justify-center z-50 p-4">
                <div className="bg-app-card w-full max-w-md rounded-2xl p-6 border border-gray-700 shadow-2xl animate-fade-in">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-white font-bold text-lg">Resultado da Chamada</h3>
                        <button onClick={() => setChamadaAtiva(false)} className="text-gray-400 hover:text-white">Fechar</button>
                    </div>
                    
                    <div className="space-y-3 max-h-[60vh] overflow-y-auto">
                        {resultado && resultado.length > 0 ? (
                            resultado.map((aluno) => (
                                <div key={aluno.id} className="flex items-center justify-between bg-black/40 p-4 rounded-xl border border-gray-800">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center font-bold text-white">
                                            {aluno.nome.charAt(0)}
                                        </div>
                                        <div>
                                            <p className="font-bold text-white">{aluno.nome}</p>
                                            <p className="text-xs text-app-green">Reconhecimento: {(aluno.confianca * 100).toFixed(0)}%</p>
                                        </div>
                                    </div>
                                    <CheckCircle className="text-app-green" size={24} />
                                </div>
                            ))
                        ) : (
                            <div className="text-center py-8 text-gray-400 flex flex-col items-center gap-3">
                                <XCircle size={48} className="text-red-500" />
                                <p>Nenhum aluno identificado nesta foto.</p>
                                <p className="text-sm">Tente melhorar a iluminação.</p>
                            </div>
                        )}
                    </div>

                    <button 
                        onClick={() => setChamadaAtiva(false)}
                        className="mt-6 w-full py-3 bg-app-green rounded-xl font-bold text-white shadow-lg"
                    >
                        OK, CONFIRMAR
                    </button>
                </div>
            </div>
        )}
      </div>
    </div>
  );
}