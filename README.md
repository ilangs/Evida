# Evida (Evidence-based Life)

Evida는 사용자의 체성분, 혈액 검사, 라이프스타일 데이터를 종합하여 **초개인화된 목표 달성(감량/증량 등)**을 지원하는 차세대 AI 헬스케어 플랫폼입니다. 의료 가이드라인(RAG)과 AI 에이전트를 활용하여 안전하고 과학적인 건강 관리 솔루션을 제공합니다.

## 🛠️ Tech Stack
*   **Frontend**: Next.js 기반 Expo & Tamagui (크로스 플랫폼 지원: Web, iOS, Android)
*   **Backend**: FastAPI, SQLAlchemy (비동기 처리 구조)
*   **Database**: PostgreSQL (Supabase 연동), Pinecone (의학 가이드라인 벡터 검색)
*   **AI / LLM**: GPT-4o-mini (리포트 생성), LangGraph (대화형 에이전트), GPT-4o Vision (혈액검사지 OCR)
*   **Payment**: PortOne (국내 간편 결제 및 정기 구독 연동)

## ✨ Key Features
1.  **초개인화된 건강 분석 (MBTI/Biometric)**
    *   신체 데이터, MBTI 성향, 기상/취침 시간을 복합적으로 분석한 플랜 제시.
    *   `GPT-4o Vision`을 활용한 혈액검사 결과지 자동 OCR 및 구조화.
2.  **LangGraph 기반 실시간 AI 코칭**
    *   3일 미접속 시 능동적 푸시 알림(Proactive Message).
    *   상태 데이터에 따른 주간 코칭 메시지 및 양방향 채팅 지원.
3.  **상용화 및 결제 인프라 구축**
    *   월 9,900원의 프리미엄 구독 결제 연동(PortOne SDK).
    *   결제 상태에 따른 API Rate Limit 및 프리미엄 기능 활성화 로직.
4.  **시계열 차트 데이터 시각화**
    *   과거 생체 지표와 목표 도달률(Milestone)의 시각화를 통한 리텐션 강화.

## 🚀 Deployment Status
*   **CI/CD**: GitHub Actions를 통한 자동 빌드 및 코드 무결성 검증 파이프라인 구축 완료.
*   **Backend**: Railway / Vercel 배포를 위한 `Dockerfile` 및 `Procfile` 최적화.
*   **Frontend**: Expo Application Services (EAS)를 통한 스토어 배포용 빌드 자동화 (`eas.json`).
*   **보안 방어 로직**: 
    *   만 19세 미만 가입 차단, DB 민감정보 암호화(Encryption at rest), 극단적 감량 목표 차단.

## 💻 Setup Guide (Local Development)

### 1. 환경 변수 설정
`backend` 디렉토리에 `.env` 파일을 생성하고 아래 값을 설정합니다.
```env
DATABASE_URL=postgresql+asyncpg://user:password@host/db
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
JWT_SECRET_KEY=...
PORTONE_API_KEY=...
ENCRYPTION_KEY=...
SENTRY_DSN=...
```
`universal-app` 디렉토리에도 배포용 `.env` 파일을 생성합니다.
```env
EXPO_PUBLIC_API_URL=http://127.0.0.1:8000/v1
```

### 2. Backend 실행
```bash
cd backend
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Frontend 실행
```bash
cd universal-app
npm install --legacy-peer-deps
npx expo start
```
