import React from 'react';
import { 
  VictoryChart, 
  VictoryLine, 
  VictoryAxis, 
  VictoryTooltip, 
  VictoryVoronoiContainer,
  VictoryTheme,
  VictoryClipContainer,
  VictoryArea
} from 'victory-native';
import { YStack, Text, XStack, Circle } from 'tamagui';

// 30일치 정교한 Mock Data 생성
const generateMockData = () => {
  const data = [];
  const now = new Date();
  for (let i = 0; i < 30; i++) {
    const date = new Date(now);
    date.setDate(date.getDate() - (29 - i));
    
    // 점진적 변화 시뮬레이션
    data.push({
      x: date.toLocaleDateString('ko-KR', { month: '2-digit', day: '2-digit' }),
      weight: 72 - (i * 0.15) + (Math.random() * 0.2), // 72kg -> 68kg
      muscle: 32 + (i * 0.08) + (Math.random() * 0.1), // 32kg -> 34.5kg
      fat: 24 - (i * 0.2) + (Math.random() * 0.3) // 24% -> 18%
    });
  }
  return data;
};

const mockData = generateMockData();

export const PremiumChart = () => {
  return (
    <YStack 
      width="100%" 
      backgroundColor="rgba(255,255,255,0.03)" 
      borderRadius="$6" 
      padding="$4"
      borderWidth={1}
      borderColor="rgba(255,255,255,0.05)"
    >
      <XStack justifyContent="space-between" marginBottom="$4" alignItems="center">
        <Text color="white" fontWeight="900" fontSize={18} letterSpacing={1}>BIOMETRIC TRENDS</Text>
        <XStack gap="$3">
          <LegendItem color="#3B82F6" label="Weight" />
          <LegendItem color="#10B981" label="Muscle" />
          <LegendItem color="#F43F5E" label="Fat" />
        </XStack>
      </XStack>

      <VictoryChart
        height={280}
        padding={{ top: 20, bottom: 40, left: 40, right: 20 }}
        containerComponent={
          <VictoryVoronoiContainer
            labels={({ datum }) => `${datum.x}\nWeight: ${datum.weight.toFixed(1)}kg\nMuscle: ${datum.muscle.toFixed(1)}kg`}
            labelComponent={<VictoryTooltip 
              flyoutStyle={{ fill: "#1f2937", stroke: "#374151" }}
              style={{ fill: "white", fontSize: 10 }}
            />}
          />
        }
      >
        <VictoryAxis
          tickCount={5}
          style={{
            axis: { stroke: "#374151" },
            tickLabels: { fill: "#94a3b8", fontSize: 10, padding: 5 },
            grid: { stroke: "rgba(255,255,255,0.05)", strokeDasharray: "4, 4" }
          }}
        />
        <VictoryAxis
          dependentAxis
          style={{
            axis: { stroke: "transparent" },
            tickLabels: { fill: "#94a3b8", fontSize: 10, padding: 5 },
            grid: { stroke: "rgba(255,255,255,0.05)" }
          }}
        />

        {/* Weight Line */}
        <VictoryLine
          data={mockData}
          y="weight"
          interpolation="monotoneX"
          animate={{ duration: 2000, onLoad: { duration: 1000 } }}
          style={{
            data: { stroke: "#3B82F6", strokeWidth: 3, strokeLinecap: "round" }
          }}
        />

        {/* Muscle Line */}
        <VictoryLine
          data={mockData}
          y="muscle"
          interpolation="monotoneX"
          animate={{ duration: 2000, onLoad: { duration: 1200 } }}
          style={{
            data: { stroke: "#10B981", strokeWidth: 3, strokeLinecap: "round" }
          }}
        />

        {/* Fat % Line (Gradient / Area concept) */}
        <VictoryLine
          data={mockData}
          y="fat"
          interpolation="monotoneX"
          animate={{ duration: 2000, onLoad: { duration: 1400 } }}
          style={{
            data: { stroke: "#F43F5E", strokeWidth: 2, strokeDasharray: "5, 5" }
          }}
        />
      </VictoryChart>
    </YStack>
  );
};

const LegendItem = ({ color, label }: { color: string, label: string }) => (
  <XStack alignItems="center" gap="$1.5">
    <Circle size={8} backgroundColor={color} />
    <Text color="white" fontSize={10} opacity={0.6}>{label}</Text>
  </XStack>
);
