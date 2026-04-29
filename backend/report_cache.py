"""
Vital Intelligence — AI Report Cache Service
==============================================
LLM 호출 비용 절감을 위한 스마트 캐싱 레이어.

[동작 원리]
1. 사용자의 '처방에 영향을 미치는 조건들'을 수치화한 후 SHA-256 해시 생성
2. 동일/유사 해시가 DB에 존재하고 TTL(7일) 이내면 → 캐시된 리포트 즉시 반환
3. 유사도 판단에 사용되는 허용 오차(Tolerance):
   - 체중        : ±0.5kg   (식단·운동 처방에 영향 없음)
   - 혈당        : ±5 mg/dL (위험 등급 변경 없는 수준)
   - LDL/HDL     : ±5 mg/dL
   - 체지방률    : ±0.5%
   - 목표/MBTI   : 완전 일치 필수 (처방 방향 자체가 바뀜)
"""

import hashlib
import json
import math
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple


# ════════════════════════════════════════════════════════════════
# 허용 오차 (임상적 처방 변경 기준)
# ════════════════════════════════════════════════════════════════
TOLERANCE = {
    "weight":               0.5,   # kg
    "skeletal_muscle_mass": 0.5,   # kg
    "body_fat_pct":         0.5,   # %
    "blood_glucose":        5.0,   # mg/dL
    "ldl_cholesterol":      5.0,   # mg/dL
    "hdl_cholesterol":      5.0,   # mg/dL
    "triglycerides":        10.0,  # mg/dL
    "crp_level":            0.2,   # mg/L
}

# 캐시 유효 기간 (일)
CACHE_TTL_DAYS = 7


def _round_to_tolerance(value: Optional[float], tolerance: float) -> Optional[float]:
    """값을 허용 오차 단위로 버킷화하여 미세 변동을 흡수"""
    if value is None:
        return None
    # 허용 오차 단위로 반올림 → 같은 버킷이면 동일 해시 생성
    return round(value / tolerance) * tolerance


def build_cache_key(user: Dict[str, Any], biometric: Dict[str, Any]) -> str:
    """
    처방에 영향을 미치는 조건들을 정규화하여 SHA-256 해시 생성.
    
    허용 오차 내 변동은 동일한 해시가 생성되어 캐시를 재사용합니다.
    처방 방향이 달라지는 조건(목표, MBTI, 성별)은 완전 일치를 요구합니다.
    """
    normalized = {
        # 처방 방향 결정 (완전 일치 필수)
        "goal_type":   user.get("goal_type", ""),
        "mbti":        (user.get("mbti") or "").upper(),
        "gender":      (user.get("gender") or "").lower(),
        "age_decade":  (user.get("age") or 0) // 10,  # 연령대 단위 (30대, 40대...)

        # 체성분 (허용 오차 적용)
        "weight":      _round_to_tolerance(biometric.get("weight"), TOLERANCE["weight"]),
        "muscle":      _round_to_tolerance(biometric.get("skeletal_muscle_mass"), TOLERANCE["skeletal_muscle_mass"]),
        "fat_pct":     _round_to_tolerance(biometric.get("body_fat_pct"), TOLERANCE["body_fat_pct"]),

        # 혈액 지표 (허용 오차 적용)
        "glucose":     _round_to_tolerance(biometric.get("blood_glucose"), TOLERANCE["blood_glucose"]),
        "ldl":         _round_to_tolerance(biometric.get("ldl_cholesterol"), TOLERANCE["ldl_cholesterol"]),
        "hdl":         _round_to_tolerance(biometric.get("hdl_cholesterol"), TOLERANCE["hdl_cholesterol"]),
        "tg":          _round_to_tolerance(biometric.get("triglycerides"), TOLERANCE["triglycerides"]),
    }

    # 결정론적 직렬화 (sort_keys=True 필수)
    raw = json.dumps(normalized, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def is_cache_valid(created_at: datetime, ttl_days: int = CACHE_TTL_DAYS) -> bool:
    """캐시 생성일로부터 TTL 이내인지 확인"""
    age = datetime.utcnow() - created_at
    return age < timedelta(days=ttl_days)


def explain_cache_miss(
    old_biometric: Dict[str, Any],
    new_biometric: Dict[str, Any],
    old_user: Dict[str, Any],
    new_user: Dict[str, Any],
) -> str:
    """
    캐시 미스 이유를 사람이 읽을 수 있는 문자열로 반환 (로깅용).
    """
    reasons = []

    # 처방 방향 변경 확인
    if old_user.get("goal_type") != new_user.get("goal_type"):
        reasons.append(f"목표 변경: {old_user.get('goal_type')} → {new_user.get('goal_type')}")
    if (old_user.get("mbti") or "").upper() != (new_user.get("mbti") or "").upper():
        reasons.append(f"MBTI 변경: {old_user.get('mbti')} → {new_user.get('mbti')}")

    # 수치 변화 확인
    metric_labels = {
        "weight": ("체중", "kg", TOLERANCE["weight"]),
        "blood_glucose": ("혈당", "mg/dL", TOLERANCE["blood_glucose"]),
        "ldl_cholesterol": ("LDL", "mg/dL", TOLERANCE["ldl_cholesterol"]),
        "hdl_cholesterol": ("HDL", "mg/dL", TOLERANCE["hdl_cholesterol"]),
        "body_fat_pct": ("체지방률", "%", TOLERANCE["body_fat_pct"]),
    }

    for key, (label, unit, tol) in metric_labels.items():
        old_v = old_biometric.get(key)
        new_v = new_biometric.get(key)
        if old_v is not None and new_v is not None:
            delta = abs(float(new_v) - float(old_v))
            if delta > tol:
                reasons.append(f"{label} 변동: {delta:.1f}{unit} (허용 오차 ±{tol}{unit} 초과)")

    return " / ".join(reasons) if reasons else "TTL 만료"


# ════════════════════════════════════════════════════════════════
# DB 연동 함수 (async SQLAlchemy)
# ════════════════════════════════════════════════════════════════
async def get_cached_report(
    db,
    user_id,
    cache_key: str,
) -> Tuple[Optional[Dict], Optional[Any]]:
    """
    캐시 키로 유효한 리포트를 조회.
    반환: (report_dict | None, cache_row | None)
    """
    from sqlalchemy import select
    from models import AIReportCache

    result = await db.execute(
        select(AIReportCache)
        .where(AIReportCache.user_id == user_id)
        .where(AIReportCache.cache_key == cache_key)
        .order_by(AIReportCache.created_at.desc())
        .limit(1)
    )
    row = result.scalar_one_or_none()

    if row and is_cache_valid(row.created_at):
        return json.loads(row.report_json), row

    return None, None


async def save_report_cache(
    db,
    user_id,
    cache_key: str,
    report: Dict[str, Any],
) -> None:
    """새 리포트를 DB에 캐시 저장하고 오래된 캐시는 정리"""
    from sqlalchemy import delete
    from models import AIReportCache

    # 해당 사용자의 만료된 캐시 정리 (7일 이상 된 것들)
    cutoff = datetime.utcnow() - timedelta(days=CACHE_TTL_DAYS)
    await db.execute(
        delete(AIReportCache).where(
            AIReportCache.user_id == user_id,
            AIReportCache.created_at < cutoff
        )
    )

    # 새 캐시 저장
    new_cache = AIReportCache(
        user_id=user_id,
        cache_key=cache_key,
        report_json=json.dumps(report, ensure_ascii=False),
    )
    db.add(new_cache)
    await db.commit()


async def increment_hit_count(db, cache_row) -> None:
    """캐시 히트 카운터 증가 (비용 절감 통계용)"""
    cache_row.hit_count += 1
    await db.commit()
