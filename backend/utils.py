from datetime import datetime, timedelta
from typing import List, Dict, Any

# ==========================================
# 1. MBTI Persona & Action Strategy
# ==========================================
MBTI_STRATEGIES = {
    "E": "외향적 성향(E)인 당신을 위해 러닝 크루나 그룹 PT처럼 타인과 활력을 나눌 수 있는 운동을 추천합니다.",
    "I": "내향적 성향(I)인 당신을 위해 홈트레이닝, 필라테스, 명상 리트릿처럼 혼자만의 몰입이 가능한 활동을 권장합니다.",
    "T": "분석적 성향(T)인 당신을 위해 심박수, 칼로리 소모량 등 정교한 수치를 활용한 데이터를 기반으로 조언합니다.",
    "F": "감성적 성향(F)인 당신의 몸과 마음이 조화를 이룰 수 있도록, 오늘의 컨디션에 맞춘 부드러운 케어를 제안합니다."
}

def get_mbti_persona_prompt(mbti: str) -> str:
    """MBTI를 기반으로 시스템 페르소나와 실천 전략 프롬프트 생성"""
    if not mbti or len(mbti) != 4:
        return "표준 헬스케어 코치로서 데이터에 기반한 보편적인 조언을 제공하세요."
    
    # E/I(0), N/S(1), T/F(2), P/J(3)
    p_ei = MBTI_STRATEGIES.get(mbti[0].upper(), "")
    p_tf = MBTI_STRATEGIES.get(mbti[2].upper(), "")
    
    return f"{p_tf} 특별히 {p_ei}"

# ==========================================
# 2. Progress & Roadmap Logic
# ==========================================
def calculate_goal_progress(start_w: float, current_w: float, target_w: float) -> Dict[str, Any]:
    """목표 체중 대비 현재 달성률 및 로드맵 계산"""
    total_diff = abs(start_w - target_w)
    if total_diff == 0: return {"progress": 100, "status": "Goal achieved"}
    
    achieved_diff = abs(start_w - current_w)
    progress_pct = min(round((achieved_diff / total_diff) * 100, 1), 100)
    
    status = "정기적인 페이스를 유지하고 있습니다."
    if progress_pct < 20: status = "이제 시작입니다! 첫 고비만 넘기면 데이터가 증명할 것입니다."
    elif progress_pct > 80: status = "목표가 눈앞에 있습니다! 마지막 스퍼트를 올릴 때입니다."
        
    return {
        "progress_pct": progress_pct,
        "remaining_weight": round(abs(current_w - target_w), 2),
        "status_message": status
    }

# ==========================================
# 3. Dynamic Lifestyle Timeline (T-Zero)
# ==========================================
def generate_lifestyle_plan(wake_time_str: str, sleep_time_str: str) -> List[Dict[str, Any]]:
    """
    기상/취침 시간(HH:MM)을 기준으로 유동적인 건강 루틴 생성
    """
    plan = []
    
    # 기상 시점 (T+0)
    plan.append({"time": "T+0", "activity": "기상 후 미지근한 물 한 잔 + 스트레칭", "type": "health"})
    
    # 오전 집중 시간 (T+2)
    plan.append({"time": "T+2", "activity": "가장 몰입이 필요한 업무 혹은 고강도 근력 운동", "type": "work/exercise"})
    
    # 오후 대사 활성 (T+6)
    plan.append({"time": "T+6", "activity": "단백질 위주의 건강한 점심 식사 (식이섬유 듬뿍)", "type": "meal"})
    
    # 취침 준비 (취침 2시간 전)
    plan.append({"time": "T-2", "activity": "모든 디지털 기기 오프 (멜라토닌 분비 촉진)", "type": "sleep_prep"})
    
    return plan
