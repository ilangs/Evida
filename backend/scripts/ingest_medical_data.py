import os
from langchain_core.documents import Document
from rag_engine import MedicalRAGEngine
from dotenv import load_dotenv

load_dotenv()

def ingest_medical_guidelines():
    """
    최신 글로벌 의학 가이드라인(2025 고혈압, 2018 콜레스테롤, 2025 WHO 비만)을 
    Pinecone에 저장합니다.
    """
    engine = MedicalRAGEngine()
    
    # 1. 고혈압 가이드라인 (AHA/ACC 2025)
    hypertension_data = [
        Document(
            page_content="AHA/ACC 2025 Hypertension Treatment Goals: The recommended blood pressure (BP) goal for most adults is <130/80 mmHg. An optimal goal close to 120/80 mmHg is encouraged. For adults with stage 2 hypertension (BP >=140/90 mmHg), initiating treatment with two medications is recommended.",
            metadata={"source": "AHA/ACC 2025", "topic": "Hypertension", "category": "Treatment Goals"}
        ),
        Document(
            page_content="Diagnosis and Risk Assessment (AHA/ACC 2025): The PREVENT risk calculator has replaced the PCE for CVD risk estimation. Risk-enhancing factors include renal function and statin use. Medication is recommended if BP >=130/80 and 10-year CVD risk >=7.5%.",
            metadata={"source": "AHA/ACC 2025", "topic": "Hypertension", "category": "Diagnosis"}
        ),
        Document(
            page_content="Lifestyle Management for Hypertension: Foundations include DASH diet, sodium reduction (<1,500 mg/day), weight loss (target >=5% of initial weight), and potassium-based salt substitutes unless contraindicated by CKD.",
            metadata={"source": "AHA/ACC 2025", "topic": "Hypertension", "category": "Lifestyle"}
        )
    ]

    # 2. 콜레스테롤 가이드라인 (AHA/ACC 2018)
    cholesterol_data = [
        Document(
            page_content="Secondary Prevention for ASCVD (AHA/ACC 2018): High-intensity or maximally tolerated statin therapy is recommended to lower LDL-C by 50% or more. If LDL-C remains >=70 mg/dL, adding ezetimibe is reasonable.",
            metadata={"source": "AHA/ACC 2018", "topic": "Cholesterol", "category": "Secondary Prevention"}
        ),
        Document(
            page_content="Primary Prevention (AHA/ACC 2018): For adults 40-75 years old without diabetes, calculate 10-year ASCVD risk. If intermediate risk (7.5%-19.9%), consider risk-enhancing factors and possibly CAC score of 0 to delay statins.",
            metadata={"source": "AHA/ACC 2018", "topic": "Cholesterol", "category": "Primary Prevention"}
        )
    ]

    # 3. 비만 치료 가이드라인 (WHO 2025)
    obesity_data = [
        Document(
            page_content="WHO 2025 Obesity Pharmacotherapy: Conditional recommendations for long-term use of GLP-1 receptor agonists (Liraglutide, Semaglutide, Tirzepatide) for adults with BMI >=30, as part of comprehensive care including lifestyle support.",
            metadata={"source": "WHO 2025", "topic": "Obesity", "category": "Medication"}
        ),
        Document(
            page_content="Comprehensive Care for Obesity (WHO 2025): Obesity is a chronic, relapsing disease. Effective management requires weight loss, physical activity, and healthy diet integrated into standard chronic care systems.",
            metadata={"source": "WHO 2025", "topic": "Obesity", "category": "Lifestyle"}
        )
    ]

    # 전체 데이터 합치기
    all_documents = hypertension_data + cholesterol_data + obesity_data
    
    print(f"[INGEST] 총 {len(all_documents)}건의 전문 지식 데이터를 업로드합니다...")
    engine.upsert_knowledge(all_documents)
    print("[INGEST] 업로드 완료!")

if __name__ == "__main__":
    ingest_medical_guidelines()
