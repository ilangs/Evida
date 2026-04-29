import React, { useState, useEffect } from 'react';
import { useLocalSearchParams, useRouter } from 'expo-router';
import {
  YStack,
  XStack,
  Text,
  Heading,
  Card,
  ScrollView,
  Theme,
  Button,
  Circle,
  Separator,
  Spinner
} from 'tamagui';
import {
  ChevronLeft,
  Flame,
  Dumbbell,
  Apple,
  CheckCircle2,
  BrainCircuit,
  Clock,
  AlertTriangle,
  ShieldAlert,
  BookOpen,
  ExternalLink,
  ChevronDown,
  ChevronUp
} from '@tamagui/lucide-icons';
import axios from 'axios';
import { Linking } from 'react-native';

const API_BASE = process.env.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000/v1";
const DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];

// ── 위험 지표 뱃지 ───────────────────────────────────────────────
const RiskBadge = ({ flag }: { flag: any }) => {
  const isDanger = flag.level === 'danger';
  const color = isDanger ? '#F87171' : '#FBBF24';
  const bg = isDanger ? 'rgba(248,113,113,0.1)' : 'rgba(251,191,36,0.1)';
  return (
    <XStack backgroundColor={bg} padding="$3" borderRadius="$4" gap="$2" alignItems="flex-start">
      <ShieldAlert size={16} color={color} marginTop={2} />
      <YStack flex={1} gap="$1">
        <Text color={color} fontWeight="900" fontSize={12}>{flag.label}: {flag.value}{flag.unit}</Text>
        <Text color="white" opacity={0.7} fontSize={12} lineHeight={18}>{flag.message}</Text>
      </YStack>
    </XStack>
  );
};

// ── 운동 항목 ────────────────────────────────────────────────────
const Bullet = ({ text }: { text: string }) => (
  <XStack gap="$2" alignItems="center">
    <Circle size={6} backgroundColor="$brandPrimary" opacity={0.5} />
    <Text color="white" opacity={0.8} fontSize={14}>{text}</Text>
  </XStack>
);

// ── 식사 행 ──────────────────────────────────────────────────────
const MealRow = ({ time, meal, calories, protein, carb, fat }:
  { time: string; meal: string; calories: number; protein: number; carb: number; fat: number }) => (
  <XStack justifyContent="space-between" alignItems="center">
    <YStack flex={1}>
      <Text color="white" fontSize={12} opacity={0.5} fontWeight="700">{time.toUpperCase()}</Text>
      <Text color="white" fontSize={15} fontWeight="800" marginTop="$1">{meal}</Text>
    </YStack>
    <YStack alignItems="flex-end" gap="$1">
      <Text color="#F472B6" fontSize={12} fontWeight="800">{calories} kcal</Text>
      <Text color="white" opacity={0.4} fontSize={10}>{carb}C / {protein}P / {fat}F</Text>
    </YStack>
  </XStack>
);

export default function Planner() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const [selectedDay, setSelectedDay] = useState('MON');
  const [workoutDone, setWorkoutDone] = useState(false);
  const [dietDone, setDietDone] = useState(false);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<any>(null);
  const [legacyFeedback, setLegacyFeedback] = useState<any>(null);
  const [expandedCitation, setExpandedCitation] = useState<string | null>(null);

  useEffect(() => {
    const userId = params.user_id;
    if (!userId || userId === 'mock_id') return;

    // 새로운 통합 분석 리포트 요청
    setLoading(true);
    axios.post(`${API_BASE}/health/analyze-report?user_id=${userId}`)
      .then(res => {
        setReport(res.data.report);
        // 선택된 요일을 오늘 요일로 초기화
        const todayIdx = new Date().getDay(); // 0=Sun
        const dayMap = ['SUN','MON','TUE','WED','THU','FRI','SAT'];
        setSelectedDay(dayMap[todayIdx]);
      })
      .catch(() => {
        // 폴백: 기존 ai-feedback 엔드포인트
        axios.get(`${API_BASE}/coach/ai-feedback?user_id=${userId}`)
          .then(res => setLegacyFeedback(res.data))
          .catch(err => console.error("Coach API Error:", err));
      })
      .finally(() => setLoading(false));
  }, [params.user_id]);

  // 선택된 요일의 운동 데이터
  const todayWorkout = report?.weekly_workout?.find((w: any) => w.day === selectedDay);
  const meals = report?.daily_meals;

  // AI 피드백 텍스트 (legacy fallback or report summary)
  const aiText = report
    ? `${report.summary}\n\n💡 ${report.priority_message}\n\n${report.disclaimer}`
    : legacyFeedback?.ai_feedback
    ?? "ENTP 성향은 반복적인 루틴을 지루해합니다!\n\n데이터를 입력하면 AI가 맞춤형 주간 플랜을 생성합니다.\n\n※ 본 서비스는 의학적 진단이나 치료를 대신할 수 없습니다.";

  return (
    <Theme name="dark">
      <ScrollView backgroundColor="$bgDeep" flex={1}>
        <YStack padding="$5" gap="$5" paddingTop="$8" maxWidth={800} alignSelf="center" width="100%">

          {/* Header */}
          <XStack alignItems="center" gap="$4" marginBottom="$2">
            <Button size="$3" circular backgroundColor="$gray2" icon={<ChevronLeft size={20} color="white" />} onPress={() => router.back()} />
            <YStack>
              <Text color="white" opacity={0.5} fontSize={14} fontWeight="700" letterSpacing={1}>AI WEEKLY PLANNER</Text>
              <Heading color="white" fontSize={26} fontWeight="900">Your Action Plan 🚀</Heading>
            </YStack>
          </XStack>

          {/* 로딩 상태 */}
          {loading && (
            <XStack justifyContent="center" alignItems="center" padding="$6" gap="$3">
              <Spinner size="large" color="$brandPrimary" />
              <Text color="white" opacity={0.6}>AI가 데이터를 분석 중입니다...</Text>
            </XStack>
          )}

          {/* AI 코칭 카드 */}
          {!loading && (
            <Card padding="$4" backgroundColor="rgba(59, 130, 246, 0.1)" borderRadius="$6" borderWidth={1} borderColor="rgba(59, 130, 246, 0.3)">
              <XStack gap="$3" alignItems="flex-start">
                <BrainCircuit color="#3B82F6" size={24} marginTop={2} />
                <YStack flex={1}>
                  <Text color="#3B82F6" fontWeight="900" fontSize={13} letterSpacing={1}>AI HEALTH AGENT</Text>
                  <YStack marginTop="$3" gap="$2">
                    {aiText.split('\n').map((line: string, i: number) => {
                      const trimmed = line.trim();
                      if (!trimmed) return null;
                      if (trimmed.startsWith('※')) {
                        return (
                          <Text key={i} color="white" opacity={0.8} fontSize={14} marginTop="$2" numberOfLines={1}>
                            {trimmed}
                          </Text>
                        );
                      }
                      if (trimmed.startsWith('💡')) {
                        return (
                          <Text key={i} color="#FBBF24" fontSize={14} fontWeight="800" marginTop="$1" lineHeight={22}>
                            {trimmed}
                          </Text>
                        );
                      }
                      return (
                        <Text key={i} color="white" fontSize={16} opacity={0.9} lineHeight={26}>
                          {trimmed}
                        </Text>
                      );
                    })}
                  </YStack>
                </YStack>
              </XStack>
            </Card>
          )}

          {/* 위험 지표 경고 뱃지 */}
          {report?.risk_flags?.length > 0 && (
            <YStack gap="$2">
              <XStack gap="$2" alignItems="center">
                <AlertTriangle size={16} color="#F87171" />
                <Text color="#F87171" fontWeight="900" fontSize={13} letterSpacing={1}>HEALTH RISK ALERT</Text>
              </XStack>
              {report.risk_flags.map((flag: any, i: number) => (
                <RiskBadge key={i} flag={flag} />
              ))}
            </YStack>
          )}

          {/* Day Selector */}
          <ScrollView horizontal showsHorizontalScrollIndicator={false} paddingVertical="$2">
            <XStack gap="$2" paddingRight="$5">
              {DAYS.map((day) => {
                const dayWorkout = report?.weekly_workout?.find((w: any) => w.day === day);
                const isRest = dayWorkout?.title === 'Rest';
                return (
                  <Button
                    key={day}
                    width={65}
                    height={75}
                    backgroundColor={day === selectedDay ? '$brandPrimary' : '$gray2'}
                    borderWidth={1}
                    borderColor={day === selectedDay ? '$brandPrimary' : '$gray3'}
                    borderRadius="$5"
                    onPress={() => { setSelectedDay(day); setWorkoutDone(false); }}
                    flexDirection="column"
                    gap="$1"
                    animation="quick"
                    pressStyle={{ scale: 0.95 }}
                  >
                    <Text color={day === selectedDay ? 'white' : '$gray10'} fontWeight="800" fontSize={15}>{day}</Text>
                    {isRest && <Text color={day === selectedDay ? 'white' : '$gray10'} fontSize={8} opacity={0.6}>REST</Text>}
                    {!isRest && dayWorkout && <Circle size={6} backgroundColor={day === selectedDay ? 'white' : '$brandPrimary'} />}
                  </Button>
                );
              })}
            </XStack>
          </ScrollView>

          {/* Today's Workout */}
          <YStack gap="$3" marginTop="$2">
            <Heading color="white" fontSize={20} fontWeight="900">Today's Workout</Heading>
            <Card backgroundColor="$gray1" borderRadius="$6" borderWidth={1} borderColor={workoutDone ? "$brandPrimary" : "$gray3"} padding="$5" animation="bouncy">
              <XStack justifyContent="space-between" alignItems="flex-start" marginBottom="$4">
                <XStack gap="$3" alignItems="center">
                  <YStack backgroundColor={workoutDone ? "rgba(16,185,129,0.2)" : "rgba(251,191,36,0.1)"} padding="$3" borderRadius="$4">
                    <Dumbbell color={workoutDone ? "#10B981" : "#FBBF24"} size={26} />
                  </YStack>
                  <YStack>
                    <Text color="white" fontSize={18} fontWeight="800">
                      {todayWorkout?.title ?? 'Upper Body & Core'}
                    </Text>
                    <XStack gap="$2" alignItems="center" marginTop="$1">
                      <Clock size={12} color="white" opacity={0.5} />
                      <Text color="white" opacity={0.5} fontSize={12}>
                        {todayWorkout ? `${todayWorkout.duration_min} Min` : '45 Min'} | AI Optimized
                      </Text>
                    </XStack>
                  </YStack>
                </XStack>
                {todayWorkout?.duration_min > 0 && (
                  <XStack alignItems="center" gap="$1" backgroundColor="rgba(255,255,255,0.1)" paddingHorizontal="$2" paddingVertical="$1" borderRadius="$100">
                    <Flame size={12} color="#F87171" />
                    <Text color="#F87171" fontWeight="800" fontSize={12}>
                      {Math.round((todayWorkout?.duration_min ?? 45) * 7)} kcal
                    </Text>
                  </XStack>
                )}
              </XStack>

              <Separator borderColor="$gray3" marginVertical="$3" />

              <YStack gap="$2" marginBottom="$4">
                {todayWorkout?.detail
                  ? todayWorkout.detail.split('/').map((item: string, i: number) => (
                      <Bullet key={i} text={item.trim()} />
                    ))
                  : (
                    <>
                      <Bullet text="Dumbbell Bench Press - 4 Sets x 12 Reps" />
                      <Bullet text="Lateral Raises - 3 Sets x 15 Reps" />
                      <Bullet text="Plank Holds - 3 Sets x 60 Secs" />
                    </>
                  )
                }
              </YStack>

              <Button
                backgroundColor={workoutDone ? "rgba(16,185,129,0.1)" : "$brandPrimary"}
                color={workoutDone ? "#10B981" : "white"}
                borderWidth={1}
                borderColor={workoutDone ? "#10B981" : "transparent"}
                fontWeight="900"
                fontSize={16}
                height={50}
                icon={workoutDone ? <CheckCircle2 size={20} /> : undefined}
                onPress={() => setWorkoutDone(!workoutDone)}
              >
                {workoutDone ? 'Workout Completed! ✅' : 'Mark as Done'}
              </Button>
            </Card>
          </YStack>

          {/* Nutrition Plan */}
          <YStack gap="$3" marginTop="$2" marginBottom="$10">
            <Heading color="white" fontSize={20} fontWeight="900">Nutrition Plan</Heading>
            <Card backgroundColor="$gray1" borderRadius="$6" borderWidth={1} borderColor={dietDone ? "$brandPrimary" : "$gray3"} padding="$5" animation="bouncy">
              <XStack justifyContent="space-between" alignItems="flex-start" marginBottom="$4">
                <XStack gap="$3" alignItems="center">
                  <YStack backgroundColor={dietDone ? "rgba(16,185,129,0.2)" : "rgba(244,114,182,0.1)"} padding="$3" borderRadius="$4">
                    <Apple color={dietDone ? "#10B981" : "#F472B6"} size={26} />
                  </YStack>
                  <YStack>
                    <Text color="white" fontSize={18} fontWeight="800">AI Personalized Diet</Text>
                    <XStack gap="$2" alignItems="center" marginTop="$1">
                      <Clock size={12} color="white" opacity={0.5} />
                      <Text color="white" opacity={0.5} fontSize={12}>
                        Target: {meals
                          ? Object.values(meals).reduce((sum: number, m: any) => sum + (m.calories ?? 0), 0)
                          : 1700
                        } kcal
                      </Text>
                    </XStack>
                  </YStack>
                </XStack>
              </XStack>

              <Separator borderColor="$gray3" marginVertical="$3" />

              <YStack gap="$4" marginBottom="$4">
                {meals ? (
                  Object.entries(meals).map(([mealTime, mealData]: [string, any]) => (
                    <MealRow
                      key={mealTime}
                      time={mealTime}
                      meal={mealData.menu}
                      calories={mealData.calories}
                      protein={mealData.protein_g}
                      carb={mealData.carb_g}
                      fat={mealData.fat_g}
                    />
                  ))
                ) : (
                  <>
                    <MealRow time="Breakfast" meal="Oatmeal & 2 Boiled Eggs" calories={380} protein={20} carb={40} fat={10} />
                    <MealRow time="Lunch" meal="Grilled Chicken Salad" calories={520} protein={45} carb={15} fat={12} />
                    <MealRow time="Dinner" meal="Salmon with Quinoa" calories={580} protein={38} carb={40} fat={22} />
                  </>
                )}
              </YStack>

              {/* 의학적 근거 */}
              {report?.medical_evidence && (
                <XStack backgroundColor="rgba(99,102,241,0.1)" padding="$3" borderRadius="$4" marginBottom="$4" gap="$2">
                  <Text color="#818CF8" fontSize={10} fontWeight="900">근거</Text>
                  <Text color="white" opacity={0.6} fontSize={11} flex={1} lineHeight={16}>{report.medical_evidence}</Text>
                </XStack>
              )}

              <Button
                backgroundColor={dietDone ? "rgba(16,185,129,0.1)" : "$gray2"}
                color={dietDone ? "#10B981" : "white"}
                borderWidth={1}
                borderColor={dietDone ? "#10B981" : "$gray3"}
                fontWeight="900"
                fontSize={16}
                height={50}
                icon={dietDone ? <CheckCircle2 size={20} /> : undefined}
                onPress={() => setDietDone(!dietDone)}
              >
                {dietDone ? 'All Meals Tracked! ✅' : 'Complete Diet for Today'}
              </Button>
            </Card>
          </YStack>

          {/* ── 논문 인용 섹션 ─────────────────────────────── */}
          {report?.citations?.length > 0 && (
            <YStack gap="$3" marginTop="$2" marginBottom="$10">
              <XStack alignItems="center" gap="$2">
                <BookOpen size={16} color="#818CF8" />
                <Text color="#818CF8" fontWeight="900" fontSize={13} letterSpacing={1}>
                  MEDICAL REFERENCES
                </Text>
                <XStack
                  backgroundColor="rgba(129,140,248,0.15)"
                  paddingHorizontal="$2"
                  paddingVertical={2}
                  borderRadius="$10"
                >
                  <Text color="#818CF8" fontSize={11} fontWeight="700">
                    {report.citations.length}편
                  </Text>
                </XStack>
              </XStack>

              <Text color="white" opacity={0.4} fontSize={12} lineHeight={18}>
                본 AI 권고안은 아래 의학 문헌 및 임상 가이드라인을 근거로 작성되었습니다.
              </Text>

              {report.citations.map((cite: any, idx: number) => {
                const isExpanded = expandedCitation === cite.id;
                const categoryColor: Record<string, string> = {
                  weight_loss:      '#34D399',
                  blood_glucose:    '#FBBF24',
                  cholesterol:      '#F87171',
                  muscle:           '#60A5FA',
                  exercise:         '#A78BFA',
                  korean_guideline: '#FB923C',
                  lifestyle:        '#F472B6',
                };
                const tagColor = categoryColor[cite.category] ?? '#94A3B8';

                return (
                  <Card
                    key={cite.id || idx}
                    backgroundColor="$gray1"
                    borderRadius="$5"
                    borderWidth={1}
                    borderColor={isExpanded ? 'rgba(129,140,248,0.4)' : '$gray3'}
                    padding="$4"
                    animation="quick"
                    pressStyle={{ scale: 0.98 }}
                    onPress={() => setExpandedCitation(isExpanded ? null : cite.id)}
                  >
                    {/* 헤더 행 */}
                    <XStack justifyContent="space-between" alignItems="flex-start">
                      <YStack flex={1} gap="$1" paddingRight="$3">
                        {/* 카테고리 태그 */}
                        <XStack
                          backgroundColor={`${tagColor}22`}
                          paddingHorizontal="$2"
                          paddingVertical={2}
                          borderRadius="$10"
                          alignSelf="flex-start"
                        >
                          <Text color={tagColor} fontSize={10} fontWeight="800" letterSpacing={0.5}>
                            {cite.category.replace('_', ' ').toUpperCase()}
                          </Text>
                        </XStack>

                        {/* 논문 제목 */}
                        <Text
                          color="white"
                          fontSize={14}
                          fontWeight="800"
                          lineHeight={20}
                          numberOfLines={isExpanded ? undefined : 2}
                        >
                          [{idx + 1}] {cite.title}
                        </Text>

                        {/* 저자·저널·연도 */}
                        <Text color="white" opacity={0.5} fontSize={11} lineHeight={16}>
                          {[cite.authors, cite.journal, cite.pub_year].filter(Boolean).join(' · ')}
                        </Text>
                      </YStack>

                      {/* 펼치기/접기 아이콘 */}
                      {isExpanded
                        ? <ChevronUp size={16} color="white" opacity={0.4} />
                        : <ChevronDown size={16} color="white" opacity={0.4} />}
                    </XStack>

                    {/* 펼친 상태: 발췌 + DOI 링크 */}
                    {isExpanded && (
                      <YStack marginTop="$3" gap="$3">
                        <Separator borderColor="rgba(129,140,248,0.2)" />

                        {/* 발췌 내용 */}
                        <Text color="white" opacity={0.7} fontSize={13} lineHeight={20}>
                          {cite.excerpt}
                        </Text>

                        {/* DOI 링크 */}
                        {cite.source && (
                          <Button
                            size="$2"
                            backgroundColor="rgba(129,140,248,0.1)"
                            borderWidth={1}
                            borderColor="rgba(129,140,248,0.3)"
                            borderRadius="$4"
                            color="#818CF8"
                            fontSize={12}
                            fontWeight="700"
                            icon={<ExternalLink size={12} />}
                            onPress={() => Linking.openURL(cite.source)}
                            alignSelf="flex-start"
                          >
                            원문 보기 (DOI)
                          </Button>
                        )}
                      </YStack>
                    )}
                  </Card>
                );
              })}
            </YStack>
          )}

        </YStack>
      </ScrollView>
    </Theme>
  );
}
