/**
 * Evida Premium Subscription Component (premium.tsx)
 * --------------------------------------------------
 * 상용화(Commercialization)를 위한 결제 플랜 선택 및 PortOne 연동 스켈레톤 화면입니다.
 * 
 * 유지보수 가이드:
 * - 수익 모델: 월간(9,900원) 및 연간 구독을 제공하여 정밀 혈액 분석, 1:1 집중 AI 코칭 기능을 언락합니다.
 * - 결제 연동: 현재는 스켈레톤(mock) 결제 로직이 구현되어 있으나, 실 배포 전 PortOne SDK의 iamport.js를 
 *   통해 실제 PG사(KCP, Toss 등) 결제창을 띄우도록 수정해야 합니다.
 * - 비즈니스 로직: 결제 성공 시 백엔드 Webhook(`/v1/billing/portone-webhook`)에서 무결성을 검증하고 User DB를 업데이트합니다.
 */
import React, { useState } from 'react';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { YStack, XStack, Text, Heading, Card, ScrollView, Theme, Button, Circle, Spinner } from 'tamagui';
import { ChevronLeft, CheckCircle2, ShieldCheck, Zap, CreditCard } from '@tamagui/lucide-icons';
import axios from 'axios';

const API_BASE = process.env.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000/v1";

export default function PremiumScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const [selectedPlan, setSelectedPlan] = useState<'monthly' | 'onetime'>('monthly');
  const [paymentMethod, setPaymentMethod] = useState<'kakaopay' | 'naverpay' | 'samsungpay' | 'card'>('kakaopay');
  const [loading, setLoading] = useState(false);

  const handlePayment = async () => {
    setLoading(true);
    // PortOne (Iamport) SDK 연동 시뮬레이션
    // 실제 환경에서는 iamport-react-native 모듈을 사용하여 결제창을 호출합니다.
    try {
      const targetUserId = params.user_id || '00000000-0000-0000-0000-000000000000';
      const merchant_uid = `${targetUserId}_premium_${selectedPlan}_${Date.now()}`;
      
      // 모의 결제 성공 후 백엔드 Webhook이 호출되었다고 가정하거나 클라이언트에서 결과 전송
      setTimeout(async () => {
        // 클라이언트에서 서버로 결제 완료를 알림 (Webhook fallback)
        await axios.post(`${API_BASE}/billing/portone-webhook`, {
          imp_uid: `imp_mock_${Date.now()}`,
          merchant_uid,
          status: "paid"
        });
        
        setLoading(false);
        alert('결제가 완료되었습니다! 프리미엄 기능이 활성화되었습니다.');
        router.back();
      }, 1500);
      
    } catch (e) {
      setLoading(false);
      alert('결제 처리 중 오류가 발생했습니다.');
    }
  };

  return (
    <Theme name="dark">
      <ScrollView backgroundColor="$bgDeep" flex={1}>
        <YStack padding="$5" gap="$6" paddingTop="$8" maxWidth={800} alignSelf="center" width="100%">
          
          <XStack alignItems="center" gap="$4">
            <Button size="$3" circular backgroundColor="$gray2" icon={<ChevronLeft size={20} color="white" />} onPress={() => router.back()} />
            <YStack>
              <Text color="white" opacity={0.5} fontSize={14} fontWeight="700" letterSpacing={1}>UPGRADE TO PRO</Text>
              <Heading color="white" fontSize={26} fontWeight="900">Premium Plans ✨</Heading>
            </YStack>
          </XStack>

          {/* 플랜 선택 */}
          <XStack gap="$3">
            <Card 
              flex={1} 
              backgroundColor={selectedPlan === 'monthly' ? "rgba(59, 130, 246, 0.15)" : "$gray1"} 
              borderColor={selectedPlan === 'monthly' ? "#3B82F6" : "$gray3"} 
              borderWidth={2} 
              borderRadius="$6" 
              padding="$4"
              onPress={() => setSelectedPlan('monthly')}
              animation="quick"
              pressStyle={{ scale: 0.98 }}
            >
              <YStack gap="$2" alignItems="center">
                <Zap color={selectedPlan === 'monthly' ? "#3B82F6" : "white"} size={24} opacity={selectedPlan === 'monthly' ? 1 : 0.5} />
                <Text color="white" fontWeight="800" fontSize={16} marginTop="$2">월간 구독</Text>
                <Text color="white" fontWeight="900" fontSize={20}>₩9,900<Text fontSize={12} opacity={0.5}>/월</Text></Text>
                <Text color="white" opacity={0.5} fontSize={11} textAlign="center">1:1 전담 AI 코칭 및 무제한 스캔</Text>
              </YStack>
            </Card>

            <Card 
              flex={1} 
              backgroundColor={selectedPlan === 'onetime' ? "rgba(16, 185, 129, 0.15)" : "$gray1"} 
              borderColor={selectedPlan === 'onetime' ? "#10B981" : "$gray3"} 
              borderWidth={2} 
              borderRadius="$6" 
              padding="$4"
              onPress={() => setSelectedPlan('onetime')}
              animation="quick"
              pressStyle={{ scale: 0.98 }}
            >
              <YStack gap="$2" alignItems="center">
                <CheckCircle2 color={selectedPlan === 'onetime' ? "#10B981" : "white"} size={24} opacity={selectedPlan === 'onetime' ? 1 : 0.5} />
                <Text color="white" fontWeight="800" fontSize={16} marginTop="$2">1회성 분석</Text>
                <Text color="white" fontWeight="900" fontSize={20}>₩4,900</Text>
                <Text color="white" opacity={0.5} fontSize={11} textAlign="center">정밀 혈액 분석 1회 한정</Text>
              </YStack>
            </Card>
          </XStack>

          {/* 결제 수단 선택 (PortOne 지원) */}
          <YStack gap="$3" marginTop="$4">
            <Heading color="white" fontSize={18} fontWeight="800">국내 간편 결제 수단</Heading>
            <YStack gap="$2">
              {[
                { id: 'kakaopay', name: '카카오페이 (KakaoPay)', color: '#FEE500', textColor: '#000000' },
                { id: 'naverpay', name: '네이버페이 (NaverPay)', color: '#03C75A', textColor: '#FFFFFF' },
                { id: 'samsungpay', name: '삼성페이 (SamsungPay)', color: '#1428A0', textColor: '#FFFFFF' },
                { id: 'card', name: '일반 신용/체크카드', color: '#333333', textColor: '#FFFFFF' },
              ].map(method => (
                <Button 
                  key={method.id}
                  backgroundColor={paymentMethod === method.id ? method.color : "$gray2"}
                  color={paymentMethod === method.id ? method.textColor : "white"}
                  opacity={paymentMethod === method.id ? 1 : 0.5}
                  borderWidth={1}
                  borderColor={paymentMethod === method.id ? method.color : "$gray3"}
                  height={55}
                  borderRadius="$5"
                  justifyContent="flex-start"
                  paddingLeft="$5"
                  icon={paymentMethod === method.id ? <CheckCircle2 size={18} color={method.textColor} /> : <CreditCard size={18} />}
                  onPress={() => setPaymentMethod(method.id as any)}
                  fontWeight="800"
                >
                  {method.name}
                </Button>
              ))}
            </YStack>
          </YStack>

          {/* 결제 버튼 */}
          <Button 
            backgroundColor="$brandPrimary" 
            color="white" 
            height={65} 
            borderRadius="$6" 
            marginTop="$4"
            fontWeight="900" 
            fontSize={18}
            iconAfter={loading ? <Spinner color="white" /> : <ShieldCheck size={20} />}
            onPress={handlePayment}
            disabled={loading}
          >
            {loading ? '결제 안전 처리 중...' : '3초 간편 결제 (PortOne)'}
          </Button>

          <Text textAlign="center" color="white" opacity={0.3} fontSize={11} paddingVertical="$2" lineHeight={16}>
            결제는 안전하게 암호화되어 처리됩니다. {'\n'}
            구독은 언제든지 마이페이지에서 위약금 없이 해지하실 수 있습니다.
          </Text>

        </YStack>
      </ScrollView>
    </Theme>
  );
}
