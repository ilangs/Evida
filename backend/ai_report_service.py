import os
import json
from typing import Dict, Any, Optional, List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class AIReportService:
    """
    체성분 + 혈액 + MBTI + 생활패턴을 통합하여
    GPT-4o-mini 기반 초개인화 건강 분석 리포트를 생성하는 서비스.

    [모델 전략]
    - OCR (이미지 분석) : gpt-4o        (Vision 기능 필수, ocr_service.py)
    - 리포트 생성 (RAG) : gpt-4o-mini   (토큰 비용 약 15배 절감)
    """

    # ── 모델 상수 ─────────────────────────────────────────────────────
    REPORT_MODEL = "gpt-4o-mini"   # RAG 통합 리포트 (저비용)
    REPORT_MAX_TOKENS = 2500       # mini는 출력 속도가 빠르므로 여유 확보""

    RISK_THRESHOLDS = {
        "blood_glucose":     {"normal": (70, 99),  "warning": (100, 125), "danger": (126, 999)},
        "ldl_cholesterol":   {"normal": (0, 99),   "warning": (100, 129), "danger": (130, 999)},
        "hdl_cholesterol":   {"normal": (60, 999), "warning": (40, 59),   "danger": (0, 39)},  # 높을수록 좋음
        "triglycerides":     {"normal": (0, 149),  "warning": (150, 199), "danger": (200, 999)},
        "body_fat_pct_male": {"normal": (10, 20),  "warning": (21, 25),   "danger": (26, 100)},
        "body_fat_pct_fem":  {"normal": (18, 28),  "warning": (29, 33),   "danger": (34, 100)},
    }

    MBTI_EXERCISE_STYLE = {
        "E": "그룹 PT, 러닝 크루, 팀 스포츠처럼 타인과 에너지를 나누는 운동",
        "I": "홈트레이닝, 필라테스, 수영처럼 혼자 집중할 수 있는 운동",
        "S": "정해진 루틴과 단계적 프로그램이 명확한 스트렝스 트레이닝",
        "N": "다양한 자극과 변화가 있는 크로스핏, HIIT, 클라이밍",
        "T": "심박수·칼로리 데이터 기반으로 효율을 극대화하는 과학적 훈련",
        "F": "몸과 마음의 균형을 위한 요가, 필라테스, 댄스",
        "J": "주간 스케줄로 체계적으로 계획된 운동 루틴",
        "P": "즉흥적으로 선택 가능한 다양한 운동 옵션과 유연한 스케줄",
    }

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
            print(f"[AI Report] {self.REPORT_MODEL} 연결 완료 (리포트 생성)")
        else:
            self.client = None
            print("[AI Report] API 키 없음. Mock 모드로 동작")

    # ──────────────────────────────────────────────────────
    # 1. 위험 지표 분석
    # ──────────────────────────────────────────────────────
    def analyze_risk_flags(self, biometric: Dict[str, Any], gender: str = "M") -> List[Dict]:
        """수치별 위험도 플래그를 계산하여 반환"""
        flags = []

        checks = {
            "혈당 (Blood Glucose)": ("blood_glucose", self.RISK_THRESHOLDS["blood_glucose"], "mg/dL", "정상: 70-99"),
            "LDL 콜레스테롤": ("ldl_cholesterol", self.RISK_THRESHOLDS["ldl_cholesterol"], "mg/dL", "정상: <100"),
            "HDL 콜레스테롤": ("hdl_cholesterol", self.RISK_THRESHOLDS["hdl_cholesterol"], "mg/dL", "정상: ≥60"),
            "중성지방": ("triglycerides", self.RISK_THRESHOLDS["triglycerides"], "mg/dL", "정상: <150"),
        }

        fat_key = "body_fat_pct_male" if gender in ("M", "male", "남성") else "body_fat_pct_fem"
        if biometric.get("body_fat_pct"):
            fat_val = float(biometric["body_fat_pct"])
            thresholds = self.RISK_THRESHOLDS[fat_key]
            label = "체지방률"
            if fat_val >= thresholds["danger"][0]:
                flags.append({"label": label, "value": fat_val, "unit": "%", "level": "danger",
                               "message": "체지방이 과다합니다. 적극적인 식단·운동 관리가 필요합니다."})
            elif fat_val >= thresholds["warning"][0]:
                flags.append({"label": label, "value": fat_val, "unit": "%", "level": "warning",
                               "message": "체지방이 다소 높습니다. 유산소 운동 비중을 늘려보세요."})

        for label, (key, thresholds, unit, normal_range) in checks.items():
            val = biometric.get(key)
            if val is None:
                continue
            val = float(val)
            # HDL은 반대 (낮을수록 위험)
            if key == "hdl_cholesterol":
                if val <= thresholds["danger"][1]:
                    flags.append({"label": label, "value": val, "unit": unit, "level": "danger",
                                   "message": f"HDL이 매우 낮습니다. 유산소 운동과 건강지방(생선·견과류) 섭취를 늘리세요."})
                elif val <= thresholds["warning"][1]:
                    flags.append({"label": label, "value": val, "unit": unit, "level": "warning",
                                   "message": "HDL이 다소 낮습니다. 규칙적인 유산소 운동을 권장합니다."})
            else:
                if val >= thresholds["danger"][0]:
                    flags.append({"label": label, "value": val, "unit": unit, "level": "danger",
                                   "message": f"{label}({val}{unit})이 위험 수준입니다. {normal_range}"})
                elif val >= thresholds["warning"][0]:
                    flags.append({"label": label, "value": val, "unit": unit, "level": "warning",
                                   "message": f"{label}({val}{unit})이 주의 구간입니다. {normal_range}"})

        return flags

    # ──────────────────────────────────────────────────────
    # 2. 핵심: GPT-4o 통합 리포트 생성
    # ──────────────────────────────────────────────────────
    def generate_report(
        self,
        user: Dict[str, Any],
        biometric: Dict[str, Any],
        rag_evidence: str = "",
        rag_engine=None,  # MedicalRAGEngine 인스섴
    ) -> Dict[str, Any]:
        """
        사용자 프로필 + 생체지표 + RAG 근거를 gpt-4o-mini에 전달하여
        구조화된 JSON 리포트 생성. (OCR은 별도로 gpt-4o Vision 사용)
        """
        risk_flags = self.analyze_risk_flags(biometric, user.get("gender", "M"))

        # 누락된 혈액 검사 수치 확인 및 사용자 피드백 안내 로직 고도화
        missing_fields = []
        if biometric.get("blood_glucose") is None: missing_fields.append("공복혈당")
        if biometric.get("ldl_cholesterol") is None: missing_fields.append("LDL 콜레스테롤")
        if biometric.get("hdl_cholesterol") is None: missing_fields.append("HDL 콜레스테롤")

        if missing_fields:
            missing_text = f"현재 혈액 검사 데이터 중 [{', '.join(missing_fields)}] 항목이 누락되어 있습니다. 더 정확한 맞춤형 AI 리포트와 위험도 분석을 위해 다음 검사 시 해당 수치를 꼭 입력해주세요."
        else:
            missing_text = ""

        # 위험 지표 플래그 코드 추출 (RAG 검색용)
        flag_codes = []
        for f in risk_flags:
            if "혈당" in f["label"] or "glucose" in f["label"].lower():
                flag_codes.append("high_glucose")
            if "LDL" in f["label"]:
                flag_codes.append("high_ldl")
            if "체지방" in f["label"]:
                flag_codes.append("high_body_fat")
            if "HDL" in f["label"]:
                flag_codes.append("low_hdl")

        # RAG 엔진이 전달된 경우 목표 기반 복합 검색 실행
        rag_citations = []
        if rag_engine and not rag_evidence:
            rag_result = rag_engine.search_by_goal(user.get("goal_type", "maintenance"), flag_codes)
            rag_evidence = rag_result["combined_text"]
            rag_citations = rag_result.get("citations", [])

        # MBTI 운동 스타일 조합
        mbti = user.get("mbti", "")
        exercise_styles = []
        for ch in mbti:
            if ch.upper() in self.MBTI_EXERCISE_STYLE:
                exercise_styles.append(self.MBTI_EXERCISE_STYLE[ch.upper()])
        mbti_style = " / ".join(exercise_styles[:2]) if exercise_styles else "균형 잡힌 운동"

        # MBTI 기반 코칭 톤앤매너 최적화 (Phase 2)
        tone_instruction = "친절하고 전문적인 어조로 답변하세요."
        if "T" in mbti.upper():
            tone_instruction = "논리적이고 데이터(수치) 중심의 근거를 제시하며, 객관적이고 명확한 어조로 분석 결과를 전달하세요. 불필요한 감정적 표현은 피하세요."
        elif "F" in mbti.upper():
            tone_instruction = "공감과 따뜻한 격려를 중심으로, 작은 성취도 칭찬하며 감성적이고 부드러운 어조로 전달하세요. 이모지를 활용해도 좋습니다."

        # 위험 지표 요약 텍스트
        risk_summary = "\n".join([
            f"- [{f['level'].upper()}] {f['label']}: {f['value']}{f['unit']} → {f['message']}"
            for f in risk_flags
        ]) or "주요 위험 지표 없음"

        system_prompt = f"""당신은 Vital Intelligence의 개인 건강 AI 코치입니다.
의학적 근거와 사용자 데이터를 바탕으로 초개인화된 건강 분석 리포트를 작성합니다.
[대화 톤앤매너 지침]: {tone_instruction}

반드시 아래 JSON 형식으로만 응답하세요. 불필요한 설명은 생략합니다.

{
  "summary": "<3문장 이내 핵심 건강 상태 요약>",
  "priority_message": "<오늘 당장 가장 중요한 한 가지 행동 권고>",
  "missing_data_feedback": "<누락된 데이터가 있을 경우 안내, 없으면 null>",
  "weekly_workout": [
    {"day": "MON", "title": "<운동명>", "detail": "<세트/시간 등 상세>", "duration_min": <int>},
    {"day": "TUE", "title": "<운동명>", "detail": "<세트/시간 등 상세>", "duration_min": <int>},
    {"day": "WED", "title": "<운동명>", "detail": "<세트/시간 등 상세>", "duration_min": <int>},
    {"day": "THU", "title": "<운동명>", "detail": "<세트/시간 등 상세>", "duration_min": <int>},
    {"day": "FRI", "title": "<운동명>", "detail": "<세트/시간 등 상세>", "duration_min": <int>},
    {"day": "SAT", "title": "Active Recovery", "detail": "스트레칭 + 산책", "duration_min": 30},
    {"day": "SUN", "title": "Rest", "detail": "완전 휴식 또는 명상", "duration_min": 0}
  ],
  "daily_meals": {
    "breakfast": {"menu": "<메뉴>", "calories": <int>, "protein_g": <int>, "carb_g": <int>, "fat_g": <int>},
    "lunch":     {"menu": "<메뉴>", "calories": <int>, "protein_g": <int>, "carb_g": <int>, "fat_g": <int>},
    "dinner":    {"menu": "<메뉴>", "calories": <int>, "protein_g": <int>, "carb_g": <int>, "fat_g": <int>},
    "snack":     {"menu": "<메뉴>", "calories": <int>, "protein_g": <int>, "carb_g": <int>, "fat_g": <int>}
  },
  "medical_evidence": "<RAG 근거 논문 한 줄 인용 또는 표준 가이드라인 출처>",
  "disclaimer": "※ 본 서비스는 의학적 진단이나 치료를 대신할 수 없으며, 질환이 있는 경우 반드시 전문의와 상의하십시오."
}"""

        user_prompt = f"""
[사용자 프로필]
- 이름: {user.get('name', '사용자')}
- 나이/성별: {user.get('age', '?')}세 / {user.get('gender', '?')}
- MBTI: {mbti} → 권장 운동 스타일: {mbti_style}
- 목표: {user.get('goal_type', '')} ({user.get('goal_description', '')})
- 시작/목표 체중: {user.get('start_weight', '?')}kg → {user.get('target_weight', '?')}kg

[최신 생체지표]
- 체중: {biometric.get('weight', 'N/A')} kg
- 골격근량: {biometric.get('skeletal_muscle_mass', 'N/A')} kg
- 체지방률: {biometric.get('body_fat_pct', 'N/A')} %
- 공복혈당: {biometric.get('blood_glucose', 'N/A')} mg/dL
- LDL 콜레스테롤: {biometric.get('ldl_cholesterol', 'N/A')} mg/dL
- HDL 콜레스테롤: {biometric.get('hdl_cholesterol', 'N/A')} mg/dL
- 중성지방: {biometric.get('triglycerides', 'N/A')} mg/dL

[위험 지표 분석]
{risk_summary}

[누락된 데이터 확인]
{missing_text}

[의학적 근거 (RAG)]
{rag_evidence or "표준 건강 관리 가이드라인 적용"}

위 데이터를 종합하여 JSON 리포트를 생성해주세요.
"""

        if not self.client:
            return self._mock_report(user, risk_flags)

        try:
            response = self.client.chat.completions.create(
                model=self.REPORT_MODEL,        # gpt-4o-mini
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.REPORT_MAX_TOKENS,
                temperature=0.4,
                response_format={"type": "json_object"}
            )
            raw = response.choices[0].message.content.strip()
            report = json.loads(raw)
            report["risk_flags"]  = risk_flags
            report["citations"]   = rag_citations         # 인용 논문 목록
            report["model_used"]  = self.REPORT_MODEL
            return report
        except Exception as e:
            print(f"[AI Report] {self.REPORT_MODEL} 오류: {e}")
            mock = self._mock_report(user, risk_flags)
            mock["citations"] = rag_citations
            return mock

    # ──────────────────────────────────────────────────────
    # 3. Mock 리포트 (API 키 없을 때)
    # ──────────────────────────────────────────────────────
    def _mock_report(self, user: Dict, risk_flags: List) -> Dict:
        name = user.get("name", "사용자")
        return {
            "summary": f"{name}님은 현재 목표 달성 초기 단계입니다. 혈당과 LDL 수치가 경계선에 있어 식단 관리가 우선입니다. 규칙적인 운동 루틴을 시작하면 4주 내 가시적인 변화를 기대할 수 있습니다.",
            "priority_message": "오늘 저녁 식사에서 정제 탄수화물(흰쌀, 밀가루)을 현미·통밀로 교체하세요.",
            "missing_data_feedback": "현재 일부 혈액 검사 수치가 누락되어 있습니다. 다음 검사 시 꼭 추가해주세요.",
            "weekly_workout": [
                {"day": "MON", "title": "Lower Body Strength", "detail": "스쿼트 4×12 / 런지 3×15 / 레그프레스 3×12", "duration_min": 50},
                {"day": "TUE", "title": "Cardio HIIT", "detail": "20초 전력질주 / 40초 휴식 × 10라운드", "duration_min": 30},
                {"day": "WED", "title": "Upper Body Push", "detail": "벤치프레스 4×10 / 숄더프레스 3×12 / 트라이셉 딥스 3×15", "duration_min": 50},
                {"day": "THU", "title": "Low-Intensity Cardio", "detail": "빠른 걷기 또는 사이클링 (심박수 120-130)", "duration_min": 40},
                {"day": "FRI", "title": "Upper Body Pull", "detail": "풀업 4×8 / 바벨로우 4×10 / 페이스풀 3×15", "duration_min": 50},
                {"day": "SAT", "title": "Active Recovery", "detail": "전신 스트레칭 15분 + 30분 산책", "duration_min": 45},
                {"day": "SUN", "title": "Rest", "detail": "완전 휴식 또는 10분 명상", "duration_min": 0},
            ],
            "daily_meals": {
                "breakfast": {"menu": "오트밀 + 블루베리 + 단백질 파우더", "calories": 380, "protein_g": 28, "carb_g": 45, "fat_g": 8},
                "lunch":     {"menu": "닭가슴살 현미밥 + 삶은 브로콜리", "calories": 520, "protein_g": 45, "carb_g": 55, "fat_g": 10},
                "dinner":    {"menu": "연어구이 + 퀴노아 + 아보카도 샐러드", "calories": 580, "protein_g": 38, "carb_g": 40, "fat_g": 22},
                "snack":     {"menu": "견과류 한 줌 + 플레인 그릭요거트", "calories": 220, "protein_g": 12, "carb_g": 15, "fat_g": 12},
            },
            "medical_evidence": "WHO 2024 비만 관리 가이드라인: 체중의 5-10% 감량 시 대사 지표가 유의미하게 개선됩니다.",
            "risk_flags": risk_flags,
            "disclaimer": "※ 본 서비스는 의학적 진단이나 치료를 대신할 수 없으며, 질환이 있는 경우 반드시 전문의와 상의하십시오."
        }
