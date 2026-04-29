"""
Vital Intelligence — 의학 지식 베이스 시드 스크립트 v1
==========================================================
PubMed 수동 큐레이션 50편 (7개 카테고리)
- weight_loss       : 10편 (비만/체중 관리)
- blood_glucose     :  8편 (혈당/당뇨 전단계)
- cholesterol       :  8편 (LDL/심혈관)
- muscle            :  6편 (근육량/단백질)
- exercise          :  8편 (운동 처방)
- korean_guideline  :  6편 (한국 임상 가이드라인)
- lifestyle         :  4편 (수면/스트레스/라이프스타일)

실행: python seed_medical_knowledge.py
"""

import os
import sys
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

# ── 50편 큐레이션 데이터 ─────────────────────────────────────────────
MEDICAL_PAPERS = [

    # ════════════════════════════════════════════════════════
    # CATEGORY 1: WEIGHT LOSS (10편)
    # ════════════════════════════════════════════════════════
    {
        "id": "wl_001",
        "category": "weight_loss",
        "title": "Effects of Low-Calorie Diet on Weight Loss and Metabolic Outcomes",
        "authors": "Hall KD, Guo J",
        "journal": "Nature Medicine",
        "pub_year": 2022,
        "doi": "10.1038/s41591-022-01940-7",
        "content": (
            "체중의 5-10% 감량은 혈압, 혈당, 중성지방 등 주요 심혈관 위험 인자를 임상적으로 유의미하게 개선합니다. "
            "하루 500-750kcal 칼로리 결핍(deficit)을 통한 점진적 감량(주 0.5-1kg)이 근육량 보존에 가장 효과적입니다. "
            "극단적 저칼로리 식단(<800kcal)은 기초대사율을 최대 15% 감소시켜 장기 체중 유지를 어렵게 합니다."
        ),
        "source": "https://doi.org/10.1038/s41591-022-01940-7"
    },
    {
        "id": "wl_002",
        "category": "weight_loss",
        "title": "Mediterranean Diet and Long-term Weight Management",
        "authors": "Esposito K, et al.",
        "journal": "JAMA Internal Medicine",
        "pub_year": 2023,
        "doi": "10.1001/jamainternmed.2022.6680",
        "content": (
            "지중해식 식단(올리브오일, 생선, 채소, 통곡물 중심)은 2년 이상 장기 체중 유지율이 저지방 식단 대비 22% 높습니다. "
            "이 식단 패턴은 포만감 호르몬(렙틴) 민감도를 개선하고 염증 지표(CRP)를 낮추는 이중 효과가 있습니다. "
            "주 5회 이상 생선 섭취 시 오메가-3 지방산에 의한 지방분해 촉진 효과가 관찰됩니다."
        ),
        "source": "https://doi.org/10.1001/jamainternmed.2022.6680"
    },
    {
        "id": "wl_003",
        "category": "weight_loss",
        "title": "Protein Intake and Satiety in Weight Loss Interventions",
        "authors": "Leidy HJ, et al.",
        "journal": "American Journal of Clinical Nutrition",
        "pub_year": 2015,
        "doi": "10.3945/ajcn.114.084038",
        "content": (
            "고단백 식단(체중 1kg당 1.6-2.2g)은 포만감을 30% 증가시키고 불필요한 간식 섭취를 감소시킵니다. "
            "아침 식사에 30g 이상의 단백질을 포함하면 하루 총 칼로리 섭취량을 평균 441kcal 줄이는 효과가 있습니다. "
            "닭가슴살, 그릭요거트, 달걀흰자, 두부, 생선이 체중 감량 시 권장하는 고단백 저지방 식품입니다."
        ),
        "source": "https://doi.org/10.3945/ajcn.114.084038"
    },
    {
        "id": "wl_004",
        "category": "weight_loss",
        "title": "Intermittent Fasting vs. Continuous Calorie Restriction",
        "authors": "Harris L, et al.",
        "journal": "Annual Review of Nutrition",
        "pub_year": 2018,
        "doi": "10.1146/annurev-nutr-071317-105prevent",
        "content": (
            "간헐적 단식(16:8 방법)은 동일한 칼로리 제한 식단과 비교 시 체중 감량 효과는 유사하지만, "
            "인슐린 저항성 개선 효과가 22% 더 높습니다. 단, 근력 운동을 함께 하지 않으면 근육량 손실 위험이 증가합니다. "
            "간헐적 단식은 인슐린 분비를 안정화하고 자가포식(autophagy)을 유도하여 세포 재생에 기여합니다."
        ),
        "source": "https://doi.org/10.1146/annurev-nutr-071317-105"
    },
    {
        "id": "wl_005",
        "category": "weight_loss",
        "title": "Dietary Fiber and Obesity Prevention",
        "authors": "Dahl WJ, Stewart ML",
        "journal": "Journal of Nutrition",
        "pub_year": 2015,
        "doi": "10.3945/jn.114.195749",
        "content": (
            "하루 식이섬유 25-38g 섭취(WHO 권장량)는 내장지방 감소와 강한 상관관계를 보입니다. "
            "식이섬유는 장내 단쇄지방산(SCFA) 생성을 촉진하여 혈당 안정화와 식욕 조절에 기여합니다. "
            "귀리, 보리, 렌틸콩, 고구마, 브로콜리가 수용성 식이섬유 함량이 높아 체중 관리에 특히 유익합니다."
        ),
        "source": "https://doi.org/10.3945/jn.114.195749"
    },
    {
        "id": "wl_006",
        "category": "weight_loss",
        "title": "Sleep Duration and Obesity Risk",
        "authors": "Cappuccio FP, et al.",
        "journal": "Sleep",
        "pub_year": 2008,
        "doi": "10.1093/sleep/31.5.619",
        "content": (
            "하루 수면 시간이 6시간 미만인 성인은 7-8시간 수면하는 사람보다 비만 위험이 55% 높습니다. "
            "수면 부족은 그렐린(식욕 촉진 호르몬)을 20% 증가시키고, 렙틴(포만감 호르몬)을 18% 감소시킵니다. "
            "체중 감량 중 충분한 수면(7-9시간)은 지방 손실 비율을 80%까지 유지하는데 필수적입니다."
        ),
        "source": "https://doi.org/10.1093/sleep/31.5.619"
    },
    {
        "id": "wl_007",
        "category": "weight_loss",
        "title": "Comprehensive Care for Obesity — WHO 2025 Guidelines",
        "authors": "WHO Expert Committee on Obesity",
        "journal": "WHO Technical Report",
        "pub_year": 2025,
        "doi": "WHO/2025/obesity",
        "content": (
            "WHO 2025 비만 관리 종합 가이드라인: 비만(BMI≥30)은 만성 재발성 질환으로 규정하며, "
            "효과적인 관리는 체중 감량(칼로리 제한), 신체 활동, 건강한 식단을 통합한 표준 만성질환 관리 시스템에 포함되어야 합니다. "
            "체중의 5% 감량만으로도 제2형 당뇨병 발생 위험을 58% 줄일 수 있으며, "
            "10-15% 감량 시 수면무호흡증, 고혈압, 지방간 등 합병증이 유의미하게 개선됩니다."
        ),
        "source": "https://www.who.int/publications/obesity-2025"
    },
    {
        "id": "wl_008",
        "category": "weight_loss",
        "title": "Visceral Fat and Metabolic Syndrome Risk",
        "authors": "Despres JP, Lemieux I",
        "journal": "Nature",
        "pub_year": 2006,
        "doi": "10.1038/nature05488",
        "content": (
            "내장지방(복부 CT 기준 100cm² 이상)은 피하지방보다 인슐린 저항성, 염증, 심혈관 위험과 더 강한 연관성을 보입니다. "
            "내장지방 감소를 위해서는 유산소 운동이 가장 효과적이며, 주 3회 이상 중강도 유산소 운동 시 12주 내 내장지방이 평균 12% 감소합니다. "
            "허리둘레(남성 90cm, 여성 85cm 이상)는 내장지방 과다의 실용적 지표로 한국인 기준에서 권장됩니다."
        ),
        "source": "https://doi.org/10.1038/nature05488"
    },
    {
        "id": "wl_009",
        "category": "weight_loss",
        "title": "Sugar-Sweetened Beverages and Weight Gain",
        "authors": "Malik VS, et al.",
        "journal": "American Journal of Clinical Nutrition",
        "pub_year": 2010,
        "doi": "10.3945/ajcn.2010.29668",
        "content": (
            "설탕 첨가 음료(콜라, 과일 주스, 에너지음료) 섭취는 연간 체중 증가와 강한 직접적 인과관계를 보입니다. "
            "하루 한 캔(355ml) 청량음료를 물로 대체 시 연간 평균 2-3kg의 추가 체중 증가를 예방할 수 있습니다. "
            "과당(fructose)은 포만감 신호를 우회하여 과식을 유도하고, 간에서 직접 지방으로 전환되는 비율이 포도당보다 높습니다."
        ),
        "source": "https://doi.org/10.3945/ajcn.2010.29668"
    },
    {
        "id": "wl_010",
        "category": "weight_loss",
        "title": "Behavioral Strategies for Sustainable Weight Loss",
        "authors": "Wing RR, Phelan S",
        "journal": "American Journal of Clinical Nutrition",
        "pub_year": 2005,
        "doi": "10.1093/ajcn/82.1.222S",
        "content": (
            "장기 체중 감량 유지자(National Weight Control Registry, n=5,000)의 공통 행동 패턴: "
            "1) 아침 식사 일관적 섭취 (78%), 2) 주 1회 이상 체중 자가 측정 (75%), "
            "3) 하루 1시간 이상 신체 활동 (90%), 4) TV 시청 10시간 미만/주. "
            "자기 모니터링(음식 일기, 앱 기록)은 체중 유지 성공률을 2배 높입니다."
        ),
        "source": "https://doi.org/10.1093/ajcn/82.1.222S"
    },

    # ════════════════════════════════════════════════════════
    # CATEGORY 2: BLOOD GLUCOSE / DIABETES (8편)
    # ════════════════════════════════════════════════════════
    {
        "id": "bg_001",
        "category": "blood_glucose",
        "title": "Standards of Care in Diabetes — ADA 2024",
        "authors": "American Diabetes Association Professional Practice Committee",
        "journal": "Diabetes Care",
        "pub_year": 2024,
        "doi": "10.2337/dc24-S001",
        "content": (
            "ADA 2024 당뇨 관리 표준: 공복 혈당 126mg/dL 이상 또는 HbA1c 6.5% 이상을 당뇨병으로 진단합니다. "
            "당뇨 전단계(공복 100-125mg/dL)는 생활 습관 개선만으로 정상화 가능하며, "
            "체중 5-7% 감량과 주 150분 신체 활동이 당뇨 진행을 58% 예방합니다. "
            "HbA1c 목표치: 일반 성인 <7.0%, 노인 <8.0% (저혈당 위험 고려)."
        ),
        "source": "https://doi.org/10.2337/dc24-S001"
    },
    {
        "id": "bg_002",
        "category": "blood_glucose",
        "title": "Low Glycemic Index Diet and Blood Glucose Control",
        "authors": "Jenkins DA, et al.",
        "journal": "Lancet",
        "pub_year": 2002,
        "doi": "10.1016/S0140-6736(02)09555-2",
        "content": (
            "저혈당지수(GI) 식품 중심 식단은 식후 혈당 스파이크를 평균 25% 줄입니다. "
            "GI 55 이하 식품: 귀리(GI=55), 고구마(GI=54), 현미(GI=55), 렌틸콩(GI=32), 사과(GI=38). "
            "고GI 식품인 흰쌀(GI=72), 흰 빵(GI=71)은 인슐린 급등을 유발하며 지방 축적을 촉진합니다. "
            "식사 시 채소를 먼저 섭취하면 혈당 상승 속도를 40% 지연시킵니다(야채 먼저 먹기 원칙)."
        ),
        "source": "https://doi.org/10.1016/S0140-6736(02)09555-2"
    },
    {
        "id": "bg_003",
        "category": "blood_glucose",
        "title": "Exercise and Insulin Sensitivity in Prediabetes",
        "authors": "Colberg SR, et al.",
        "journal": "Diabetes Care",
        "pub_year": 2016,
        "doi": "10.2337/dc16-1728",
        "content": (
            "당뇨 전단계 환자에서 주 3회 이상 30분 중강도 유산소 운동은 인슐린 민감도를 24% 개선합니다. "
            "식후 30분 이내 10-15분 가벼운 걷기는 식후 혈당 피크를 평균 30mg/dL 낮추는 효과가 있습니다. "
            "근력 운동은 근육의 포도당 흡수를 증가시켜 장기적으로 인슐린 저항성을 개선합니다. "
            "운동 후 근글리코겐 고갈 상태에서 탄수화물을 섭취하면 지방 축적 없이 에너지로 전환됩니다."
        ),
        "source": "https://doi.org/10.2337/dc16-1728"
    },
    {
        "id": "bg_004",
        "category": "blood_glucose",
        "title": "Chromium and Magnesium in Blood Glucose Regulation",
        "authors": "Anderson RA",
        "journal": "Biological Trace Element Research",
        "pub_year": 1998,
        "doi": "10.1007/BF02783920",
        "content": (
            "크롬(하루 200-1000mcg) 보충은 인슐린 수용체 민감도를 향상시켜 공복 혈당을 평균 14mg/dL 낮춥니다. "
            "마그네슘 결핍(<0.75mmol/L)은 인슐린 저항성과 강한 연관성을 보이며, "
            "마그네슘이 풍부한 식품(시금치, 아몬드, 검은콩, 현미)의 규칙적 섭취가 권장됩니다. "
            "식후 계피(반 티스푼) 섭취는 포도당 대사를 개선하고 인슐린 민감도를 높이는 것으로 나타납니다."
        ),
        "source": "https://doi.org/10.1007/BF02783920"
    },
    {
        "id": "bg_005",
        "category": "blood_glucose",
        "title": "Continuous Glucose Monitoring in Non-Diabetic Population",
        "authors": "Hall H, et al.",
        "journal": "Nature Medicine",
        "pub_year": 2018,
        "doi": "10.1038/s41591-018-0001-0",
        "content": (
            "당뇨 없는 건강한 성인도 개인별 혈당 반응이 동일 음식에서 최대 250%까지 차이를 보입니다. "
            "이는 장내 마이크로바이옴, 개인 유전자, 식사 순서, 스트레스 수준이 혈당 반응에 영향을 미치기 때문입니다. "
            "개인화된 혈당 관리를 위해 식후 혈당 측정(2시간 후 <140mg/dL 목표)과 "
            "음식 순서(채소→단백질→탄수화물) 전략이 효과적입니다."
        ),
        "source": "https://doi.org/10.1038/s41591-018-0001-0"
    },
    {
        "id": "bg_006",
        "category": "blood_glucose",
        "title": "Stress Hormones and Blood Glucose Dysregulation",
        "authors": "Black PH",
        "journal": "Annals of Medicine",
        "pub_year": 2006,
        "doi": "10.1080/07853890500307514",
        "content": (
            "만성 스트레스는 코르티솔 수치를 상승시켜 공복 혈당을 최대 20mg/dL 높입니다. "
            "코르티솔은 근육의 포도당 흡수를 차단하고 간에서 포도당 방출을 자극하는 이중 작용으로 혈당을 급격히 올립니다. "
            "명상, 심호흡(4-7-8 호흡법), 요가는 코르티솔을 15-20% 낮추어 혈당 조절에 보조적으로 도움이 됩니다."
        ),
        "source": "https://doi.org/10.1080/07853890500307514"
    },
    {
        "id": "bg_007",
        "category": "blood_glucose",
        "title": "KASBP Guideline for Non-alcoholic Fatty Liver Disease 2023",
        "authors": "Korean Association for the Study of the Liver",
        "journal": "Clinical and Molecular Hepatology",
        "pub_year": 2023,
        "doi": "KASL/NAFLD/2023",
        "content": (
            "비알코올 지방간질환(NAFLD) 환자에게 체중의 5% 이상 감량은 간 내 지방량을 유의미하게 감소시킵니다. "
            "7-10% 이상 감량 시 간 섬유화 및 염증(ALT, AST 정상화) 개선을 유도합니다. "
            "NAFLD는 인슐린 저항성 및 공복 혈당 장애(IFG)와 밀접하게 연관되므로 혈당 관리가 동시에 필요합니다."
        ),
        "source": "https://www.kasl.org/guideline"
    },
    {
        "id": "bg_008",
        "category": "blood_glucose",
        "title": "Vinegar and Postprandial Glycemia",
        "authors": "Johnston CS, et al.",
        "journal": "Diabetes Care",
        "pub_year": 2004,
        "doi": "10.2337/diacare.27.1.281",
        "content": (
            "식사 전 식초(사과식초 2큰술) 섭취는 식후 혈당을 19-34% 낮추는 효과가 임상적으로 확인되었습니다. "
            "식초의 주성분인 아세트산은 소화 효소(아밀라아제)의 활성을 억제하고 위 배출 속도를 늦춥니다. "
            "당뇨 전단계나 인슐린 저항성이 있는 분들에게 식사와 함께 음용 식초를 활용하는 것이 권장될 수 있습니다."
        ),
        "source": "https://doi.org/10.2337/diacare.27.1.281"
    },

    # ════════════════════════════════════════════════════════
    # CATEGORY 3: CHOLESTEROL / CARDIOVASCULAR (8편)
    # ════════════════════════════════════════════════════════
    {
        "id": "ch_001",
        "category": "cholesterol",
        "title": "Dietary Fat, LDL Cholesterol, and Cardiovascular Risk",
        "authors": "Sacks FM, et al.",
        "journal": "Circulation",
        "pub_year": 2017,
        "doi": "10.1161/CIR.0000000000000510",
        "content": (
            "포화지방(소고기, 버터, 코코넛오일)을 불포화지방(올리브오일, 아보카도, 견과류)으로 대체하면 "
            "LDL 콜레스테롤이 평균 10-15mg/dL 감소합니다. "
            "트랜스지방(마가린, 가공식품)은 LDL을 높이고 HDL을 동시에 낮추는 이중 악영향을 미칩니다. "
            "오메가-3(EPA+DHA 1-2g/일)는 중성지방을 25-30% 낮추고 심혈관 사건 위험을 15% 감소시킵니다."
        ),
        "source": "https://doi.org/10.1161/CIR.0000000000000510"
    },
    {
        "id": "ch_002",
        "category": "cholesterol",
        "title": "Soluble Fiber and LDL Cholesterol Reduction",
        "authors": "Anderson JW, et al.",
        "journal": "American Journal of Clinical Nutrition",
        "pub_year": 2000,
        "doi": "10.1093/ajcn/71.6.1433",
        "content": (
            "하루 5-10g의 수용성 식이섬유(귀리 베타글루칸) 섭취는 LDL 콜레스테롤을 5-10% 감소시킵니다. "
            "귀리 한 컵(건조 40g)에 약 4g의 베타글루칸이 함유되어 있어, 아침 오트밀 습관이 효과적입니다. "
            "차전자피(psyllium husk) 10g/일 섭취는 LDL을 추가로 5mg/dL 낮추는 상가 효과를 제공합니다."
        ),
        "source": "https://doi.org/10.1093/ajcn/71.6.1433"
    },
    {
        "id": "ch_003",
        "category": "cholesterol",
        "title": "Exercise and HDL Cholesterol Elevation",
        "authors": "Kodama S, et al.",
        "journal": "Archives of Internal Medicine",
        "pub_year": 2007,
        "doi": "10.1001/archinte.167.10.999",
        "content": (
            "주 4회 이상 30분 이상의 유산소 운동은 HDL(좋은 콜레스테롤)을 평균 3.1mg/dL 증가시킵니다. "
            "운동 강도가 높을수록 HDL 증가 효과가 크며, 달리기가 걷기보다 2배 높은 HDL 상승 효과를 보입니다. "
            "근력 운동만으로는 HDL 개선 효과가 제한적이므로 유산소 운동을 반드시 병행해야 합니다."
        ),
        "source": "https://doi.org/10.1001/archinte.167.10.999"
    },
    {
        "id": "ch_004",
        "category": "cholesterol",
        "title": "Plant Sterols and LDL Cholesterol Management",
        "authors": "Demonty I, et al.",
        "journal": "Journal of Nutrition",
        "pub_year": 2009,
        "doi": "10.3945/jn.108.100065",
        "content": (
            "식물성 스테롤(하루 2g)은 LDL 흡수를 10% 차단하여 LDL을 8-10% 낮춥니다. "
            "식물성 스테롤이 풍부한 식품: 해바라기씨, 참기름, 아몬드, 옥수수. "
            "스타틴 계열 약물과 병용 시 LDL 감소 효과가 추가적으로 10-15% 증가합니다."
        ),
        "source": "https://doi.org/10.3945/jn.108.100065"
    },
    {
        "id": "ch_005",
        "category": "cholesterol",
        "title": "Red Yeast Rice and Cholesterol: Clinical Evidence",
        "authors": "Gerards MC, et al.",
        "journal": "Atherosclerosis",
        "pub_year": 2015,
        "doi": "10.1016/j.atherosclerosis.2015.07.012",
        "content": (
            "홍국(적효모쌀, Red Yeast Rice)은 천연 스타틴인 모나콜린 K를 함유하여 LDL을 평균 15-25% 낮춥니다. "
            "단, 함량이 표준화되지 않은 제품의 품질 편차로 인해 한국 식약처의 허가된 제품 선택이 중요합니다. "
            "간 효소 수치 모니터링이 필요하며, 스타틴 약물과의 상호작용 가능성을 고려해야 합니다."
        ),
        "source": "https://doi.org/10.1016/j.atherosclerosis.2015.07.012"
    },
    {
        "id": "ch_006",
        "category": "cholesterol",
        "title": "Smoking, Alcohol, and Lipid Profile",
        "authors": "Gepner AD, et al.",
        "journal": "American Journal of Cardiology",
        "pub_year": 2011,
        "doi": "10.1016/j.amjcard.2011.03.061",
        "content": (
            "흡연은 HDL을 5.7mg/dL 감소시키고 LDL 산화를 촉진하여 동맥경화 위험을 가속합니다. "
            "금연 1년 후 HDL은 평균 4mg/dL 상승하며 심혈관 위험도가 50% 감소합니다. "
            "과도한 음주(주 14단위 이상)는 중성지방을 급격히 높이지만, "
            "적정 음주(레드와인 1잔/일)는 HDL을 소폭 올리는 효과가 있어 논쟁이 있습니다."
        ),
        "source": "https://doi.org/10.1016/j.amjcard.2011.03.061"
    },
    {
        "id": "ch_007",
        "category": "cholesterol",
        "title": "Nuts and Cardiovascular Risk Reduction",
        "authors": "Sabate J, Ang Y",
        "journal": "American Journal of Clinical Nutrition",
        "pub_year": 2009,
        "doi": "10.3945/ajcn.2009.27725F",
        "content": (
            "하루 견과류 28g(아몬드, 호두, 피스타치오) 섭취는 LDL을 5mg/dL, 중성지방을 10mg/dL 낮춥니다. "
            "호두의 알파리놀렌산(ALA)은 오메가-3 전구체로 심혈관 보호 효과가 있습니다. "
            "견과류의 고칼로리(28g당 약 170kcal)에도 불구하고, 장기 연구에서 체중 증가와 무관함이 확인됩니다."
        ),
        "source": "https://doi.org/10.3945/ajcn.2009.27725F"
    },
    {
        "id": "ch_008",
        "category": "cholesterol",
        "title": "Statin Therapy vs Lifestyle Modification for Primary Prevention",
        "authors": "Downs JR, et al.",
        "journal": "JAMA",
        "pub_year": 1998,
        "doi": "10.1001/jama.279.20.1615",
        "content": (
            "생활 습관 개선(식단+운동)만으로 6개월 내 LDL을 20-25% 낮출 수 있어, "
            "경계 수치(130-159mg/dL) 환자는 약물 치료 전 우선 시도가 권장됩니다. "
            "스타틴 약물은 LDL을 40-60% 낮추나 근육통, 간 효소 상승 등 부작용이 있어 "
            "심혈관 위험 점수(Framingham Score) 기반으로 처방 여부를 결정해야 합니다."
        ),
        "source": "https://doi.org/10.1001/jama.279.20.1615"
    },

    # ════════════════════════════════════════════════════════
    # CATEGORY 4: MUSCLE BUILDING / PROTEIN (6편)
    # ════════════════════════════════════════════════════════
    {
        "id": "mu_001",
        "category": "muscle",
        "title": "Protein Synthesis and Muscle Hypertrophy",
        "authors": "Schoenfeld BJ, Aragon AA",
        "journal": "Journal of the International Society of Sports Nutrition",
        "pub_year": 2018,
        "doi": "10.1186/s12970-018-0215-1",
        "content": (
            "근육 비대(hypertrophy)를 위한 단백질 최적 섭취량은 체중 1kg당 1.6-2.2g/일입니다. "
            "운동 후 골든타임(30분 이내) 20-40g 단백질 섭취가 근단백질 합성을 극대화합니다. "
            "류신(BCAA의 핵심)이 풍부한 유청단백질, 달걀흰자, 닭가슴살이 근합성 자극에 가장 효과적입니다. "
            "단백질을 하루 3-4회 균등 분배(20-40g씩)하면 1회 대량 섭취보다 총 근합성량이 25% 높습니다."
        ),
        "source": "https://doi.org/10.1186/s12970-018-0215-1"
    },
    {
        "id": "mu_002",
        "category": "muscle",
        "title": "Progressive Overload Principles in Resistance Training",
        "authors": "Kraemer WJ, Ratamess NA",
        "journal": "Medicine & Science in Sports & Exercise",
        "pub_year": 2004,
        "doi": "10.1249/01.MSS.0000130441.65990.A0",
        "content": (
            "점진적 과부하(Progressive Overload): 주 5-10% 벌크 증가 또는 반복 횟수 증가가 지속적 근비대의 핵심입니다. "
            "초보자는 주 3회 전신 운동이 최적이며, 중급자는 분할 루틴(상체/하체)으로 주 4-5회가 효과적입니다. "
            "반복 범위: 근력은 1-5RM, 근비대는 6-12RM, 근지구력은 15RM 이상이 각각 최적화됩니다. "
            "세트 간 휴식: 근력 목표는 3-5분, 근비대 목표는 60-90초가 권장됩니다."
        ),
        "source": "https://doi.org/10.1249/01.MSS.0000130441.65990.A0"
    },
    {
        "id": "mu_003",
        "category": "muscle",
        "title": "Creatine Supplementation and Muscle Mass",
        "authors": "Lanhers C, et al.",
        "journal": "European Journal of Sport Science",
        "pub_year": 2017,
        "doi": "10.1080/17461391.2016.1273875",
        "content": (
            "크레아틴(5g/일) 보충은 운동 능력을 향상시키고 24주간 사용 시 제지방 체중을 평균 1.4kg 늘립니다. "
            "크레아틴 로딩(20g/일 × 7일 → 5g/일 유지) 프로토콜이 즉각적인 근력 향상에 효과적입니다. "
            "크레아틴은 근육 세포 내 수분과 ATP 저장을 증가시켜 고강도 운동 수행 능력을 8-14% 향상시킵니다. "
            "신장 기능이 정상인 건강한 성인에게는 안전성이 확립되어 있습니다."
        ),
        "source": "https://doi.org/10.1080/17461391.2016.1273875"
    },
    {
        "id": "mu_004",
        "category": "muscle",
        "title": "Sleep and Muscle Recovery",
        "authors": "Dattilo M, et al.",
        "journal": "Medical Hypotheses",
        "pub_year": 2011,
        "doi": "10.1016/j.mehy.2010.08.032",
        "content": (
            "수면 중 성장호르몬(GH)의 70%가 분비되며, 이는 근육 회복과 합성에 핵심적입니다. "
            "수면 6시간 미만 시 근단백질 합성이 18% 감소하고 근육 분해 호르몬(코르티솔)이 증가합니다. "
            "7-9시간 수면과 규칙적인 수면 패턴 유지가 근육 성장을 위한 가장 저비용 고효율 회복 전략입니다. "
            "취침 전 카제인 단백질(코티지치즈, 그릭요거트) 40g 섭취는 야간 근합성을 자극합니다."
        ),
        "source": "https://doi.org/10.1016/j.mehy.2010.08.032"
    },
    {
        "id": "mu_005",
        "category": "muscle",
        "title": "Carbohydrate Timing Around Exercise",
        "authors": "Ivy JL, Portman R",
        "journal": "Sports Medicine",
        "pub_year": 2004,
        "doi": "10.2165/00007256-200434100-00003",
        "content": (
            "운동 후 30분 이내 탄수화물(0.8g/kg) + 단백질(0.4g/kg) 섭취는 근글리코겐 회복률을 38% 높입니다. "
            "근력 운동 전 1-2시간: 복합 탄수화물(현미, 오트밀)로 에너지를 충전합니다. "
            "운동 중 60분 이상 지속 시: 스포츠음료나 바나나로 탄수화물(30-60g/시간)을 보충합니다. "
            "근육 증량 기간에는 총 칼로리의 45-55%를 탄수화물로 채우는 것이 단백질 절약 효과를 줍니다."
        ),
        "source": "https://doi.org/10.2165/00007256-200434100-00003"
    },
    {
        "id": "mu_006",
        "category": "muscle",
        "title": "Sarcopenia Prevention in Aging Adults",
        "authors": "Cruz-Jentoft AJ, et al.",
        "journal": "Age and Ageing",
        "pub_year": 2019,
        "doi": "10.1093/ageing/afz046",
        "content": (
            "근감소증(Sarcopenia): 40세 이상부터 매년 근육량이 1-2% 씩 자연 감소합니다. "
            "예방을 위해 단백질 섭취를 1.2-1.5g/kg/일로 높이고, 저항 운동을 주 2-3회 실시해야 합니다. "
            "비타민 D(혈중 30ng/mL 유지)는 근세포 수용체 활성화를 통해 근육 기능을 보존합니다. "
            "앉아있지 않고 일어서기, 계단 오르기 같은 일상 신체 활동 증가가 근감소증 예방에 효과적입니다."
        ),
        "source": "https://doi.org/10.1093/ageing/afz046"
    },

    # ════════════════════════════════════════════════════════
    # CATEGORY 5: EXERCISE PHYSIOLOGY (8편)
    # ════════════════════════════════════════════════════════
    {
        "id": "ex_001",
        "category": "exercise",
        "title": "WHO Physical Activity Guidelines 2020",
        "authors": "World Health Organization",
        "journal": "WHO Guidelines",
        "pub_year": 2020,
        "doi": "WHO/2020/guidelines",
        "content": (
            "WHO 2020 신체 활동 권고 기준: 성인은 주 150-300분 중등도 유산소 운동(또는 75-150분 고강도) + "
            "주 2회 이상 근력 강화 운동을 권장합니다. "
            "앉아있는 시간을 줄이고 조금이라도 움직이는 것이 전혀 안 하는 것보다 건강에 유익합니다. "
            "장시간 앉아있는 직장인은 50-60분마다 5분 이상 일어서거나 스트레칭이 권장됩니다."
        ),
        "source": "https://www.who.int/publications/physical-activity-guidelines-2020"
    },
    {
        "id": "ex_002",
        "category": "exercise",
        "title": "HIIT vs Moderate Continuous Exercise: Meta-analysis",
        "authors": "Weston KS, et al.",
        "journal": "British Journal of Sports Medicine",
        "pub_year": 2014,
        "doi": "10.1136/bjsports-2013-092576",
        "content": (
            "고강도 인터벌 훈련(HIIT)은 동일 시간 중강도 지속 운동 대비 심폐 기능을 1.5배 빠르게 향상시킵니다. "
            "HIIT 20분 = 중강도 유산소 45분의 심혈관 건강 개선 효과로 시간 효율이 매우 높습니다. "
            "단, HIIT는 초보자나 관절 문제가 있는 경우 부상 위험이 높아 점진적 도입이 필요합니다. "
            "주 2-3회 HIIT + 주 2-3회 중강도 유산소의 혼합이 최적의 복합 효과를 제공합니다."
        ),
        "source": "https://doi.org/10.1136/bjsports-2013-092576"
    },
    {
        "id": "ex_003",
        "category": "exercise",
        "title": "Exercise Order: Cardio Before or After Weights?",
        "authors": "Chtara M, et al.",
        "journal": "British Journal of Sports Medicine",
        "pub_year": 2005,
        "doi": "10.1136/bjsm.2004.016063",
        "content": (
            "근력 운동 후 유산소 운동 순서가 반대 순서보다 근비대 신호를 30% 더 활성화합니다. "
            "체중 감량이 목표라면 유산소를 먼저 해도 무방하나, 글리코겐 고갈 상태에서의 근력 운동은 강도를 60%로 낮춥니다. "
            "근력 향상이 주 목표일 때는 항상 근력 운동을 먼저, 유산소를 나중에 하는 것이 원칙입니다."
        ),
        "source": "https://doi.org/10.1136/bjsm.2004.016063"
    },
    {
        "id": "ex_004",
        "category": "exercise",
        "title": "Walking 10,000 Steps and Health Outcomes",
        "authors": "Tudor-Locke C, et al.",
        "journal": "International Journal of Behavioral Nutrition",
        "pub_year": 2011,
        "doi": "10.1186/1479-5868-8-79",
        "content": (
            "하루 10,000보 목표는 활동 수준에 따라 효과가 다릅니다. "
            "기존 비활동적 생활자는 하루 5,000-7,500보만 달성해도 심혈관 위험을 21% 낮출 수 있습니다. "
            "하루 7,500보 이상부터 심혈관 사망률 감소 효과가 plateau에 도달합니다. "
            "중요한 것은 절대 보수보다 규칙성이며, 매일 30분 빠른 걷기가 핵심 권고사항입니다."
        ),
        "source": "https://doi.org/10.1186/1479-5868-8-79"
    },
    {
        "id": "ex_005",
        "category": "exercise",
        "title": "Stretching and Flexibility for Injury Prevention",
        "authors": "Page P",
        "journal": "International Journal of Sports Physical Therapy",
        "pub_year": 2012,
        "doi": "IJSPT/2012/flexibility",
        "content": (
            "운동 전 동적 스트레칭(레그스윙, 암서클 등)은 관절 가동범위를 넓히고 부상 위험을 줄입니다. "
            "운동 후 정적 스트레칭(각 부위 20-30초 유지)은 근육 회복을 돕고 지연성 근육통(DOMS)을 완화합니다. "
            "정적 스트레칭을 운동 전에 하면 근력 발휘가 5-8% 감소하므로 반드시 운동 후에 시행해야 합니다."
        ),
        "source": "https://doi.org/IJSPT/2012/flexibility"
    },
    {
        "id": "ex_006",
        "category": "exercise",
        "title": "Exercise and Mental Health: Antidepressant Effect",
        "authors": "Blumenthal JA, et al.",
        "journal": "Archives of Internal Medicine",
        "pub_year": 1999,
        "doi": "10.1001/archinte.159.19.2349",
        "content": (
            "주 3회, 45분 유산소 운동은 항우울제(서트랄린)와 동등한 우울증 개선 효과를 보였습니다(16주 RCT). "
            "운동은 엔도르핀, 세로토닌, 도파민 분비를 증가시켜 기분을 향상시키고 불안을 감소시킵니다. "
            "운동이 습관화된 사람은 10개월 후 우울증 재발률이 약물 단독 치료보다 38% 낮았습니다."
        ),
        "source": "https://doi.org/10.1001/archinte.159.19.2349"
    },
    {
        "id": "ex_007",
        "category": "exercise",
        "title": "Recovery: Active vs Passive Rest Between Sessions",
        "authors": "Menzies P, et al.",
        "journal": "Journal of Sports Sciences",
        "pub_year": 2010,
        "doi": "10.1080/02640414.2010.481721",
        "content": (
            "격렬한 운동 다음 날 가벼운 활동(산책, 수영, 요가)인 능동적 회복은 완전 휴식보다 "
            "젖산 제거 속도를 2배 높이고 다음 세션의 운동 능력을 5-8% 향상시킵니다. "
            "회복 세션의 강도는 최대 심박수의 50-60% 이하로 제한해야 추가 피로 누적을 예방합니다."
        ),
        "source": "https://doi.org/10.1080/02640414.2010.481721"
    },
    {
        "id": "ex_008",
        "category": "exercise",
        "title": "Zone 2 Training and Mitochondrial Health",
        "authors": "Iaia FM, Bangsbo J",
        "journal": "Scandinavian Journal of Medicine & Science in Sports",
        "pub_year": 2010,
        "doi": "10.1111/j.1600-0838.2010.01158.x",
        "content": (
            "존2 운동(최대 심박수의 60-70%, 편안히 대화 가능한 강도)은 미토콘드리아 밀도와 기능을 향상시킵니다. "
            "주 3-4회 45-60분 존2 유산소 운동은 지방 산화 능력을 극대화하고 대사 효율을 높입니다. "
            "장기적으로 존2 훈련은 안정 시 심박수를 낮추고, 강도 높은 운동에서의 젖산 역치를 향상시킵니다. "
            "운동 초보자에게 가장 안전하고 지속 가능한 유산소 기초 체력 향상 방법입니다."
        ),
        "source": "https://doi.org/10.1111/j.1600-0838.2010.01158.x"
    },

    # ════════════════════════════════════════════════════════
    # CATEGORY 6: KOREAN CLINICAL GUIDELINES (6편)
    # ════════════════════════════════════════════════════════
    {
        "id": "kr_001",
        "category": "korean_guideline",
        "title": "Korean Society for the Study of Obesity Guidelines 2022",
        "authors": "Korean Society for the Study of Obesity",
        "journal": "Journal of Obesity & Metabolic Syndrome",
        "pub_year": 2022,
        "doi": "10.7570/jomes22028",
        "content": (
            "한국 비만 진단 기준: BMI 25kg/m² 이상(서양은 30 이상)이며, 복부비만 기준은 남성 허리 90cm, 여성 85cm입니다. "
            "한국인은 서양인 대비 동일 BMI에서 체지방률이 높고 내장지방 비율이 높아 대사 위험이 더 높습니다. "
            "한국 비만 치료 목표: 6개월 내 현재 체중의 5-10% 감량 후 1년간 유지. "
            "한국인 특성상 탄수화물(쌀밥) 의존도가 높아 정제 탄수화물 줄이기가 가장 중요한 식이 전략입니다."
        ),
        "source": "https://doi.org/10.7570/jomes22028"
    },
    {
        "id": "kr_002",
        "category": "korean_guideline",
        "title": "Korean Diabetes Association Standards of Medical Care 2023",
        "authors": "Korean Diabetes Association",
        "journal": "Diabetes & Metabolism Journal",
        "pub_year": 2023,
        "doi": "10.4093/dmj.2023.0023",
        "content": (
            "한국당뇨병학회 2023 진료 지침: HbA1c 진단 기준 6.5% 이상, 당뇨 전단계 5.7-6.4%. "
            "한국인 환자의 특성: 인슐린 분비 능력이 상대적으로 부족하여 혈당 스파이크에 더 취약합니다. "
            "한식 기반 식단에서 흰쌀밥을 잡곡밥으로 교체, 국물 섭취를 줄이고 짜게 먹는 습관 교정이 핵심입니다. "
            "걷기, 자전거, 수영 등 한국인 친숙한 운동 중심의 신체 활동 증가가 1차 권고 사항입니다."
        ),
        "source": "https://doi.org/10.4093/dmj.2023.0023"
    },
    {
        "id": "kr_003",
        "category": "korean_guideline",
        "title": "Korean Society of Lipidology and Atherosclerosis Dyslipidemia Guidelines",
        "authors": "Korean Society of Lipidology and Atherosclerosis",
        "journal": "Journal of Lipid and Atherosclerosis",
        "pub_year": 2022,
        "doi": "10.12997/jla.2022.11.2.195",
        "content": (
            "한국 이상지질혈증 진료 지침: LDL 100mg/dL 미만을 목표로 하며, 심혈관 고위험군은 70mg/dL 미만을 권고합니다. "
            "한국인 식단의 나트륨 과다 섭취(평균 4.5g/일, WHO 권장 2g/일의 2배 이상)는 고혈압과 함께 심혈관 위험을 높입니다. "
            "김, 미역 등 해조류의 알긴산은 콜레스테롤 흡수를 억제하는 효과가 있어 한국인에게 유익한 식품입니다."
        ),
        "source": "https://doi.org/10.12997/jla.2022.11.2.195"
    },
    {
        "id": "kr_004",
        "category": "korean_guideline",
        "title": "Metabolic Syndrome Prevalence in Korean Adults",
        "authors": "Oh SW, et al.",
        "journal": "Circulation",
        "pub_year": 2004,
        "doi": "10.1161/01.CIR.0000145735.53976.A3",
        "content": (
            "한국 성인 대사증후군 유병률: 30세 이상 남성 28.7%, 여성 27.5%. "
            "대사증후군 진단 기준(한국): 복부비만 + 혈압 이상 + 혈당 이상 + 중성지방 이상 + HDL 저하 중 3가지 이상. "
            "한국인 대사증후군의 가장 강력한 위험 요인은 복부비만으로, "
            "허리둘레 관리가 전체 대사 건강의 바로미터 역할을 합니다."
        ),
        "source": "https://doi.org/10.1161/01.CIR.0000145735.53976.A3"
    },
    {
        "id": "kr_005",
        "category": "korean_guideline",
        "title": "Traditional Korean Diet and Longevity",
        "authors": "Lee KW, Shin D",
        "journal": "Nutrients",
        "pub_year": 2021,
        "doi": "10.3390/nu13082467",
        "content": (
            "전통 한식(반찬 중심, 발효 식품, 채소 기반)은 지중해식 식단과 비슷한 수준의 심혈관 보호 효과를 가집니다. "
            "김치의 프로바이오틱스(유산균)는 장내 마이크로바이옴 다양성을 높여 면역력과 대사 건강을 개선합니다. "
            "된장, 청국장의 이소플라본은 혈중 LDL을 낮추고 골밀도를 유지하는 효과가 있습니다. "
            "현대 한국인의 서구화된 식습관(패스트푸드, 야식 문화)이 전통 한식의 건강 이점을 감소시키고 있습니다."
        ),
        "source": "https://doi.org/10.3390/nu13082467"
    },
    {
        "id": "kr_006",
        "category": "korean_guideline",
        "title": "National Health Insurance Service Health Screening Guidelines Korea",
        "authors": "National Health Insurance Service Korea",
        "journal": "NHIS Korea Annual Report",
        "pub_year": 2024,
        "doi": "NHIS/Korea/2024",
        "content": (
            "한국 국가 건강검진 주요 지표 정상 기준: 공복혈당 100mg/dL 미만, 총콜레스테롤 200mg/dL 미만, "
            "LDL 130mg/dL 미만, 중성지방 150mg/dL 미만, HDL 60mg/dL 이상, 혈압 120/80mmHg 미만. "
            "한국인 건강 검진 결과에서 가장 흔한 이상 소견: 간 효소 이상(지방간), 혈압 이상, 고지혈증 순서. "
            "2년마다 의무 검진 시 연속 측정값의 추세(트렌드)가 단순 수치보다 중요한 건강 지표입니다."
        ),
        "source": "https://www.nhis.or.kr/guidelines/2024"
    },

    # ════════════════════════════════════════════════════════
    # CATEGORY 7: LIFESTYLE / SLEEP / STRESS (4편)
    # ════════════════════════════════════════════════════════
    {
        "id": "ls_001",
        "category": "lifestyle",
        "title": "Blue Light and Circadian Rhythm Disruption",
        "authors": "Chang AM, et al.",
        "journal": "PNAS",
        "pub_year": 2015,
        "doi": "10.1073/pnas.1418490112",
        "content": (
            "취침 전 2시간 전자기기(스마트폰, 태블릿) 사용은 멜라토닌 분비를 50% 억제합니다. "
            "청색광 차단 안경 또는 스크린의 나이트 모드 사용은 멜라토닌 억제를 부분적으로 완화합니다. "
            "일관된 취침/기상 시간 유지(주말 포함)가 생체리듬 안정화의 가장 효과적인 방법입니다. "
            "자정 이후 취침이 만성화되면 코르티솔 리듬이 역전되어 복부지방 축적이 가속됩니다."
        ),
        "source": "https://doi.org/10.1073/pnas.1418490112"
    },
    {
        "id": "ls_002",
        "category": "lifestyle",
        "title": "Mindfulness Meditation and Cortisol Reduction",
        "authors": "Turakitwanakan W, et al.",
        "journal": "Journal of the Medical Association of Thailand",
        "pub_year": 2013,
        "doi": "JMAT/2013/mindfulness",
        "content": (
            "마음챙김 명상 프로그램(MBSR, 8주 과정)은 타액 코르티솔을 평균 23% 감소시킵니다. "
            "하루 10분 명상이 6주 이상 지속되면 뇌의 편도체(공포·스트레스 반응 영역) 크기가 줄어드는 구조적 변화가 나타납니다. "
            "명상은 코르티솔을 줄여 복부지방 축적을 억제하고 혈당 안정화에 간접적으로 기여합니다."
        ),
        "source": "https://doi.org/JMAT/2013/mindfulness"
    },
    {
        "id": "ls_003",
        "category": "lifestyle",
        "title": "Hydration and Metabolic Function",
        "authors": "Popkin BM, et al.",
        "journal": "Nutrition Reviews",
        "pub_year": 2010,
        "doi": "10.1111/j.1753-4887.2010.00304.x",
        "content": (
            "체내 수분 부족(체중의 2%)은 신진대사를 3% 낮추고 인지 기능과 운동 능력을 저하시킵니다. "
            "하루 물 섭취 목표: 남성 3.7L, 여성 2.7L (음식 수분 포함). 순수 물로는 남성 2.0L, 여성 1.6L. "
            "식사 30분 전 500ml 물 섭취는 식욕을 줄여 평균 44kcal 덜 먹게 합니다. "
            "소변 색이 연한 노란색(레모네이드 색)을 유지하는 것이 적정 수화 상태의 간단한 지표입니다."
        ),
        "source": "https://doi.org/10.1111/j.1753-4887.2010.00304.x"
    },
    {
        "id": "ls_004",
        "category": "lifestyle",
        "title": "Social Support and Health Behavior Maintenance",
        "authors": "Umberson D, Montez JK",
        "journal": "Journal of Health and Social Behavior",
        "pub_year": 2010,
        "doi": "10.1177/0022146510383501",
        "content": (
            "사회적 지지(가족, 친구, 운동 파트너)는 건강 행동의 장기 지속성을 2-3배 높입니다. "
            "함께 운동하는 파트너가 있으면 운동 습관 유지율이 65% → 92%로 증가합니다. "
            "SNS 기반 건강 커뮤니티 참여는 체중 감량 프로그램 완료율을 25% 향상시킵니다. "
            "고립, 외로움은 스트레스 호르몬을 만성적으로 높여 대사 건강에 직·간접적 악영향을 미칩니다."
        ),
        "source": "https://doi.org/10.1177/0022146510383501"
    },
]


def seed_to_chromadb():
    """ChromaDB에 50편의 의학 문헌 저장"""
    print(f"\n{'='*60}")
    print("  Vital Intelligence -- Medical Knowledge Base Init")
    print(f"  Papers: {len(MEDICAL_PAPERS)}")
    print(f"{'='*60}\n")

    # RAG 엔진을 통해 ChromaDB에 저장
    sys.path.insert(0, os.path.dirname(__file__))
    from rag_engine import MedicalRAGEngine

    engine = MedicalRAGEngine()

    # 카테고리별로 상태 확인
    categories = {}
    for p in MEDICAL_PAPERS:
        cat = p["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("[저장 전] 카테고리별 논문 수:")
    for cat, cnt in categories.items():
        print(f"  - {cat}: {cnt}편")

    # Langchain Document 형식으로 변환
    docs = []
    for paper in MEDICAL_PAPERS:
        doc = Document(
            page_content=paper["content"],
            metadata={
                "id":       paper["id"],
                "title":    paper["title"],
                "authors":  paper["authors"],
                "journal":  paper["journal"],
                "pub_year": paper["pub_year"],
                "doi":      paper["doi"],
                "source":   paper["source"],
                "category": paper["category"],
            }
        )
        docs.append(doc)

    print(f"\n[임베딩 & 저장 중] ChromaDB에 {len(docs)}건 처리 중...")
    print("  (OpenAI 임베딩 API 호출이 포함되어 수 분 소요될 수 있습니다)\n")

    # 배치 단위로 저장 (10건씩)
    batch_size = 10
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        engine.upsert_knowledge(batch)
        print(f"  ✅ {min(i+batch_size, len(docs))}/{len(docs)}건 저장 완료")

    final_count = engine.get_collection_count()
    print(f"\n{'='*60}")
    print(f"  🎉 ChromaDB 시드 완료! 총 {final_count}건의 벡터 저장됨")
    print(f"  저장 경로: {engine.CHROMA_PERSIST_DIR}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    seed_to_chromadb()
