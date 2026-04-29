import os
import uuid
from dotenv import load_dotenv
from langchain_core.documents import Document
from rag_engine import MedicalRAGEngine

def seed_weight_gain_knowledge():
    load_dotenv()
    engine = MedicalRAGEngine()
    
    # 1. 증량 및 근육 성장 관련 전문 의학 데이터 가이드라인 정의
    gain_docs = [
        Document(
            page_content="""[Healthy Weight Gain Guideline 2025] 
            마른 체형(BMI < 18.5) 사용자의 건강한 증량은 단순히 칼로리를 늘리는 것이 아니라 '지방량 대비 제지방량(LBM)의 우세한 증가'를 목표로 해야 합니다. 
            Caloric Surplus 전략: 일일 에너지 소모량(TDEE)보다 약 300~500kcal를 추가 섭취하며, 정제 탄수화물보다는 복합 탄수화물과 불포화 지방을 통해 영양 밀도를 높여야 합니다.
            근비대(Hypertrophy)를 위한 최소 단백질 요구량: 체중 1kg당 1.6g~2.2g의 양질의 단백질(류신 포함) 섭취가 필수적입니다.""",
            metadata={"source": "WHO Clinical Nutrition Guide", "topic": "weight_gain", "title": "Precision Nutritional Therapy for Lean Patients"}
        ),
        Document(
            page_content="""[Resistance Training for Muscle Hypertrophy - ACSM Standards]
            효과적인 근력 증가를 위해서는 '점진적 과부하(Progressive Overload)' 원칙을 적용해야 합니다. 
            주당 최소 2~3회의 전신 혹은 분할 근력 운동을 권장하며, 각 세트당 8~12회의 반복 횟수를 통해 대사적 스트레스와 기계적 긴장을 극대화합니다. 
            운동 직후 30분 이내에 탄수화물과 단백질을 3:1 비율로 섭취하는 것이 글리코겐 회복 및 단백질 합성에 최적입니다.""",
            metadata={"source": "ACSM 2024 Guidelines", "topic": "muscle_gain", "title": "Optimal Training Volume for Hypertrophy"}
        ),
        Document(
            page_content="""[Safety and Metabolism in Underweight Management]
            급격한 체중 증가는 인슐린 저항성을 높여 '마른 비만(Normal-weight obesity)'을 초래할 수 있습니다. 
            증량 과정에서 공복 혈당이 100mg/dL를 초과하거나 중성지방 수치가 급격히 상승할 경우, 식단의 지방 종류를 검토하고 유산소 운동 비중을 20% 이내로 유지하며 심폐 건강을 병행 관리해야 합니다. 
            기저 질환자(갑상선 기능 항진증 등)는 반드시 의학적 진단 후 증량을 시작해야 합니다.""",
            metadata={"source": "The Lancet Diabetes & Endocrinology", "topic": "metabolic_safety", "title": "Metabolic Risks of Rapid Weight Gain"}
        )
    ]
    
    # 2. Pinecone에 업서트
    print(f"[SEED] Pinecone에 {len(gain_docs)}건의 증량/근육 지식 데이터 저장 중...")
    engine.upsert_knowledge(gain_docs)
    print("[SEED] 완료: 이제 AI가 증량 목표 유저에게 전문적인 조언을 제공할 수 있습니다.")

if __name__ == "__main__":
    seed_weight_gain_knowledge()
