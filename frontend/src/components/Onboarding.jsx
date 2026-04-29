import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShieldCheck, UserCircle, Target, ChevronRight, 
  ChevronLeft, CheckCircle2, Info, Moon, Sun, Scale
} from 'lucide-react';

const API_BASE = "http://localhost:8000/v1";

const Onboarding = ({ onComplete, openLegal }) => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    name: '',
    age: 25,
    gender: 'male',
    mbti: 'INTJ',
    goal_type: 'weight_loss',
    goal_description: '',
    start_weight: 70,
    target_weight: 65,
    wake_time: '07:00',
    sleep_time: '23:00',
    is_consented: false
  });

  const nextStep = () => setStep(s => s + 1);
  const prevStep = () => setStep(s => s - 1);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const resp = await axios.post(`${API_BASE}/users/register`, form);
      if (resp.data.status === 'success') {
        onComplete(resp.data.user_id);
      }
    } catch (err) {
      console.error(err);
      alert("Registration failed. Please check the inputs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[200] bg-[#0f172a] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_-20%,#312e81,transparent)] opacity-40" />
      
      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-xl glass-card p-10 relative overflow-hidden"
      >
        {/* Progress Bar */}
        <div className="flex gap-2 mb-10">
          {[1,2,3].map(s => (
            <div key={s} className={`h-1.5 flex-grow rounded-full transition-all duration-500 ${step >= s ? 'bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.5)]' : 'bg-white/5'}`} />
          ))}
        </div>

        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.div 
              key="step1"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div className="space-y-2">
                <h2 className="text-3xl font-black gradient-text">Safety First.</h2>
                <p className="text-slate-400 text-sm">서비스 이용을 위해 법적 약관 및 면책 사항 동의가 필요합니다.</p>
              </div>

              <div className="space-y-3">
                {['PRIVACY', 'TERMS', 'DISCLAIMER'].map(type => (
                  <div key={type} className="flex items-center justify-between p-4 bg-white/5 border border-white/10 rounded-2xl">
                    <span className="text-sm font-bold text-slate-300">
                      {type === 'PRIVACY' ? '개인정보 처리방침 (필수)' : type === 'TERMS' ? '서비스 이용약관 (필수)' : '의료 법적 고지 (필수)'}
                    </span>
                    <button 
                      onClick={() => openLegal(type)}
                      className="text-[10px] uppercase font-black text-indigo-400 hover:text-indigo-300 bg-indigo-500/10 px-3 py-1 rounded-lg"
                    >
                      View View
                    </button>
                  </div>
                ))}
              </div>

              <label className="flex items-center gap-3 p-6 bg-indigo-500/5 rounded-3xl border border-indigo-500/20 group cursor-pointer">
                <input 
                  type="checkbox" 
                  checked={form.is_consented}
                  onChange={(e) => setForm({...form, is_consented: e.target.checked})}
                  className="w-5 h-5 rounded-md accent-indigo-500"
                />
                <span className="text-sm font-bold text-slate-200 group-hover:text-indigo-400 transition-colors">
                  모든 법적 고지 및 데이터 수집에 동의합니다.
                </span>
              </label>

              <button 
                disabled={!form.is_consented}
                onClick={nextStep}
                className={`w-full py-4 rounded-2xl font-black text-sm flex items-center justify-center gap-2 transition-all ${form.is_consented ? 'bg-indigo-600 hover:bg-indigo-500 shadow-xl' : 'bg-slate-800'}`}
              >
                Next Step <ChevronRight size={18} />
              </button>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div 
              key="step2"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div className="space-y-2">
                <h2 className="text-3xl font-black gradient-text">Tell us who you are.</h2>
                <p className="text-slate-400 text-sm">초개인화 가이드를 위해 당신의 페르소나를 입력해 주세요.</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2 text-glow">Full Name</label>
                  <input 
                    type="text"
                    value={form.name}
                    onChange={(e) => setForm({...form, name: e.target.value})}
                    placeholder="홍길동"
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2">Age</label>
                  <input 
                    type="number"
                    value={form.age}
                    onChange={(e) => setForm({...form, age: parseInt(e.target.value)})}
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2 text-glow">MBTI</label>
                  <input 
                    type="text"
                    value={form.mbti}
                    onChange={(e) => setForm({...form, mbti: e.target.value.toUpperCase()})}
                    maxLength={4}
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2">Gender</label>
                  <select 
                    value={form.gender}
                    onChange={(e) => setForm({...form, gender: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500"
                  >
                    <option value="male" className="bg-[#1e293b]">남성 (Male)</option>
                    <option value="female" className="bg-[#1e293b]">여성 (Female)</option>
                  </select>
                </div>
              </div>

              <div className="flex gap-3">
                <button onClick={prevStep} className="flex-grow py-4 rounded-2xl font-black text-sm bg-white/5 border border-white/10 flex items-center justify-center gap-2">
                  <ChevronLeft size={18} /> Back
                </button>
                <button 
                  disabled={!form.name || !form.mbti}
                  onClick={nextStep}
                  className="flex-[2] py-4 rounded-2xl font-black text-sm bg-indigo-600 hover:bg-indigo-500 flex items-center justify-center gap-2"
                >
                  Continuue <ChevronRight size={18} />
                </button>
              </div>
            </motion.div>
          )}

          {step === 3 && (
            <motion.div 
              key="step3"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
              <div className="space-y-2">
                <h2 className="text-3xl font-black gradient-text">Mission Setup.</h2>
                <p className="text-slate-400 text-sm">마지막 단계입니다. 달성하고 싶은 목표와 생활 패턴을 적어주세요.</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5 flex flex-col">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2">MISSION TYPE</label>
                  <select 
                    value={form.goal_type}
                    onChange={(e) => setForm({...form, goal_type: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500 appearance-none text-sm font-bold"
                  >
                    <option value="weight_loss" className="bg-[#1e293b]">체중 감량 (Weight Loss)</option>
                    <option value="weight_gain" className="bg-[#1e293b]">건강한 증량 (Weight Gain)</option>
                  </select>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2">A Health Goal Description</label>
                  <input 
                    type="text"
                    value={form.goal_description}
                    onChange={(e) => setForm({...form, goal_description: e.target.value})}
                    placeholder={form.goal_type === 'weight_loss' ? "예: 6개월간 지방 5kg 감량" : "예: 6개월간 근육 3kg 증가/증량"}
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2 flex items-center gap-1">
                    <Scale size={10} /> CURRENT WEIGHT
                  </label>
                  <input 
                    type="number"
                    value={form.start_weight}
                    onChange={(e) => setForm({...form, start_weight: parseFloat(e.target.value)})}
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2 flex items-center gap-1">
                    <Target size={10} /> TARGET WEIGHT
                  </label>
                  <input 
                    type="number"
                    value={form.target_weight}
                    onChange={(e) => setForm({...form, target_weight: parseFloat(e.target.value)})}
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2 flex items-center gap-1">
                    <Sun size={10} /> Wake-up TIME
                  </label>
                  <input 
                    type="time"
                    value={form.wake_time}
                    onChange={(e) => setForm({...form, wake_time: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[10px] uppercase font-black text-slate-500 ml-2 flex items-center gap-1">
                    <Moon size={10} /> SLEEP TIME
                  </label>
                  <input 
                    type="time"
                    value={form.sleep_time}
                    onChange={(e) => setForm({...form, sleep_time: e.target.value})}
                    className="w-full bg-white/5 border border-white/10 p-3 rounded-xl focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div className="flex gap-3">
                <button onClick={prevStep} className="flex-grow py-4 rounded-2xl font-black text-sm bg-white/5 border border-white/10 flex items-center justify-center gap-2">
                  <ChevronLeft size={18} /> Back
                </button>
                <button 
                  disabled={loading || !form.goal_description}
                  onClick={handleSubmit}
                  className="flex-[2] py-4 rounded-2xl font-black text-sm bg-emerald-600 hover:bg-emerald-500 shadow-xl shadow-emerald-900/40 flex items-center justify-center gap-2"
                >
                  {loading ? "..." : <>Start My Journey <CheckCircle2 size={18} /></>}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer info */}
        <div className="mt-8 flex items-center justify-center gap-2 text-slate-600">
          <Info size={12} />
          <span className="text-[9px] font-bold uppercase tracking-widest">Medical Intelligence Compliance Pack v1.0</span>
        </div>
      </motion.div>
    </div>
  );
};

export default Onboarding;
