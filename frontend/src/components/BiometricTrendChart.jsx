import React from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, ReferenceArea
} from 'recharts';

const BiometricTrendChart = ({ data }) => {
  // 날짜 형식 변환 (MM/DD)
  const formattedData = data.map(item => ({
    ...item,
    displayDate: new Date(item.test_date).toLocaleDateString('ko-KR', { month: '2-digit', day: '2-digit' })
  }));

    <div className="space-y-6">
      <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-md">
        <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
          <span className="p-2 bg-blue-500/20 rounded-lg text-blue-400">📈</span>
          체형 변화 추이 (Body Metrics)
        </h3>
        
        <div style={{ height: '300px', width: '100%', minHeight: '300px', position: 'relative' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={formattedData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
              <XAxis 
                dataKey="displayDate" 
                stroke="#94a3b8" 
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <YAxis 
                stroke="#94a3b8" 
                fontSize={12}
                tickLine={false}
                axisLine={false}
                domain={['auto', 'auto']}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #ffffff20',
                  borderRadius: '12px',
                  color: '#f8fafc'
                }}
                itemStyle={{ color: '#f8fafc' }}
              />
              <Legend verticalAlign="top" height={36}/>
              
              {/* 정상 범위 표시 (예: 체지방률 15-25%) */}
              <ReferenceArea y1={15} y2={25} fill="#10b981" fillOpacity={0.1} />

              {/* 체중 (Weight) - 메인 라인 */}
              <Line 
                name="체중 (kg)"
                type="monotone" 
                dataKey="weight" 
                stroke="#3b82f6" 
                strokeWidth={3}
                dot={{ r: 4, fill: '#3b82f6' }}
                activeDot={{ r: 6 }}
                animationDuration={1500}
              />
              
              {/* 골격근량 (Muscle) */}
              <Line 
                name="골격근량 (kg)"
                type="monotone" 
                dataKey="muscle" 
                stroke="#10b981" 
                strokeWidth={2}
                dasharray="5 5"
                dot={{ r: 3, fill: '#10b981' }}
                animationDuration={1500}
              />

              {/* 체지방률 (Fat %) */}
              <Line 
                name="체지방률 (%)"
                type="monotone" 
                dataKey="fat_pct" 
                stroke="#f43f5e" 
                strokeWidth={2}
                dot={{ r: 3, fill: '#f43f5e' }}
                animationDuration={1500}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        
        <div className="mt-4 flex gap-4 text-xs text-slate-400 justify-center">
          <p className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-blue-500"></span> 체중 감소
          </p>
          <p className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-green-500"></span> 근육 증가
          </p>
          <p className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-rose-500"></span> 체지방 감소
          </p>
          <p className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500/20 border border-emerald-500"></span> 체지방 정상범위 (15-25%)
          </p>
        </div>
      </div>

      {/* 혈액 지표 차트 */}
      <div className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-md mt-6">
        <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
          <span className="p-2 bg-rose-500/20 rounded-lg text-rose-400">🩸</span>
          혈액 지표 추이 (Blood Metrics)
        </h3>
        
        <div style={{ height: '300px', width: '100%', minHeight: '300px', position: 'relative' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={formattedData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
              <XAxis 
                dataKey="displayDate" 
                stroke="#94a3b8" 
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <YAxis 
                stroke="#94a3b8" 
                fontSize={12}
                tickLine={false}
                axisLine={false}
                domain={['auto', 'auto']}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1e293b', 
                  border: '1px solid #ffffff20',
                  borderRadius: '12px',
                  color: '#f8fafc'
                }}
                itemStyle={{ color: '#f8fafc' }}
              />
              <Legend verticalAlign="top" height={36}/>
              
              {/* 정상 범위 표시 */}
              <ReferenceArea y1={70} y2={100} fill="#3b82f6" fillOpacity={0.1} />
              <ReferenceArea y1={0} y2={130} fill="#f59e0b" fillOpacity={0.1} />

              {/* 공복혈당 (Glucose) */}
              <Line 
                name="공복혈당 (mg/dL)"
                type="monotone" 
                dataKey="glucose" 
                stroke="#3b82f6" 
                strokeWidth={3}
                dot={{ r: 4, fill: '#3b82f6' }}
                activeDot={{ r: 6 }}
                animationDuration={1500}
              />
              
              {/* LDL 콜레스테롤 (LDL) */}
              <Line 
                name="LDL 콜레스테롤 (mg/dL)"
                type="monotone" 
                dataKey="ldl" 
                stroke="#f59e0b" 
                strokeWidth={2}
                dasharray="5 5"
                dot={{ r: 3, fill: '#f59e0b' }}
                animationDuration={1500}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        
        <div className="mt-4 flex gap-4 text-xs text-slate-400 justify-center">
          <p className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-blue-500/20 border border-blue-500"></span> 혈당 정상 (70-100)
          </p>
          <p className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-amber-500/20 border border-amber-500"></span> LDL 정상 (0-130)
          </p>
        </div>
      </div>
    </div>
  );
};

export default BiometricTrendChart;
