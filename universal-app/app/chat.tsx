/**
 * Evida Interactive Chat Component (chat.tsx)
 * -------------------------------------------
 * 이 화면은 사용자가 AI 코치와 실시간으로 대화할 수 있는 양방향 커뮤니케이션 인터페이스입니다.
 * 
 * 유지보수 가이드:
 * - 상태 관리: `messages` 배열을 통해 대화 로그를 관리하며, API 응답 대기 중에는 `loading` 상태로 UI 피드백을 제공합니다.
 * - API 통신: 백엔드의 `/v1/coach/chat` 엔드포인트(LangGraph 연동)와 통신합니다.
 * - 디자인 시스템: Tamagui 기반의 다크 모드/글래스모피즘 UI를 적용하여 모바일 환경에 최적화된 UX를 제공합니다.
 */
import React, { useState, useRef } from 'react';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { YStack, XStack, Text, Heading, Button, Input, ScrollView, Theme, Card, Circle, Spinner } from 'tamagui';
import { ChevronLeft, Send, User, Bot, Sparkles } from '@tamagui/lucide-icons';
import axios from 'axios';

const API_BASE = process.env.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000/v1";

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: '안녕하세요! 당신의 전담 AI 건강 코치입니다. 오늘 어떤 도움이 필요하신가요?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const scrollViewRef = useRef<any>(null);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      const targetUserId = params.user_id || '00000000-0000-0000-0000-000000000000';
      const res = await axios.post(`${API_BASE}/coach/chat`, {
        user_id: targetUserId,
        message: userMsg
      });
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'assistant', content: '죄송합니다. 통신에 문제가 발생했습니다. 다시 시도해주세요.' }]);
    } finally {
      setLoading(false);
      setTimeout(() => scrollViewRef.current?.scrollToEnd({ animated: true }), 100);
    }
  };

  return (
    <Theme name="dark">
      <YStack backgroundColor="$bgDeep" flex={1} padding="$5" paddingTop="$8">
        <XStack alignItems="center" gap="$4" marginBottom="$4">
          <Button size="$3" circular backgroundColor="$gray2" icon={<ChevronLeft size={20} color="white" />} onPress={() => router.back()} />
          <YStack>
            <Text color="white" opacity={0.5} fontSize={14} fontWeight="700" letterSpacing={1}>REAL-TIME ASSISTANT</Text>
            <Heading color="white" fontSize={24} fontWeight="900">AI Coach Chat <Sparkles size={20} color="#FBBF24" /></Heading>
          </YStack>
        </XStack>

        <Card flex={1} backgroundColor="$gray1" borderRadius="$6" borderWidth={1} borderColor="$gray3" padding="$4" elevation={10}>
          <ScrollView ref={scrollViewRef} flex={1} showsVerticalScrollIndicator={false}>
            <YStack gap="$4" paddingBottom="$4">
              {messages.map((msg, i) => (
                <XStack key={i} justifyContent={msg.role === 'user' ? 'flex-end' : 'flex-start'} gap="$3">
                  {msg.role === 'assistant' && (
                    <Circle size={40} backgroundColor="rgba(59, 130, 246, 0.2)">
                      <Bot color="#3B82F6" size={20} />
                    </Circle>
                  )}
                  <YStack 
                    maxWidth="75%" 
                    backgroundColor={msg.role === 'user' ? '$brandPrimary' : '$gray2'} 
                    padding="$3" 
                    borderRadius="$5"
                    borderTopRightRadius={msg.role === 'user' ? 0 : '$5'}
                    borderTopLeftRadius={msg.role === 'assistant' ? 0 : '$5'}
                  >
                    <Text color="white" fontSize={15} lineHeight={22}>{msg.content}</Text>
                  </YStack>
                  {msg.role === 'user' && (
                    <Circle size={40} backgroundColor="$gray3">
                      <User color="white" opacity={0.5} size={20} />
                    </Circle>
                  )}
                </XStack>
              ))}
              {loading && (
                <XStack justifyContent="flex-start" gap="$3">
                  <Circle size={40} backgroundColor="rgba(59, 130, 246, 0.2)">
                    <Bot color="#3B82F6" size={20} />
                  </Circle>
                  <YStack backgroundColor="$gray2" padding="$3" borderRadius="$5" borderTopLeftRadius={0}>
                     <Spinner size="small" color="#3B82F6" />
                  </YStack>
                </XStack>
              )}
            </YStack>
          </ScrollView>

          <XStack marginTop="$4" gap="$3" alignItems="center">
            <Input 
              flex={1} 
              height={50} 
              placeholder="코치에게 질문하세요..." 
              value={input} 
              onChangeText={setInput} 
              backgroundColor="$gray2" 
              color="white" 
              borderColor="$gray3" 
              borderRadius="$5"
              onSubmitEditing={sendMessage}
            />
            <Button 
              width={50} 
              height={50} 
              backgroundColor="$brandPrimary" 
              color="white" 
              icon={<Send size={20} />} 
              onPress={sendMessage} 
              disabled={loading || !input.trim()}
              borderRadius="$5"
            />
          </XStack>
        </Card>
      </YStack>
    </Theme>
  );
}
