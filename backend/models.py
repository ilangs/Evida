import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, DECIMAL, DateTime, ForeignKey, Enum, Text, Date, func, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    gender: Mapped[Optional[str]] = mapped_column(String(10))
    mbti: Mapped[Optional[str]] = mapped_column(String(4))
    goal_type: Mapped[str] = mapped_column(String(20)) # weight_loss, gain_muscle, maintenance
    goal_description: Mapped[Optional[str]] = mapped_column(Text) # "6개월 10kg 감량"
    
    start_weight: Mapped[Optional[float]] = mapped_column(DECIMAL(5, 2))
    target_weight: Mapped[Optional[float]] = mapped_column(DECIMAL(5, 2))
    target_duration_months: Mapped[Optional[int]] = mapped_column(Integer, default=6)
    
    # 표준 생활 패턴 (HH:MM 형식)
    wake_time: Mapped[Optional[str]] = mapped_column(String(5)) 
    sleep_time: Mapped[Optional[str]] = mapped_column(String(5))
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    
    # 법적 동의 관련 필드
    is_consented: Mapped[bool] = mapped_column(Boolean, default=False)
    consented_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    consent_version: Mapped[Optional[str]] = mapped_column(String(10), default="1.0")
    
    # 프리미엄 구독 (Phase 3-K)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    premium_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    biometrics: Mapped[List["Biometric"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    logs: Mapped[List["LifeLog"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Biometric(Base):
    __tablename__ = "biometrics"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    test_date: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow)
    
    weight: Mapped[Optional[float]] = mapped_column(DECIMAL(5, 2))
    skeletal_muscle_mass: Mapped[Optional[float]] = mapped_column(DECIMAL(5, 2))
    body_fat_pct: Mapped[Optional[float]] = mapped_column(DECIMAL(4, 1))
    blood_glucose: Mapped[Optional[int]] = mapped_column(Integer)
    ldl_cholesterol: Mapped[Optional[int]] = mapped_column(Integer)
    hdl_cholesterol: Mapped[Optional[int]] = mapped_column(Integer)
    crp_level: Mapped[Optional[float]] = mapped_column(DECIMAL(5, 2))
    
    raw_ocr_text: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    user: Mapped["User"] = relationship(back_populates="biometrics")

class LifeLog(Base):
    __tablename__ = "lifelogs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    log_type: Mapped[str] = mapped_column(String(20)) # sleep, work, meal, exercise
    shift_type: Mapped[Optional[str]] = mapped_column(String(20)) # day, night, off
    
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime)
    content: Mapped[Optional[str]] = mapped_column(Text)
    intensity: Mapped[Optional[int]] = mapped_column(Integer)
    calories: Mapped[Optional[int]] = mapped_column(Integer)
    
    user: Mapped["User"] = relationship(back_populates="logs")

class PaymentLog(Base):
    __tablename__ = "payment_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    imp_uid: Mapped[str] = mapped_column(String(100), unique=True)
    merchant_uid: Mapped[str] = mapped_column(String(100))
    amount: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20)) # paid, failed, cancelled
    plan_type: Mapped[str] = mapped_column(String(50)) # premium_monthly, onetime_analysis
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

class MedicalKnowledge(Base):
    __tablename__ = "medical_knowledge"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text)
    authors: Mapped[Optional[str]] = mapped_column(Text)
    journal: Mapped[Optional[str]] = mapped_column(String(255))
    pub_year: Mapped[Optional[int]] = mapped_column(Integer)
    doi: Mapped[Optional[str]] = mapped_column(String(100))
    summary: Mapped[Optional[str]] = mapped_column(Text)
    vector_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True)


class AIReportCache(Base):
    """
    LLM 호출 결과를 캐시하여 불필요한 재호출을 방지하는 테이블.
    - cache_key : 사용자 조건의 SHA-256 해시 (conditions_hash)
    - report_json: GPT가 생성한 전체 JSON 문자열
    - ttl_days  : 유효 만료일 (기본 7일)
    """
    __tablename__ = "ai_report_cache"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    cache_key: Mapped[str] = mapped_column(String(64), index=True)  # SHA-256 hex
    report_json: Mapped[str] = mapped_column(Text)                  # JSON string
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    hit_count: Mapped[int] = mapped_column(Integer, default=0)       # 캐시 히트 수
