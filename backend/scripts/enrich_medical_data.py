import os
import asyncio
from langchain_core.documents import Document
from rag_engine import MedicalRAGEngine
from dotenv import load_dotenv

load_dotenv()

async def enrich_knowledge():
    engine = MedicalRAGEngine(api_key=os.getenv("OPENAI_API_KEY"))
    
    additional_papers = [
        {
            "title": "Standards of Care in Diabetes—2024 (ADA)",
            "authors": "American Diabetes Association Professional Practice Committee",
            "journal": "Diabetes Care",
            "pub_year": 2024,
            "content": "공복 혈당(Fasting Plasma Glucose) 126 mg/dL 이상 또는 당화혈색소(HbA1c) 6.5% 이상을 당뇨병으로 진단합니다. 당뇨 전단계(Prediabetes)는 100-125 mg/dL 범위입니다. 비만을 동반한 당뇨 환자의 경우 체중의 5-15% 감량이 혈당 조절에 유의미한 개선을 가져옵니다.",
            "source": "https://diabetesjournals.org/care/article/47/Supplement_1/S1/153950/Standards-of-Care-in-Diabetes-2024"
        },
        {
            "title": "KASBP Guideline for Non-alcoholic Fatty Liver Disease (2023)",
            "authors": "Korean Association for the Study of the Liver",
            "journal": "Clinical and Molecular Hepatology",
            "pub_year": 2023,
            "content": "비알코올 지방간질환(NAFLD) 환자에게 체중의 5% 이상 감량은 간 내 지방량을 감소시키며, 7-10% 이상 감량은 간 섬유화 및 염증 개선을 유도합니다. 허리둘레 기준 남성 90cm, 여성 85cm 이상인 경우 대사 위험이 높으므로 적극적인 생활 습관 교정이 필요합니다.",
            "source": "https://www.kasl.org/guideline/index.php"
        }
    ]

    print("[ENRICH] Preparing professional medical documents...")
    docs_to_upsert = []
    for paper in additional_papers:
        doc = Document(
            page_content=paper["content"],
            metadata={
                "title": paper["title"],
                "author": paper["authors"],
                "journal": paper["journal"],
                "pub_year": paper["pub_year"],
                "source": paper["source"]
            }
        )
        docs_to_upsert.append(doc)

    print(f"[ENRICH] Upserting {len(docs_to_upsert)} documents to Pinecone...")
    engine.upsert_knowledge(docs_to_upsert)
    print("[ENRICH] Knowledge enrichment completed!")

if __name__ == "__main__":
    asyncio.run(enrich_knowledge())
