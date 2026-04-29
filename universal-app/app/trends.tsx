import React, { useState, useEffect } from 'react';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { YStack, XStack, Text, Heading, Card, ScrollView, Theme, Button, Spinner, Progress } from 'tamagui';
import { ChevronLeft, TrendingUp, Target, Activity, Flame } from '@tamagui/lucide-icons';
import axios from 'axios';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';

const API_BASE = process.env.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000/v1";
const screenWidth = Dimensions.get("window").width;

export default function TrendsScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const [history, setHistory] = useState<any[]>([]);
  const [milestones, setMilestones] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [proactiveMsg, setProactiveMsg] = useState<string | null>(null);

  useEffect(() => {
    const userId = params.user_id || '00000000-0000-0000-0000-000000000000';
    
    Promise.all([
      axios.get(`${API_BASE}/users/${userId}/biometric-history`),
      axios.get(`${API_BASE}/users/${userId}/milestones`),
      axios.get(`${API_BASE}/coach/proactive-message?user_id=${userId}`)
    ])
    .then(([histRes, mileRes, proMsgRes]) => {
      // 데이터가 적을 경우 차트 라이브러리 시각화를 위해 목업 데이터 보정
      const apiHist = histRes.data || [];
      const chartData = apiHist.length > 1 ? apiHist : [
        { test_date: '03-01', weight: 80, fat_pct: 28 },
        { test_date: '03-15', weight: 78, fat_pct: 26 },
        { test_date: '04-01', weight: 76, fat_pct: 24 },
        ...apiHist
      ];
      
      setHistory(chartData);
      setMilestones(mileRes.data.milestones || []);
      setProactiveMsg(proMsgRes.data.proactive_message);
    })
    .catch(err => console.error(err))
    .finally(() => setLoading(false));
  }, [params.user_id]);

  const weightData = history.map(h => h.weight || 0);
  const labels = history.map(h => {
    const d = new Date(h.test_date);
    return isNaN(d.getTime()) ? String(h.test_date).substring(0,5) : `${d.getMonth()+1}/${d.getDate()}`;
  });

  const targetWeight = milestones.length > 0 ? milestones[milestones.length-1].target_weight : 65;
  const currentWeight = weightData[weightData.length-1] || 80;
  const startWeight = weightData[0] || 80;
  
  // 6개월 목표 대비 달성률 계산
  const totalDiff = Math.abs(startWeight - targetWeight);
  const currentDiff = Math.abs(startWeight - currentWeight);
  const progressPct = totalDiff === 0 ? 0 : Math.min(100, Math.max(0, (currentDiff / totalDiff) * 100));

  return (
    <Theme name="dark">
      <ScrollView backgroundColor="$bgDeep" flex={1}>
        <YStack padding="$5" gap="$6" paddingTop="$8" maxWidth={800} alignSelf="center" width="100%">
          
          <XStack alignItems="center" gap="$4">
            <Button size="$3" circular backgroundColor="$gray2" icon={<ChevronLeft size={20} color="white" />} onPress={() => router.back()} />
            <YStack>
              <Text color="white" opacity={0.5} fontSize={14} fontWeight="700" letterSpacing={1}>DATA VISUALIZATION</Text>
              <Heading color="white" fontSize={26} fontWeight="900">Health Trends 📈</Heading>
            </YStack>
          </XStack>

          {loading ? (
            <YStack padding="$10" alignItems="center"><Spinner size="large" color="$brandPrimary" /></YStack>
          ) : (
            <>
              {/* AI Proactive Coaching Notification */}
              {proactiveMsg && (
                <Card padding="$4" backgroundColor="rgba(244, 114, 182, 0.15)" borderRadius="$6" borderWidth={1} borderColor="rgba(244, 114, 182, 0.4)">
                  <XStack gap="$3" alignItems="flex-start">
                    <Flame color="#F472B6" size={24} marginTop={2} />
                    <YStack flex={1}>
                      <Text color="#F472B6" fontWeight="900" fontSize={13} letterSpacing={1}>AI PUSH NOTIFICATION</Text>
                      <Text color="white" fontSize={15} lineHeight={22} marginTop="$2">{proactiveMsg}</Text>
                    </YStack>
                  </XStack>
                </Card>
              )}

              {/* Time-series Chart */}
              <Card backgroundColor="$gray1" borderRadius="$6" borderWidth={1} borderColor="$gray3" padding="$4" gap="$4" overflow="hidden">
                <XStack alignItems="center" gap="$2">
                  <TrendingUp color="#3B82F6" size={20} />
                  <Heading color="white" fontSize={18} fontWeight="800">Weight Trend</Heading>
                </XStack>
                
                {weightData.length > 0 ? (
                  <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                    <LineChart
                      data={{
                        labels: labels.slice(-6),
                        datasets: [{ data: weightData.slice(-6) }]
                      }}
                      width={Math.max(screenWidth - 70, 320)}
                      height={220}
                      chartConfig={{
                        backgroundColor: "transparent",
                        backgroundGradientFrom: "#1C1C1E",
                        backgroundGradientTo: "#1C1C1E",
                        decimalPlaces: 1,
                        color: (opacity = 1) => `rgba(59, 130, 246, ${opacity})`,
                        labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
                        style: { borderRadius: 16 },
                        propsForDots: { r: "5", strokeWidth: "2", stroke: "#2563EB" }
                      }}
                      bezier
                      style={{ marginVertical: 8, borderRadius: 8, alignSelf: 'center' }}
                    />
                  </ScrollView>
                ) : (
                  <Text color="white" opacity={0.5}>데이터가 부족합니다.</Text>
                )}
              </Card>

              {/* Goal Progress Bar */}
              <Card backgroundColor="$gray1" borderRadius="$6" borderWidth={1} borderColor="$gray3" padding="$5" gap="$4">
                <XStack alignItems="center" gap="$2" marginBottom="$2">
                  <Target color="#10B981" size={20} />
                  <Heading color="white" fontSize={18} fontWeight="800">Goal Progress</Heading>
                </XStack>

                <YStack gap="$2">
                  <XStack justifyContent="space-between">
                    <Text color="white" opacity={0.6} fontSize={14}>Start: {startWeight}kg</Text>
                    <Text color="white" fontWeight="900" fontSize={14}>Target: {targetWeight}kg</Text>
                  </XStack>
                  <Progress size="$4" value={progressPct} backgroundColor="$gray3">
                    <Progress.Indicator backgroundColor="#10B981" animation="bouncy" />
                  </Progress>
                  <XStack justifyContent="space-between" marginTop="$1">
                    <Text color="#10B981" fontWeight="800" fontSize={14}>{progressPct.toFixed(1)}% Achieved</Text>
                    <Text color="white" opacity={0.5} fontSize={12}>Current: {currentWeight}kg</Text>
                  </XStack>
                </YStack>
              </Card>
              
            </>
          )}

        </YStack>
      </ScrollView>
    </Theme>
  );
}
