import uuid
from typing import TypedDict, Annotated, Sequence
from datetime import datetime

class CoachingState(TypedDict):
    user_id: str
    user_profile: dict
    latest_bio: dict
    goal_status: dict
    milestones: list
    generated_message: str

def fetch_user_data(state: CoachingState):
    # This would fetch from DB in a real scenario
    return state

def calculate_milestone_progress(state: CoachingState):
    return state

def generate_coaching_message(state: CoachingState):
    user = state.get("user_profile", {})
    goal_status = state.get("goal_status", {})
    name = user.get("name", "회원")
    
    # Simple prompt logic for the mock
    message = f"🌟 주간 AI 코칭 메시지 🌟\n\n안녕하세요 {name}님!\n새로운 한 주가 시작되었습니다.\n"
    message += f"현재 목표 달성률은 {goal_status.get('progress_pct', 0)}% 입니다. 잘 하고 계십니다!\n"
    message += "이번 주도 저희와 함께 힘차게 달려볼까요?! 파이팅입니다!"
    
    return {"generated_message": message}

# Simple LangGraph setup mock
class MockLangGraph:
    def invoke(self, state):
        state = fetch_user_data(state)
        state = calculate_milestone_progress(state)
        state = generate_coaching_message(state)
        return state

def run_weekly_coaching(user_profile: dict, goal_status: dict) -> str:
    graph = MockLangGraph()
    result = graph.invoke({
        "user_id": str(uuid.uuid4()),
        "user_profile": user_profile,
        "latest_bio": {},
        "goal_status": goal_status,
        "milestones": [],
        "generated_message": ""
    })
    return result["generated_message"]
