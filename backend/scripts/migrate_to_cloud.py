"""
데이터베이스 마이그레이션 전략 스크립트
로컬 DB -> 클라우드 PostgreSQL (Supabase/AWS RDS)
"""
import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

# 상위 폴더의 models 모듈 참조를 위해 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Base

async def migrate_schema():
    load_dotenv()
    # 실제 이전할 프로덕션 환경의 클라우드 URL (별도 분리)
    cloud_url = os.getenv("PROD_DATABASE_URL") 
    
    if not cloud_url:
        print("[오류] PROD_DATABASE_URL 환경 변수가 설정되지 않았습니다.")
        return

    # 1. 클라우드 DB에 연결하여 SQLAlchemy 모델 기반의 전체 테이블/스키마 생성
    engine = create_async_engine(cloud_url, echo=True)
    async with engine.begin() as conn:
        print("[1/2] 클라우드 DB 테이블 및 스키마 생성 중...")
        await conn.run_sync(Base.metadata.create_all)
        
    print("[2/2] 클라우드 스키마 구축 완료.")
    
    # 2. 실제 데이터 마이그레이션(ETL) 가이드 안내
    print("\n[안내] 데이터 마이그레이션은 다음과 같이 pg_dump 방식을 권장합니다.")
    print("터미널에서 아래 명령어를 실행하여 로컬 데이터를 클라우드로 이전하세요:")
    print("--------------------------------------------------")
    print("pg_dump -U <로컬유저> -h 127.0.0.1 -d <로컬DB명> -a | psql -U <클라우드유저> -h <클라우드엔드포인트> -d <클라우드DB명>")
    print("--------------------------------------------------")

if __name__ == "__main__":
    asyncio.run(migrate_schema())
