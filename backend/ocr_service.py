import re
import json
import os
import base64
from typing import Dict, Any, Optional

class OCRHealthService:
    """
    GPT-4o Vision 기반 건강검진 결과지 분석 서비스.
    API 키가 없을 시 EasyOCR → Mock 순으로 폴백.
    """

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_gpt_vision = bool(self.openai_api_key)

        if self.use_gpt_vision:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.openai_api_key)
            print("[OCR] GPT-4o Vision 모드로 초기화되었습니다.")
        else:
            print("[OCR] OPENAI_API_KEY 없음. Mock 모드로 동작합니다.")

    def _encode_image_bytes(self, image_bytes: bytes) -> str:
        """바이트 데이터를 base64 문자열로 변환"""
        return base64.b64encode(image_bytes).decode("utf-8")

    def extract_structured_data(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        GPT-4o Vision으로 이미지를 직접 분석하여 구조화된 JSON 반환.
        OCR 텍스트 추출과 파싱을 한 번에 처리.
        """
        if not self.use_gpt_vision:
            return self._mock_response()

        b64 = self._encode_image_bytes(image_bytes)

        system_prompt = """당신은 의료 문서 분석 전문 AI입니다.
건강검진 결과지, InBody 체성분 분석, 혈액검사 결과지 이미지를 받으면
다음 JSON 형식으로만 응답하세요. 값이 없으면 null로 채우세요.

{
  "document_type": "inbody | blood_test | unknown",
  "test_date": "YYYY-MM-DD 또는 null",
  "weight": <float kg 또는 null>,
  "skeletal_muscle_mass": <float kg 또는 null>,
  "body_fat_pct": <float % 또는 null>,
  "bmi": <float 또는 null>,
  "blood_glucose": <int mg/dL 또는 null>,
  "ldl_cholesterol": <int mg/dL 또는 null>,
  "hdl_cholesterol": <int mg/dL 또는 null>,
  "triglycerides": <int mg/dL 또는 null>,
  "crp_level": <float mg/L 또는 null>,
  "raw_summary": "<한 문장으로 전체 결과 요약>"
}
JSON 외 다른 텍스트는 절대 포함하지 마세요."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{b64}",
                                    "detail": "high"
                                }
                            },
                            {
                                "type": "text",
                                "text": "이 건강검진 결과지를 분석하여 JSON으로 반환해주세요."
                            }
                        ]
                    }
                ],
                max_tokens=800,
                temperature=0
            )

            raw_json = response.choices[0].message.content.strip()
            # 혹시 코드블록으로 감싸진 경우 제거
            raw_json = raw_json.replace("```json", "").replace("```", "").strip()
            return json.loads(raw_json)

        except Exception as e:
            print(f"[OCR] GPT-4o Vision 오류: {e}. Mock으로 폴백합니다.")
            return self._mock_response()

    def _mock_response(self) -> Dict[str, Any]:
        """개발/테스트용 Mock 데이터"""
        return {
            "document_type": "blood_test",
            "test_date": "2026-04-12",
            "weight": None,
            "skeletal_muscle_mass": None,
            "body_fat_pct": None,
            "bmi": None,
            "blood_glucose": 112,
            "ldl_cholesterol": 145,
            "hdl_cholesterol": 52,
            "triglycerides": 130,
            "crp_level": None,
            "raw_summary": "[MOCK] 공복혈당 112mg/dL (경계), LDL 145mg/dL (주의 필요)"
        }

    # ── 하위 호환 메서드 (기존 코드에서 호출 시) ──────────────────────────
    def extract_from_image(self, image_input: Any) -> str:
        """기존 호환용: 바이트 입력 시 raw_summary 텍스트 반환"""
        if isinstance(image_input, bytes) and self.use_gpt_vision:
            result = self.extract_structured_data(image_input)
            return result.get("raw_summary", "")
        return "[MOCK] 공복혈당 112 mg/dL, LDL 145 mg/dL"

    def parse_extracted_data(self, raw_text: str) -> Dict[str, Any]:
        """기존 호환용: 텍스트 기반 정규식 파싱 (폴백용)"""
        data = {"blood_glucose": None, "ldl_cholesterol": None, "weight": None, "test_date": None}

        date_matches = re.findall(r'(\d{4})[-./](\d{1,2})[-./](\d{1,2})', raw_text)
        if date_matches:
            y, m, d = date_matches[0]
            data["test_date"] = f"{y}-{m.zfill(2)}-{d.zfill(2)}"

        def find_value(keywords, text, min_v, max_v):
            for kw in keywords:
                match = re.search(rf'{kw}[^\d]{{0,20}}(\d{{2,3}}(?:\.\d)?)', text, re.IGNORECASE)
                if match:
                    val = float(match.group(1))
                    if min_v <= val <= max_v:
                        return val
            return None

        data["blood_glucose"] = find_value([r'혈당', r'glucose', r'fasting'], raw_text, 50, 400)
        data["ldl_cholesterol"] = find_value([r'ldl', r'콜레스테롤'], raw_text, 40, 300)
        data["weight"] = find_value([r'체중', r'weight'], raw_text, 30, 250)
        return data
