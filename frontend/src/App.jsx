import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, Target, Sun, Brain, Droplet, Scale, Dna, 
  TrendingUp, FileText, Zap, ChevronRight, BarChart2
} from 'lucide-react';
import BiometricTrendChart from './components/BiometricTrendChart';
import LegalModal from './components/LegalModal';
import Onboarding from './components/Onboarding';
import { LEGAL_TEXTS } from './constants/LegalTexts';

const API_BASE = "http://localhost:8000/v1";

const StatCard = ({ label, value, unit, diff, trend, icon }) => (
  <div className="glass-card p-6 flex items-center gap-4 transition-all duration-300">
    <div className="p-3 bg-white/5 rounded-2xl text-slate-400 group-hover:text-indigo-400 transition-colors">
      {icon}
    </div>
    <div>
      <div className="text-slate-400 text-xs uppercase tracking-wider font-bold mb-1">{label}</div>
      <div className="text-2xl font-black flex items-baseline gap-1">
        {value} <span className="text-sm font-normal text-slate-500">{unit}</span>
        {diff && (
          <span className={`ml-2 text-xs px-2 py-0.5 rounded-full ${trend === 'up' ? 'bg-red-500/10 text-red-400' : 'bg-green-500/10 text-green-400'}`}>
            {trend === 'up' ? '▲' : '▼'} {diff}
          </span>
        )}
      </div>
    </div>
  </div>
);

function App() {
  const [userId, setUserId] = useState('a44f1533-0d51-491e-ae0a-856b8ae3efaa');
  const [userStatus, setUserStatus] = useState({ is_registered: false, is_consented: false });
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // Legal Modal States
  const [isLegalOpen, setIsLegalOpen] = useState(false);
  const [selectedLegal, setSelectedLegal] = useState({ title: "", content: "" });

  const checkStatus = async (id) => {
    try {
      const resp = await axios.get(`${API_BASE}/users/${id}/status`);
      setUserStatus(resp.data);
      if (resp.data.is_registered && resp.data.is_consented) {
        fetchData(id);
      }
    } catch (err) {
      console.error("Status check failed", err);
    }
  };

  const fetchData = async (id = userId) => {
    if (!id) return;
    setLoading(true);
    try {
      const resp = await axios.get(`${API_BASE}/coach/ai-feedback?user_id=${id}`);
      setData(resp.data);
      
      const histResp = await axios.get(`${API_BASE}/users/${id}/biometric-history`);
      setHistory(histResp.data);
    } catch (err) {
      console.error("Fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  const openLegal = (type) => {
    setSelectedLegal({
      title: LEGAL_TEXTS[type].TITLE,
      content: LEGAL_TEXTS[type].CONTENT
    });
    setIsLegalOpen(true);
  };

  const handleOnboardingComplete = (newId) => {
    setUserId(newId);
    checkStatus(newId);
  };

  useEffect(() => {
    if (userId) checkStatus(userId);
  }, []);

  const showDashboard = userStatus.is_registered && userStatus.is_consented;

  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Onboarding Layer */}
      <AnimatePresence>
        {!showDashboard && (
          <Onboarding 
            onComplete={handleOnboardingComplete} 
            openLegal={openLegal}
          />
        )}
      </AnimatePresence>

      {/* Header Section */}
      <header className="max-w-7xl mx-auto mb-10 flex flex-col md:flex-row md:items-center justify-between gap-8">
        <div>
          <h1 className="text-4xl font-extrabold gradient-text tracking-tight mb-2">Vital Intelligence</h1>
          <p className="text-slate-400 font-medium font-bold">WELCOME BACK, <span className="text-indigo-400">{userStatus.name || "GUEST"}</span></p>
        </div>
        
        <div className="flex gap-3 p-3 glass-card rounded-2xl">
          <input 
            type="text" 
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="bg-transparent px-4 py-2 focus:outline-none w-64 text-sm font-mono text-indigo-300"
            placeholder="User ID 입력..."
          />
          <button 
            onClick={() => checkStatus(userId)}
            disabled={loading}
            className="primary-button flex items-center gap-2 group"
          >
            {loading ? (
              <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1 }}>
                <Activity size={18} />
              </motion.div>
            ) : (
              <>Switch Account <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" /></>
            )}
          </button>
        </div>
      </header>

      {showDashboard && (
        <AnimatePresence>
          {data && (
            <motion.main 
              initial={{ opacity: 0, scale: 0.98 }} 
              animate={{ opacity: 1, scale: 1 }}
              className="max-w-7xl mx-auto space-y-8"
            >
              {/* Row 1: Key Goals & AI Feedback */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Progress Panel */}
                <div className="glass-card p-8 flex flex-col justify-center">
                  <div className="flex items-center gap-3 mb-10">
                    <div className="p-3 bg-violet-500/20 rounded-2xl text-violet-400">
                      <Target size={24} />
                    </div>
                    <h2 className="text-xl font-bold">목표 달성 현황</h2>
                  </div>
                  
                  <div className="text-center relative">
                    <div className="text-7xl font-black text-white glow-text">
                      {data.goal_status.progress_pct}%
                    </div>
                    <p className="text-slate-400 font-bold tracking-widest uppercase text-xs mt-3">
                      {data.goal_status.goal_type === 'weight_loss' ? '6개월 감량 목표 달성률' : '6개월 증량 목표 달성률'}
                    </p>
                    
                    <div className="mt-8 w-full bg-white/5 h-3 rounded-full overflow-hidden border border-white/5">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${data.goal_status.progress_pct}%` }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        className={`h-full bg-gradient-to-r ${data.goal_status.goal_type === 'weight_loss' ? 'from-violet-500 to-indigo-500' : 'from-emerald-500 to-teal-500'}`}
                      />
                    </div>
                    <p className={`mt-4 text-sm font-bold py-2 rounded-xl inline-block px-4 ${data.goal_status.goal_type === 'weight_loss' ? 'text-violet-400/80 bg-violet-500/5' : 'text-emerald-400/80 bg-emerald-500/5'}`}>
                      {data.goal_status.goal_type === 'weight_loss' ? '남은 감량치: ' : '추가 증량 목표: '} {data.goal_status.remaining_weight}kg
                    </p>
                  </div>
                </div>

                {/* AI Coaching Panel */}
                <div className="lg:col-span-2 glass-card p-8 flex flex-col relative overflow-hidden">
                  <div className="absolute top-0 right-0 bg-amber-500/10 px-4 py-1 rounded-bl-xl text-[10px] font-black text-amber-500 border-l border-b border-amber-500/20 uppercase tracking-tighter">
                    Non-Medical Guidance
                  </div>

                  <div className="flex items-center gap-3 mb-6">
                    <div className="p-3 bg-blue-500/20 rounded-2xl text-blue-400">
                      <Brain size={24} />
                    </div>
                    <h2 className="text-xl font-bold">AI 성격 맞춤형 실시간 가이드</h2>
                  </div>
                  
                  <div className="flex-grow bg-black/20 p-6 rounded-3xl border border-white/5 relative mb-6">
                    <p className="text-lg leading-relaxed text-slate-300 whitespace-pre-wrap font-medium lg:pr-12">
                      "{data.ai_feedback}"
                    </p>
                    <Zap size={48} className="absolute bottom-4 right-4 text-blue-500/10" />
                  </div>
                  
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mt-auto">
                    <div className="flex items-center gap-3 text-sm text-slate-500">
                      <div className="p-2 bg-emerald-500/10 rounded-lg text-emerald-400">
                        <FileText size={16} />
                      </div>
                      <span>
                        의학 데이터 근거: 
                        <a 
                          href={data.medical_evidence.source} 
                          target="_blank" 
                          rel="noreferrer"
                          className="ml-2 text-indigo-400 hover:text-indigo-300 underline font-bold"
                        >
                          {data.medical_evidence.title || "가이드라인 원문보기"}
                        </a>
                      </span>
                    </div>
                    
                    <div className="text-[10px] text-slate-600 font-medium bg-white/5 px-3 py-1 rounded-full italic">
                      {data.disclaimer}
                    </div>
                  </div>
                </div>
              </div>

              {/* Row 2: Trend Chart & Lifestyle Plan */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-8">
                  <BiometricTrendChart data={history} />
                  
                  <div className="glass-card p-8">
                    <div className="flex items-center gap-3 mb-8">
                      <div className="p-3 bg-orange-500/20 rounded-2xl text-orange-400">
                        <Sun size={24} />
                      </div>
                      <h2 className="text-xl font-bold">Dynamic Lifestyle Plan (T-Zero 기준)</h2>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      {data.daily_lifestyle_plan.map((item, idx) => (
                        <motion.div 
                          key={idx}
                          whileHover={{ y: -5, backgroundColor: 'rgba(255,255,255,0.08)' }}
                          className="p-5 bg-white/5 border border-white/10 rounded-2xl transition-all border-l-4 border-l-orange-500"
                        >
                          <div className="text-orange-400 font-extrabold text-lg mb-2">{item.time}</div>
                          <div className="font-bold text-sm mb-1">{item.activity}</div>
                          <div className="text-[10px] text-slate-500 font-black uppercase tracking-widest">{item.category}</div>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="space-y-6">
                  <StatCard label="LDL Cholesterol" value={data.goal_status.current_ldl} unit="mg/dL" trend={data.goal_status.current_ldl > 130 ? "up" : "down"} icon={<Droplet />} />
                  <StatCard label="Body Fat %" value={data.goal_status.current_fat} unit="%" trend="down" icon={<Dna />} />
                  <StatCard label="Weight" value={data.goal_status.current_weight} unit="kg" trend="down" icon={<Scale />} />
                  
                  <div className="bg-gradient-to-br from-indigo-500/20 to-transparent p-8 rounded-3xl border border-indigo-500/20 flex flex-col items-center text-center">
                    <TrendingUp className="text-indigo-400 mb-4" size={32} />
                    <h4 className="font-bold mb-2">분석 완료</h4>
                    <p className="text-sm text-slate-400 leading-relaxed">최근 6개월간 체중이 꾸준히 하향 곡선을 그리고 있습니다. 근육량 유지가 핵심입니다.</p>
                  </div>

                  <button 
                    onClick={async () => {
                      if(window.confirm("모든 데이터를 영구 삭제하시겠습니까?")) {
                        try {
                          await axios.delete(`${API_BASE}/user/${userId}`);
                          alert("성공적으로 모든 데이터가 삭제되었습니다.");
                          window.location.reload();
                        } catch(e) { alert("삭제 실패"); }
                      }
                    }}
                    className="w-full py-4 text-xs font-bold text-slate-600 hover:text-red-400 transition-colors border border-dashed border-slate-800 rounded-2xl"
                  >
                    데이터 삭제 요청 (Forget My Data)
                  </button>
                </div>
              </div>
            </motion.main>
          )}
        </AnimatePresence>
      )}

      <footer className="max-w-7xl mx-auto mt-20 pb-10 text-center space-y-4">
        <div className="flex justify-center gap-6 text-[10px] text-slate-600 font-bold uppercase tracking-widest cursor-pointer">
          <span onClick={() => openLegal('PRIVACY')} className="hover:text-slate-400">Privacy Policy</span>
          <span onClick={() => openLegal('TERMS')} className="hover:text-slate-400">Terms of Service</span>
          <span onClick={() => openLegal('DISCLAIMER')} className="hover:text-slate-400">Medical Disclaimer</span>
        </div>
        <p className="text-slate-600 text-xs font-medium tracking-widest uppercase">© 2026 Vital Intelligence. AI Powered Healthcare.</p>
      </footer>

      <LegalModal isOpen={isLegalOpen} onClose={() => setIsLegalOpen(false)} title={selectedLegal.title} content={selectedLegal.content} />
    </div>
  );
}

export default App;
