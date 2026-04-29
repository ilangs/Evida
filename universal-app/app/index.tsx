import React, { useState } from 'react';
import { useRouter } from 'expo-router';
import { 
  YStack, 
  XStack, 
  Text, 
  Heading, 
  Button, 
  Theme,
  Spinner,
  Input
} from 'tamagui';
import { 
  Hexagon, 
  Activity,
  MessageCircle, 
  Chrome,
  Mail,
  ChevronRight
} from '@tamagui/lucide-icons';

export default function LoginSplash() {
  const router = useRouter();
  const [loadingKakao, setLoadingKakao] = useState(false);
  const [loadingGoogle, setLoadingGoogle] = useState(false);
  const [loadingEmail, setLoadingEmail] = useState(false);
  const [showEmailForm, setShowEmailForm] = useState(false);

  const handleLogin = (provider: 'kakao' | 'google' | 'email') => {
    if (provider === 'kakao') setLoadingKakao(true);
    if (provider === 'google') setLoadingGoogle(true);
    if (provider === 'email') setLoadingEmail(true);
    
    // Simulate OAuth Login process
    setTimeout(() => {
      // Upon successful authentication, forward user to the Onboarding pipeline
      router.replace('/onboarding');
    }, 1500);
  };

  return (
    <Theme name="dark">
      <YStack flex={1} backgroundColor="$bgDeep" alignItems="center" justifyContent="center" padding="$5">
        
        {/* Brand Identity / Splash Area */}
        <YStack alignItems="center" gap="$5" marginBottom="$12" animation="bouncy" enterStyle={{ opacity: 0, scale: 0.9 }}>
          <ZStack alignItems="center" justifyContent="center" width={100} height={100}>
            <Hexagon size={100} color="$brandPrimary" strokeWidth={1} opacity={0.2} />
            <Hexagon size={80} color="$brandPrimary" strokeWidth={2} opacity={0.5} />
            <Activity size={40} color="white" />
          </ZStack>
          
          <YStack alignItems="center" gap="$2">
            <Heading color="white" fontSize={32} fontWeight="900" letterSpacing={2}>VITAL INTELLIGENCE</Heading>
            <Text color="$brandPrimary" fontSize={16} fontWeight="700" letterSpacing={4}>AI HEALTH AGENT</Text>
          </YStack>
          
          <Text textAlign="center" color="white" opacity={0.5} fontSize={14} maxWidth={300} marginTop="$8" marginBottom="$4" lineHeight={22}>
            Your personalized AI companion for peak physical performance and longevity.
          </Text>
        </YStack>

        {/* Social Login Buttons */}
        <YStack gap="$4" width="100%" maxWidth={350} animation="quick" enterStyle={{ opacity: 0, y: 20 }}>
          
          {!showEmailForm ? (
            <>
              {/* Email Option Intro Button */}
              <Button 
                backgroundColor="transparent" 
                borderWidth={1}
                borderColor="rgba(255,255,255,0.4)"
                height={60} 
                borderRadius="$6" 
                icon={() => <Mail size={20} color="white" />}
                onPress={() => setShowEmailForm(true)}
                disabled={loadingKakao || loadingGoogle}
                pressStyle={{ scale: 0.98 }}
              >
                <Text color="white" fontSize={18} fontWeight="800">이메일로 시작하기</Text>
              </Button>

              <XStack alignItems="center" gap="$4" marginVertical="$4">
                <YStack flex={1} height={1} backgroundColor="$gray4" />
                <Text color="white" opacity={0.3} fontSize={12} fontWeight="800">OR</Text>
                <YStack flex={1} height={1} backgroundColor="$gray4" />
              </XStack>

              {/* Kakao Login Button */}
              <Button 
                backgroundColor="#FEE500" 
                height={60} 
                borderRadius="$6" 
                icon={loadingKakao ? () => <Spinner color="black" /> : () => <MessageCircle size={22} color="black" fill="black" />}
                onPress={() => handleLogin('kakao')}
                disabled={loadingKakao || loadingGoogle}
                pressStyle={{ scale: 0.98 }}
              >
                <Text color="black" fontSize={18} fontWeight="900">
                  {loadingKakao ? '로그인 중...' : '카카오로 시작하기'}
                </Text>
              </Button>

              {/* Google Login Button */}
              <Button 
                backgroundColor="white" 
                height={60} 
                borderRadius="$6" 
                icon={loadingGoogle ? () => <Spinner color="black" /> : () => <Chrome size={22} color="black" />}
                onPress={() => handleLogin('google')}
                disabled={loadingKakao || loadingGoogle}
                pressStyle={{ scale: 0.98 }}
              >
                <Text color="black" fontSize={18} fontWeight="900">
                  {loadingGoogle ? '로그인 중...' : '구글로 시작하기'}
                </Text>
              </Button>
            </>
          ) : (
            <YStack gap="$4" animation="quick" enterStyle={{ opacity: 0, scale: 0.95 }}>
              <Input 
                placeholder="이메일 주소" 
                placeholderTextColor="rgba(255,255,255,0.4)" 
                backgroundColor="$gray2" 
                borderColor="$gray4" 
                color="white" 
                height={55} 
                fontSize={16}
                borderRadius="$4"
              />
              <Input 
                placeholder="비밀번호" 
                placeholderTextColor="rgba(255,255,255,0.4)" 
                backgroundColor="$gray2" 
                borderColor="$gray4" 
                color="white" 
                height={55} 
                fontSize={16}
                borderRadius="$4"
                secureTextEntry
              />
              
              <Button 
                backgroundColor="$brandPrimary" 
                height={60} 
                borderRadius="$6" 
                iconAfter={loadingEmail ? undefined : () => <ChevronRight size={20} color="white" />}
                onPress={() => handleLogin('email')}
                disabled={loadingEmail}
                marginTop="$2"
              >
                {loadingEmail ? <Spinner color="white" /> : <Text color="white" fontSize={18} fontWeight="900">로그인</Text>}
              </Button>
              
              <Button 
                backgroundColor="transparent" 
                color="white" 
                opacity={0.5} 
                marginTop="$2" 
                onPress={() => setShowEmailForm(false)}
              >
                <Text color="white" fontSize={14}>이전 뷰로 돌아가기</Text>
              </Button>
            </YStack>
          )}

        </YStack>
        
        <Text position="absolute" bottom={40} color="white" opacity={0.2} fontSize={12} letterSpacing={1}>
          SECURE & ENCRYPTED PLATFORM
        </Text>
        
      </YStack>
    </Theme>
  );
}

// Tamagui ZStack polyfill for stacking elements
const ZStack = ({ children, width, height, ...props }: any) => (
  <YStack width={width} height={height} alignItems="center" justifyContent="center" {...props}>
    {React.Children.map(children, (child) => (
      <YStack position="absolute">
        {child}
      </YStack>
    ))}
  </YStack>
);
