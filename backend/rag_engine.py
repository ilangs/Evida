"""
Vital Intelligence RAG Engine v2
==================================
- Primary  : ChromaDB  (로컬 영구 저장, 오프라인 가능)
- Fallback : Pinecone  (클라우드 백업, 선택적)
- Embedding: OpenAI text-embedding-3-small (비용 효율 최적)
- 검색 전략: 하이브리드 (의미론적 유사도 + 목표/카테고리 메타필터)
"""
import os
from typing import List, Dict, Any, Optional
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# ── 임베딩 설정 ─────────────────────────────────────────────────────
def _build_embeddings():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model="text-embedding-3-small",   # 비용 효율적 최신 모델
            openai_api_key=api_key
        )
    # API 키 없을 때 Mock
    from langchain_core.embeddings import FakeEmbeddings
    return FakeEmbeddings(size=1536)


class MedicalRAGEngine:
    """
    ChromaDB 로컬 우선 + Pinecone 클라우드 폴백 방식의 의학 지식 검색 엔진.
    """

    CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
    CHROMA_COLLECTION  = "medical_knowledge_v1"

    def __init__(self, api_key: Optional[str] = None):
        self.openai_api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.embeddings = _build_embeddings()

        # ChromaDB (로컬 벡터 DB) 초기화
        self._init_chroma()

        # Pinecone (클라우드 백업) 선택적 초기화
        self.pinecone_store = None
        if os.getenv("PINECONE_API_KEY"):
            self._init_pinecone()

    # ── ChromaDB 초기화 ──────────────────────────────────────────────
    def _init_chroma(self):
        try:
            from langchain_chroma import Chroma
            self.chroma_store = Chroma(
                collection_name=self.CHROMA_COLLECTION,
                embedding_function=self.embeddings,
                persist_directory=self.CHROMA_PERSIST_DIR,
            )
            count = self.chroma_store._collection.count()
            print(f"[RAG] ChromaDB 로드 완료 — {count}건의 의학 문서 준비됨")
        except Exception as e:
            print(f"[RAG] ChromaDB 초기화 실패: {e}")
            self.chroma_store = None

    # ── Pinecone 초기화 (선택적 클라우드 백업) ─────────────────────────
    def _init_pinecone(self):
        try:
            from pinecone import Pinecone, ServerlessSpec
            from langchain_pinecone import PineconeVectorStore

            pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            index_name = os.getenv("PINECONE_INDEX_NAME", "healthcare-index")

            if index_name not in pc.list_indexes().names():
                pc.create_index(
                    name=index_name,
                    dimension=1536,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )

            self.pinecone_store = PineconeVectorStore(
                index_name=index_name,
                embedding=self.embeddings,
                pinecone_api_key=os.getenv("PINECONE_API_KEY")
            )
            print("[RAG] Pinecone 클라우드 백업 연결 완료")
        except Exception as e:
            print(f"[RAG] Pinecone 연결 실패 (무시됨): {e}")
            self.pinecone_store = None

    # ── 핵심: 의학 근거 검색 ─────────────────────────────────────────
    def search_evidence(
        self,
        query: str,
        k: int = 3,
        category_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        ChromaDB에서 관련 의학 논문 검색.
        category_filter: 'weight_loss' | 'blood_glucose' | 'cholesterol' |
                         'muscle' | 'exercise' | 'korean_guideline' | 'lifestyle'
        """
        fallback = [{
            "content": "균형 잡힌 식단과 규칙적인 신체 활동은 모든 건강 목표의 기초입니다. "
                       "WHO 2024 가이드라인에 따르면 주 150분 이상의 중강도 유산소 운동과 "
                       "주 2회 이상의 근력 운동이 권장됩니다.",
            "metadata": {"source": "WHO Physical Activity Guidelines 2024", "category": "general"}
        }]

        # 1. ChromaDB 검색
        if self.chroma_store:
            try:
                search_kwargs = {"k": k}
                if category_filter:
                    search_kwargs["filter"] = {"category": {"$eq": category_filter}}

                docs = self.chroma_store.similarity_search(query, **search_kwargs)
                if docs:
                    return [{"content": d.page_content, "metadata": d.metadata} for d in docs]
            except Exception as e:
                print(f"[RAG] ChromaDB 검색 오류: {e}")

        # 2. Pinecone 폴백
        if self.pinecone_store:
            try:
                docs = self.pinecone_store.similarity_search(query, k=k)
                if docs:
                    return [{"content": d.page_content, "metadata": d.metadata} for d in docs]
            except Exception as e:
                print(f"[RAG] Pinecone 검색 오류: {e}")

        return fallback

    # ── 목표 유형별 최적화 검색 ─────────────────────────────────────
    def search_by_goal(self, goal_type: str, biometric_flags: List[str]) -> Dict[str, Any]:
        """
        목표 + 위험 지표를 함께 고려한 복합 검색.
        biometric_flags: ['high_glucose', 'high_ldl', 'high_body_fat'] 등
        반환값에 citations 리스트(전체 메타데이터) 포함.
        """
        # 가장 긴급한 위험 지표 우선 검색
        if "high_glucose" in biometric_flags:
            results = self.search_evidence(
                "blood glucose control prediabetes lifestyle intervention diet",
                k=2, category_filter="blood_glucose"
            )
        elif "high_ldl" in biometric_flags:
            results = self.search_evidence(
                "LDL cholesterol dietary management cardiovascular risk",
                k=2, category_filter="cholesterol"
            )
        elif "high_body_fat" in biometric_flags:
            results = self.search_evidence(
                "obesity body fat reduction calorie deficit exercise",
                k=2, category_filter="weight_loss"
            )
        elif goal_type == "weight_loss":
            results = self.search_evidence(
                "calorie deficit weight loss sustainable diet adherence",
                k=2, category_filter="weight_loss"
            )
        elif goal_type == "weight_gain":
            results = self.search_evidence(
                "muscle hypertrophy progressive overload protein synthesis",
                k=2, category_filter="muscle"
            )
        else:
            results = self.search_evidence(
                "metabolic health maintenance balanced nutrition lifestyle",
                k=2
            )

        # 운동 근거 항상 추가
        exercise_result = self.search_evidence(
            "exercise prescription optimal frequency intensity health outcomes",
            k=1, category_filter="exercise"
        )

        all_results = results + exercise_result

        # 인용용 정제된 메타데이터 리스트 (중복 제거)
        seen_ids = set()
        citations = []
        for r in all_results:
            meta = r.get("metadata", {})
            paper_id = meta.get("id") or meta.get("doi") or meta.get("title", "")[:40]
            if paper_id and paper_id not in seen_ids:
                seen_ids.add(paper_id)
                citations.append({
                    "id":       meta.get("id", ""),
                    "title":    meta.get("title", "Unknown Title"),
                    "authors":  meta.get("authors", ""),
                    "journal":  meta.get("journal", ""),
                    "pub_year": meta.get("pub_year", ""),
                    "doi":      meta.get("doi", ""),
                    "source":   meta.get("source", ""),
                    "category": meta.get("category", "general"),
                    "excerpt":  r["content"][:200] + "…",  # 요약 발췌
                })

        return {
            "primary":      results,
            "exercise":     exercise_result,
            "citations":    citations,                   # ← 전체 인용 목록 (NEW)
            "combined_text": "\n".join([r["content"][:300] for r in all_results])
        }

    # ── 문서 저장 ────────────────────────────────────────────────────
    def upsert_knowledge(self, documents: List[Document], sync_to_pinecone: bool = False):
        """ChromaDB에 논문 저장 (필요 시 Pinecone에도 동기화)"""
        if self.chroma_store:
            self.chroma_store.add_documents(documents)
            print(f"[RAG] ChromaDB에 {len(documents)}건 저장 완료")

        if sync_to_pinecone and self.pinecone_store:
            self.pinecone_store.add_documents(documents)
            print(f"[RAG] Pinecone에 {len(documents)}건 동기화 완료")

    def get_collection_count(self) -> int:
        """저장된 문서 수 반환"""
        if self.chroma_store:
            return self.chroma_store._collection.count()
        return 0
