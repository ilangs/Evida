import React, { useState } from 'react';
import { 
  YStack, 
  XStack, 
  Text, 
  Heading, 
  Button, 
  Input, 
  Switch, 
  ScrollView,
  Theme,
  Card,
  Circle,
  useTheme
} from 'tamagui';
import { MotiView, AnimatePresence } from 'moti';
import { 
  ShieldCheck, 
  UserCircle, 
  Target, 
  ChevronRight, 
  ChevronLeft, 
  CheckCircle2, 
  Info,
  Scale
} from '@tamagui/lucide-icons';
import axios from 'axios';

const API_BASE = "http://localhost:8000/v1";

interface OnboardingProps {
  onComplete: (userId: string) => void;
  openLegal: (type: string) => void;
}

export const OnboardingUniversal = ({ onComplete, openLegal }: OnboardingProps) => {
  const theme = useTheme();
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
      // Native environments should use Alert.alert, Web uses window.alert
      alert("Registration failed. Please check the inputs.");
    } finally {
      setLoading(false);
    }
  };

  const renderStep1 = () => (
    <MotiView
      from={{ opacity: 0, translateX: 50 }}
      animate={{ opacity: 1, translateX: 0 }}
      exit={{ opacity: 0, translateX: -50 }}
      transition={{ type: 'timing', duration: 500 }}
      style={{ width: '100%', gap: 24 }}
    >
      <YStack gap="$2">
        <Heading color="$primary" size="$9" fontWeight="900">Safety First.</Heading>
        <Text color="$color" opacity={0.6} size="$3">서비스 이용을 위해 법적 약관 및 면책 사항 동의가 필요합니다.</Text>
      </YStack>

      <YStack gap="$3">
        {['PRIVACY', 'TERMS', 'DISCLAIMER'].map(type => (
          <XStack 
            key={type} 
            padding="$4" 
            backgroundColor="$bgCard" 
            borderWidth={1} 
            borderColor="$borderColor" 
            borderRadius="$6" 
            justifyContent="space-between" 
            alignItems="center"
          >
            <Text size="$3" fontWeight="700">
              {type === 'PRIVACY' ? '개인정보 처리방침 (필수)' : type === 'TERMS' ? '서비스 이용약관 (필수)' : '의료 법적 고지 (필수)'}
            </Text>
            <Button 
              size="$2" 
              themeInverse 
              onPress={() => openLegal(type)}
              backgroundColor="$primary"
              borderRadius="$4"
            >
              <Text size="$1" fontWeight="900">VIEW</Text>
            </Button>
          </XStack>
        ))}
      </YStack>

      <XStack 
        padding="$6" 
        backgroundColor="$primary" 
        opacity={0.1}
        borderRadius="$8" 
        borderWidth={1} 
        borderColor="$primary" 
        gap="$4" 
        alignItems="center"
      >
        <Switch 
          size="$3" 
          checked={form.is_consented} 
          onCheckedChange={(val) => setForm({...form, is_consented: val})}
        />
        <Text size="$3" fontWeight="700" color="white">모든 법적 고지 및 데이터 수집에 동의합니다.</Text>
      </XStack>

      <Button 
        disabled={!form.is_consented}
        onPress={nextStep}
        backgroundColor={form.is_consented ? "$primary" : "$gray8"}
        height={60}
        borderRadius="$6"
        iconAfter={<ChevronRight size={20} />}
      >
        <Text fontWeight="900">Next Step</Text>
      </Button>
    </MotiView>
  );

  const renderStep2 = () => (
    <MotiView
      from={{ opacity: 0, translateX: 50 }}
      animate={{ opacity: 1, translateX: 0 }}
      exit={{ opacity: 0, translateX: -50 }}
      transition={{ type: 'timing', duration: 500 }}
      style={{ width: '100%', gap: 24 }}
    >
      <YStack gap="$2">
        <Heading color="$primary" size="$9" fontWeight="900">Who are you?</Heading>
        <Text color="$color" opacity={0.6} size="$3">초개인화 가이드를 위해 당신의 페르소나를 입력해 주세요.</Text>
      </YStack>

      <YStack gap="$4">
        <XStack gap="$4">
          <YStack flex={1} gap="$2">
            <Text size="$1" fontWeight="900" opacity={0.5} paddingLeft="$2">FULL NAME</Text>
            <Input 
              value={form.name} 
              onChangeText={(text) => setForm({...form, name: text})}
              placeholder="홍길동"
              backgroundColor="$bgCard"
              borderColor="$borderColor"
            />
          </YStack>
          <YStack flex={1} gap="$2">
            <Text size="$1" fontWeight="900" opacity={0.5} paddingLeft="$2">AGE</Text>
            <Input 
              keyboardType="number-pad"
              value={form.age.toString()} 
              onChangeText={(text) => setForm({...form, age: parseInt(text) || 0})}
              backgroundColor="$bgCard"
              borderColor="$borderColor"
            />
          </YStack>
        </XStack>

        <XStack gap="$4">
          <YStack flex={1} gap="$2">
            <Text size="$1" fontWeight="900" opacity={0.5} paddingLeft="$2">MBTI</Text>
            <Input 
              value={form.mbti} 
              onChangeText={(text) => setForm({...form, mbti: text.toUpperCase()})}
              maxLength={4}
              backgroundColor="$bgCard"
              borderColor="$borderColor"
            />
          </YStack>
          <YStack flex={1} gap="$2">
            <Text size="$1" fontWeight="900" opacity={0.5} paddingLeft="$2">GENDER</Text>
            <XStack backgroundColor="$bgCard" borderRadius="$4" borderWidth={1} borderColor="$borderColor" padding="$2" gap="$2">
              <Button 
                flex={1} 
                size="$2" 
                backgroundColor={form.gender === 'male' ? '$primary' : 'transparent'}
                onPress={() => setForm({...form, gender: 'male'})}
              >Male</Button>
              <Button 
                flex={1} 
                size="$2" 
                backgroundColor={form.gender === 'female' ? '$primary' : 'transparent'}
                onPress={() => setForm({...form, gender: 'female'})}
              >Female</Button>
            </XStack>
          </YStack>
        </XStack>
      </YStack>

      <XStack gap="$3">
        <Button flex={1} onPress={prevStep} backgroundColor="$bgCard" icon={<ChevronLeft size={18} />}>Back</Button>
        <Button 
          flex={2} 
          disabled={!form.name || !form.mbti}
          onPress={nextStep}
          backgroundColor="$primary"
          iconAfter={<ChevronRight size={18} />}
        >Continue</Button>
      </XStack>
    </MotiView>
  );

  const renderStep3 = () => (
    <MotiView
      from={{ opacity: 0, translateX: 50 }}
      animate={{ opacity: 1, translateX: 0 }}
      exit={{ opacity: 0, translateX: -50 }}
      transition={{ type: 'timing', duration: 500 }}
      style={{ width: '100%', gap: 24 }}
    >
      <YStack gap="$2">
        <Heading color="$primary" size="$9" fontWeight="900">Mission Setup.</Heading>
        <Text color="$color" opacity={0.6} size="$3">달성하고 싶은 목표와 생활 패턴을 적어주세요.</Text>
      </YStack>

      <YStack gap="$4">
        <YStack gap="$2">
          <Text size="$1" fontWeight="900" opacity={0.5} paddingLeft="$2">MISSION TYPE</Text>
          <XStack backgroundColor="$bgCard" borderRadius="$4" borderWidth={1} borderColor="$borderColor" padding="$2" gap="$2">
            <Button 
              flex={1} 
              size="$2" 
              backgroundColor={form.goal_type === 'weight_loss' ? '$secondary' : 'transparent'}
              onPress={() => setForm({...form, goal_type: 'weight_loss'})}
            >Weight Loss</Button>
            <Button 
              flex={1} 
              size="$2" 
              backgroundColor={form.goal_type === 'weight_gain' ? '$primary' : 'transparent'}
              onPress={() => setForm({...form, goal_type: 'weight_gain'})}
            >Weight Gain</Button>
          </XStack>
        </YStack>

        <YStack gap="$2">
          <Text size="$1" fontWeight="900" opacity={0.5} paddingLeft="$2">GOAL DESCRIPTION</Text>
          <Input 
            value={form.goal_description} 
            onChangeText={(text) => setForm({...form, goal_description: text})}
            placeholder={form.goal_type === 'weight_loss' ? "예: 6개월간 지방 5kg 감량" : "예: 6개월간 근육 3kg 증량"}
            backgroundColor="$bgCard"
            borderColor="$borderColor"
          />
        </YStack>

        <XStack gap="$4">
          <YStack flex={1} gap="$2">
            <Text size="$1" fontWeight="900" opacity={0.5} paddingLeft="$2">START WEIGHT</Text>
            <Input 
              keyboardType="decimal-pad"
              value={form.start_weight.toString()} 
              onChangeText={(text) => setForm({...form, start_weight: parseFloat(text) || 0})}
              backgroundColor="$bgCard"
              borderColor="$borderColor"
            />
          </YStack>
          <YStack flex={1} gap="$2">
            <Text size="$1" fontWeight="900" opacity={0.5} paddingLeft="$2">TARGET WEIGHT</Text>
            <Input 
              keyboardType="decimal-pad"
              value={form.target_weight.toString()} 
              onChangeText={(text) => setForm({...form, target_weight: parseFloat(text) || 0})}
              backgroundColor="$bgCard"
              borderColor="$borderColor"
            />
          </YStack>
        </XStack>
      </YStack>

      <XStack gap="$3">
        <Button flex={1} onPress={prevStep} backgroundColor="$bgCard" icon={<ChevronLeft size={18} />}>Back</Button>
        <Button 
          flex={2} 
          loading={loading}
          onPress={handleSubmit}
          backgroundColor="$primary"
          iconAfter={<CheckCircle2 size={18} />}
        >Start My Journey</Button>
      </XStack>
    </MotiView>
  );

  return (
    <YStack flex={1} backgroundColor="$background" padding="$6" alignItems="center" justifyContent="center">
      {/* Background Gradient Effect (Native compatible) */}
      <YStack position="absolute" top={-100} width={400} height={400} borderRadius={200} backgroundColor="$primary" opacity={0.05} />
      
      <Card 
        width="100%" 
        maxWidth={500} 
        padding="$8" 
        backgroundColor="$bgCard" 
        borderRadius="$10" 
        borderWidth={1} 
        borderColor="$borderColor"
        elevate
      >
        {/* Progress Dots */}
        <XStack gap="$2" marginBottom="$8" justifyContent="center">
          {[1, 2, 3].map(s => (
            <Circle 
              key={s} 
              size={12} 
              backgroundColor={step >= s ? "$primary" : "$gray6"} 
              opacity={step >= s ? 1 : 0.2}
            />
          ))}
        </XStack>

        <AnimatePresence>
          {step === 1 && renderStep1()}
          {step === 2 && renderStep2()}
          {step === 3 && renderStep3()}
        </AnimatePresence>
        
        <YStack marginTop="$10" alignItems="center" gap="$2" opacity={0.3}>
          <XStack alignItems="center" gap="$2">
            <Info size={12} />
            <Text size="$1" fontWeight="900" letterSpacing={1}>COMPLIANCE PACK v1.0</Text>
          </XStack>
        </YStack>
      </Card>
    </YStack>
  );
};
