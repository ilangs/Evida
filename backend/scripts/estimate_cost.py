import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def calculate_monthly_margin():
    """
    유저 1인당 한 달 평균 API 및 유지보수 비용을 추산하여
    프리미엄 구독(월 9,900원)의 마진율을 계산합니다.
    """
    subscription_fee = 9900  # 월 구독료 (KRW)
    exchange_rate = 1400     # 환율 (KRW/USD)

    # 1. AI API 비용 추산 (GPT-4o-mini 기준)
    # - 가격: 입력 $0.150 / 1M tokens, 출력 $0.600 / 1M tokens
    
    # 시나리오: 주간 건강 리포트 (월 4회)
    report_input_tokens = 4 * 2000
    report_output_tokens = 4 * 1000
    
    # 시나리오: 데일리 AI 코칭 챗봇 (월 40회 질문/답변)
    chat_input_tokens = 40 * 600
    chat_output_tokens = 40 * 400
    
    total_input_tokens = report_input_tokens + chat_input_tokens
    total_output_tokens = report_output_tokens + chat_output_tokens
    
    llm_cost_usd = (total_input_tokens / 1_000_000) * 0.150 + (total_output_tokens / 1_000_000) * 0.600
    
    # 2. Vision API 비용 추산 (GPT-4o Vision)
    # 시나리오: 월 1회 혈액검사 스캔 (고해상도 이미지 약 $0.01)
    ocr_cost_usd = 0.01
    
    api_cost_krw = (llm_cost_usd + ocr_cost_usd) * exchange_rate
    
    # 3. 기타 인프라/서버 유지 비용 (DB, Vector DB, Hosting 등 유저당 할당분)
    # Pinecone 및 Supabase 프리티어를 넘어간 시점에서의 유저 1인당 분담금 보수적 추산
    infra_cost_krw = 200 
    
    # 4. 결제 수수료 (PG사 수수료 통상 약 3%)
    pg_fee_krw = subscription_fee * 0.03
    
    # 총 비용 계산
    total_cost_krw = api_cost_krw + infra_cost_krw + pg_fee_krw
    
    # 마진 계산
    margin = subscription_fee - total_cost_krw
    margin_percent = (margin / subscription_fee) * 100
    
    print("=== 📊 프리미엄 구독(9,900원) 월간 마진율 추산 ===")
    print(f"- LLM API 요금 (GPT-4o-mini + Vision): 약 {api_cost_krw:.0f}원 (${llm_cost_usd+ocr_cost_usd:.4f})")
    print(f"- 클라우드 인프라 비용 (유저당 N빵): 약 {infra_cost_krw}원")
    print(f"- 결제 PG 수수료 (3%): {pg_fee_krw:.0f}원")
    print("---------------------------------------------------------")
    print(f"💰 유저 1인당 월간 총 원가: {total_cost_krw:.0f}원")
    print(f"🚀 유저 1인당 월간 순이익: {margin:.0f}원")
    print(f"📈 예상 마진율: {margin_percent:.1f}%")

if __name__ == "__main__":
    calculate_monthly_margin()
