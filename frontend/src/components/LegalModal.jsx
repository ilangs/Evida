import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

const LegalModal = ({ isOpen, onClose, title, content }) => {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="bg-[#1e293b] border border-white/10 rounded-3xl w-full max-w-2xl max-h-[80vh] flex flex-col shadow-2xl relative overflow-hidden"
        >
          {/* Header */}
          <div className="p-6 border-b border-white/5 flex items-center justify-between bg-white/5">
            <h2 className="text-xl font-bold gradient-text">{title}</h2>
            <button 
              onClick={onClose}
              className="p-2 hover:bg-white/10 rounded-full transition-colors text-slate-400"
            >
              <X size={24} />
            </button>
          </div>

          {/* Content Area */}
          <div className="p-8 overflow-y-auto scrollbar-hide">
            <div className="text-slate-300 whitespace-pre-wrap leading-relaxed font-light text-sm space-y-4">
              {content}
            </div>
            
            <div className="mt-12 p-6 bg-indigo-500/5 rounded-2xl border border-indigo-500/10">
              <p className="text-xs text-indigo-400 font-bold mb-2">💡 중요 안내</p>
              <p className="text-xs text-slate-500 italic">본 문서는 'Vital Intelligence' 대시보드 프로젝트의 법적 리스크 방지를 위해 가이드라인에 따라 작성되었습니다. 실제 서비스 배포 시 전문 법조인의 검수가 필요합니다.</p>
            </div>
          </div>

          {/* Footer */}
          <div className="p-6 border-t border-white/5 text-right bg-white/5">
            <button 
              onClick={onClose}
              className="px-6 py-2 bg-white/10 hover:bg-white/20 rounded-xl font-bold transition-all text-sm"
            >
              닫기 (Close)
            </button>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default LegalModal;
