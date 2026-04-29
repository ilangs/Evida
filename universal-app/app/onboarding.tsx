import React, { useState } from 'react';
import { useRouter } from 'expo-router';
import { 
  YStack, 
  XStack, 
  Text, 
  Heading, 
  Button, 
  Input, 
  Switch, 
  Card,
  Circle,
  Dialog,
  Adapt,
  Unspaced,
  ScrollView,
  Theme,
  Sheet
} from 'tamagui';
import { 
  ShieldCheck, 
  ChevronRight, 
  ChevronLeft, 
  CheckCircle2, 
  Info,
  X
} from '@tamagui/lucide-icons';
import axios from 'axios';

const API_BASE = process.env.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000/v1";

const TERMS_DATA = {
  'PRIVACY POLICY': '개인정보 및 민감정보 수집/이용 동의 (필수)\n\n수집 항목: 성명, MBTI, 체성분 데이터, 혈액 검사 수치(혈당, 콜레스테롤 등).\n\n이용 목적: AI 기반 개인 맞춤형 식단/운동 가이드 생성 및 건강 데이터 추이 시각화.\n\n보유 기간: 회원 탈퇴 시 즉시 파기 (단, 법령에 따른 보존 필요 시 해당 기간 준수).',
  'MEDICAL DISCLAIMER': '건강 가이드 면책 고지 (중요)\n\n본 서비스가 제공하는 식단 및 운동 가이드는 AI 알고리즘과 의학적 근거를 바탕으로 생성되나, 의사의 전문적인 진단이나 치료를 대체할 수 없습니다. 사용자는 서비스 내용을 실천하기 전 반드시 의료 전문가와 상의해야 하며, 서비스 이용 중 발생하는 건강상의 변화에 대해 본 서비스는 의학적 책임을 지지 않습니다.',
  'TERMS OF SERVICE': '서비스 이용 약관 (수익화 관련)\n\n구독 결제는 한국 내 간편결제 시스템을 통하며, 디지털 콘텐츠 특성상 리포트 생성 후에는 환불이 제한될 수 있음을 명시합니다.'
};

export default function RootIndex() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [readDocs, setReadDocs] = useState<Set<string>>(new Set());
  const [form, setForm] = useState({
    name: '',
    age: '',
    gender: 'male',
    mbti: '',
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

  const handleNextStep2 = () => {
    const ageNum = parseInt(form.age);
    if (ageNum < 19) {
      alert("본 서비스는 성인 전용 건강 관리 솔루션입니다. 만 19세 미만은 가입이 제한됩니다.");
      return;
    }
    nextStep();
  };

  const markAsRead = (doc: string) => {
    const newDocs = new Set(readDocs);
    newDocs.add(doc);
    setReadDocs(newDocs);
  };

  const allDocsRead = readDocs.size === 3;

  const handleSubmit = async () => {
    if (form.goal_type === 'weight_loss') {
      // 6개월(24주) 기준 주당 감량 속도 계산
      const durationWeeks = 24; 
      const lossPerWeek = (form.start_weight - form.target_weight) / durationWeeks;
      
      if (lossPerWeek > 2.0) {
        alert("위험: 설정하신 목표는 주당 2kg 이상의 극단적인 감량을 요구합니다. 의학적 권장 감량 속도(주당 0.5~1kg)를 초과하므로 건강을 위해 목표를 수정해 주십시오.");
        return;
      }
    }

    setLoading(true);
    try {
      // Direct call to FastAPI backend
      const response = await axios.post(`${API_BASE}/users/register`, {
        ...form,
        age: parseInt(form.age) || 20 // Enforce integer
      });
      
      const userId = response.data.user_id;

      router.replace({
        pathname: '/dashboard',
        params: {
          user_id: userId, // Injecting UUID from backend
          name: form.name,
          mbti: form.mbti,
          goal_type: form.goal_type,
          goal_description: form.goal_description,
        }
      });
    } catch (err) {
      console.error("Backend connection failed:", err);
      // Fallback for UI visualization if DB is strictly unavailable
      router.replace({
        pathname: '/dashboard',
        params: {
          user_id: "mock_id",
          name: form.name,
          mbti: form.mbti,
          goal_type: form.goal_type,
          goal_description: form.goal_description,
        }
      });
    } finally {
      setLoading(false);
    }
  };

  const renderStep1 = () => (
    <YStack gap="$6" width="100%">
      <YStack gap="$2">
        <Heading color="$brandPrimary" fontSize={32} fontWeight="900">Safety First.</Heading>
        <Text color="white" opacity={0.6} fontSize={16}>서비스 이용을 위해 모든 약관을 확인해 주세요.</Text>
      </YStack>

      <YStack gap="$3">
        {Object.keys(TERMS_DATA).map(type => (
          <Dialog key={type} onOpenChange={(open) => open && markAsRead(type)}>
            <Dialog.Trigger asChild>
              <XStack 
                padding="$4" 
                backgroundColor="$gray2" 
                borderRadius="$5" 
                justifyContent="space-between" 
                alignItems="center"
                borderWidth={1}
                borderColor={readDocs.has(type) ? "$brandPrimary" : "$gray3"}
                animation="quick"
                pressStyle={{ scale: 0.98, opacity: 0.8 }}
              >
                <XStack gap="$3" alignItems="center">
                  <ShieldCheck size={20} color={readDocs.has(type) ? "#10B981" : "#444"} />
                  <Text color="white" fontWeight="600" fontSize={15}>{type}</Text>
                </XStack>
                {readDocs.has(type) ? (
                  <CheckCircle2 size={18} color="#10B981" />
                ) : (
                  <Button size="$2" circular icon={<Info size={16} />} backgroundColor="transparent" color="white" opacity={0.5} />
                )}
              </XStack>
            </Dialog.Trigger>

            <Adapt when="sm" platform="touch">
              <Sheet modal dismissOnSnapToBottom>
                <Sheet.Frame padding="$4" gap="$4">
                  <Adapt.Contents />
                </Sheet.Frame>
                <Sheet.Overlay backgroundColor="rgba(0,0,0,0.8)" />
              </Sheet>
            </Adapt>

            <Dialog.Portal>
              <Dialog.Overlay key="overlay" backgroundColor="rgba(0,0,0,0.8)" animation="quick" enterStyle={{ opacity: 0 }} exitStyle={{ opacity: 0 }} />
              <Dialog.Content key="content" bordered elevate backgroundColor="$gray1" borderRadius="$6" gap="$4" width="90%" maxWidth={400} animation="quick">
                <Dialog.Title fontSize={22} color="white" fontWeight="900">{type}</Dialog.Title>
                <ScrollView maxHeight={300}>
                  <Text color="white" opacity={0.7} fontSize={16} lineHeight={24}>
                    {TERMS_DATA[type as keyof typeof TERMS_DATA]}
                  </Text>
                </ScrollView>
                <Unspaced>
                  <Dialog.Close asChild>
                    <Button position="absolute" top="$3" right="$3" size="$2" circular icon={<X size={16} />} />
                  </Dialog.Close>
                </Unspaced>
                <Dialog.Close asChild>
                  <Button backgroundColor="$brandPrimary" color="white" fontWeight="800" height={55} borderRadius="$6" fontSize={18}>
                    확인했습니다
                  </Button>
                </Dialog.Close>
              </Dialog.Content>
            </Dialog.Portal>
          </Dialog>
        ))}
      </YStack>

      <XStack 
        padding="$5" 
        backgroundColor="rgba(16, 185, 129, 0.08)" 
        borderRadius="$5" 
        gap="$4" 
        alignItems="center"
        borderWidth={1}
        borderColor={allDocsRead ? "rgba(16, 185, 129, 0.4)" : "rgba(255,255,255,0.05)"}
        opacity={allDocsRead ? 1 : 0.5}
      >
        <Switch 
          disabled={!allDocsRead}
          checked={form.is_consented} 
          onCheckedChange={(val) => setForm({...form, is_consented: val})}
          backgroundColor={form.is_consented ? "$brandPrimary" : "$gray3"}
          borderWidth={0}
          minWidth={55}
          height={34}
          justifyContent="center"
          padding="$1"
        >
          <Switch.Thumb animation="bouncy" backgroundColor="green" height={22} width={22} />
        </Switch>
        <YStack>
          <Text color="white" fontSize={16} fontWeight="700">모든 법적 고지에 동의합니다.</Text>
          {!allDocsRead && <Text color="$brandPrimary" fontSize={11}>먼저 위 약관들을 하나씩 확인해 주세요.</Text>}
        </YStack>
      </XStack>

      <Button 
        disabled={!form.is_consented}
        onPress={nextStep}
        backgroundColor={form.is_consented ? "$brandPrimary" : "$gray3"}
        height={65}
        borderRadius="$5"
        iconAfter={<ChevronRight size={22} />}
      >
        <Text color="white" fontSize={20} fontWeight="900">Next Step</Text>
      </Button>
    </YStack>
  );

  const renderStep2 = () => (
    <YStack gap="$6" width="100%">
      <YStack gap="$2">
        <Heading color="$brandPrimary" fontSize={32} fontWeight="900">Who are you?</Heading>
        <Text color="white" opacity={0.6} fontSize={16}>프리미엄 관리를 위한 기초 정보를 입력해 주세요.</Text>
      </YStack>

      <YStack gap="$4">
        <Input 
          height={65}
          fontSize={20}
          value={form.name} 
          onChangeText={(text) => setForm({...form, name: text})}
          placeholder="성함 (Full Name)"
          placeholderTextColor="rgba(255, 255, 255, 0.4)"
          backgroundColor="$gray2"
          color="white"
          borderColor="$gray3"
          borderRadius="$5"
          paddingLeft="$5"
        />
        <XStack gap="$4">
          <Input 
            flex={1}
            height={65}
            fontSize={20}
            value={form.age.toString()} 
            onChangeText={(text) => setForm({...form, age: text.replace(/[^0-9]/g, '')})}
            placeholder="나이"
            placeholderTextColor="rgba(255, 255, 255, 0.4)"
            backgroundColor="$gray2"
            color="white"
            borderColor="$gray3"
            borderRadius="$5"
            paddingLeft="$5"
            keyboardType="number-pad"
          />
          <Input 
            flex={1}
            height={65}
            fontSize={20}
            value={form.mbti} 
            onChangeText={(text) => setForm({...form, mbti: text.toUpperCase()})}
            maxLength={4}
            autoCapitalize="characters"
            placeholder="MBTI"
            placeholderTextColor="rgba(255, 255, 255, 0.4)"
            backgroundColor="$gray2"
            color="white"
            borderColor="$gray3"
            borderRadius="$5"
            paddingLeft="$5"
          />
        </XStack>
      </YStack>

      <XStack gap="$4">
        <Button flex={1} onPress={prevStep} backgroundColor="$gray3" color="white" height={65} borderRadius="$5" fontSize={18} fontWeight="700">Back</Button>
        <Button 
          flex={2} 
          disabled={!form.name || !form.age || !form.mbti || form.mbti.length !== 4}
          onPress={handleNextStep2}
          backgroundColor="$brandPrimary"
          color="white"
          height={65}
          borderRadius="$5"
          fontSize={18}
          fontWeight="900"
          iconAfter={<ChevronRight size={20} />}
        >Continue</Button>
      </XStack>
    </YStack>
  );

  const renderStep3 = () => (
    <YStack gap="$6" width="100%">
      <YStack gap="$2">
        <Heading color="$brandPrimary" fontSize={32} fontWeight="900">Mission Setup.</Heading>
        <Text color="white" opacity={0.6} fontSize={16}>달성하고 싶은 목표를 수립합니다.</Text>
      </YStack>

      <YStack gap="$5">
        <XStack backgroundColor="transparent" gap="$4" height={65}>
          <Button 
            flex={1} 
            height="100%"
            backgroundColor={form.goal_type === 'weight_loss' ? '$brandPrimary' : '$gray2'}
            color={form.goal_type === 'weight_loss' ? 'white' : '$gray10'}
            onPress={() => setForm({...form, goal_type: 'weight_loss'})}
            borderRadius="$4"
            borderWidth={1}
            borderColor={form.goal_type === 'weight_loss' ? '$brandPrimary' : '$gray4'}
            fontSize={18}
            fontWeight="800"
          >Weight Loss</Button>
          <Button 
            flex={1} 
            height="100%"
            backgroundColor={form.goal_type === 'weight_gain' ? '$brandPrimary' : '$gray2'}
            color={form.goal_type === 'weight_gain' ? 'white' : '$gray10'}
            onPress={() => setForm({...form, goal_type: 'weight_gain'})}
            borderRadius="$4"
            borderWidth={1}
            borderColor={form.goal_type === 'weight_gain' ? '$brandPrimary' : '$gray4'}
            fontSize={18}
            fontWeight="800"
          >Weight Gain</Button>
        </XStack>
        <Input 
          height={65}
          fontSize={18}
          value={form.goal_description} 
          onChangeText={(text) => setForm({...form, goal_description: text})}
          placeholder="목표 설명 (예: 6개월 5kg 감량)"
          placeholderTextColor="rgba(255, 255, 255, 0.4)"
          backgroundColor="$gray2"
          color="white"
          borderColor="$gray3"
          borderRadius="$5"
          paddingLeft="$5"
        />
        <XStack gap="$4">
          <Input 
            flex={1} height={65} fontSize={18}
            value={form.start_weight ? form.start_weight.toString() : ''} 
            onChangeText={(t) => setForm({...form, start_weight: parseFloat(t) || 0})}
            placeholder="현재 체중(kg)" backgroundColor="$gray2" color="white" borderColor="$gray3" borderRadius="$5" paddingLeft="$5" keyboardType="numeric"
          />
          <Input 
            flex={1} height={65} fontSize={18}
            value={form.target_weight ? form.target_weight.toString() : ''} 
            onChangeText={(t) => setForm({...form, target_weight: parseFloat(t) || 0})}
            placeholder="목표 체중(kg)" backgroundColor="$gray2" color="white" borderColor="$gray3" borderRadius="$5" paddingLeft="$5" keyboardType="numeric"
          />
        </XStack>
      </YStack>

      <XStack gap="$4">
        <Button flex={1} onPress={prevStep} backgroundColor="$gray3" color="white" height={65} borderRadius="$5" fontSize={18} fontWeight="700" icon={<ChevronLeft size={20} />}>Back</Button>
        <Button 
          flex={2} 
          loading={loading}
          onPress={handleSubmit}
          backgroundColor="$brandPrimary"
          color="white"
          height={65}
          borderRadius="$5"
          fontSize={18}
          fontWeight="900"
          iconAfter={<CheckCircle2 size={20} />}
        >Start Agent</Button>
      </XStack>
    </YStack>
  );

  return (
    <YStack flex={1} backgroundColor="$bgDeep" alignItems="center" justifyContent="center" padding="$5">
      <Card 
        width="100%" 
        maxWidth={500} 
        padding="$8" 
        backgroundColor="$gray1" 
        borderRadius="$10" 
        borderWidth={1} 
        borderColor="$gray3"
        elevation={20}
        shadowColor="black"
        shadowRadius={40}
        shadowOpacity={0.4}
      >
        <XStack gap="$3" marginBottom="$10" justifyContent="center">
          {[1, 2, 3].map(s => (
            <Circle key={s} size={10} backgroundColor={step >= s ? "$brandPrimary" : "$gray3"} opacity={step >= s ? 1 : 0.4} />
          ))}
        </XStack>

        {step === 1 && renderStep1()}
        {step === 2 && renderStep2()}
        {step === 3 && renderStep3()}
      </Card>
      
      <Text marginTop="$6" color="white" opacity={0.3} fontSize={12} letterSpacing={2}>VITAL INTELLIGENCE PLATFORM 2026</Text>
    </YStack>
  );
}
