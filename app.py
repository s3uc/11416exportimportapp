import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(
    page_title="농림수산물 수출입 분석",
    page_icon="📊",
    layout="wide"
)

# CSS 디자인
st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}

.title {
    text-align:center;
    color:#1f4e79;
}

.analysis-box {
    background-color:#eef6ff;
    padding:20px;
    border-radius:15px;
    border-left:6px solid #1f77b4;
}
</style>
""", unsafe_allow_html=True)



exim = "exim.csv" 
df = pd.read_csv("exim.csv")



st.markdown("<h1 class='title'>📊 연도별 농림수산물 수출입 분석 시스템</h1>", unsafe_allow_html=True)

st.markdown("""
### 🔍 조회 안내
2010년 ~ 2022년 사이의 연도를 선택하면

- 총 수출액
- 총 수입액
- 무역수지
- 시군별 현황
- AI 분석 코멘트

를 확인할 수 있습니다.
""")

# 연도 선택
year = st.selectbox(
    "조회할 연도 선택",
    [str(i) for i in range(2010, 2023)]
)

# 변수 사전 선언 (NameError 원천 차단)
ex_col = f"{year}수출"
im_col = f"{year}수입"


# 2. 분석 시작 메인 블록 (모든 들여쓰기를 4칸 스페이스로 완벽히 통일했습니다)
if st.button("📈 분석 시작", use_container_width=True):
    
    if ex_col not in df.columns or im_col not in df.columns:
        st.error(f"{year}년 데이터가 존재하지 않습니다.")
    else:
        year_df = df[['행정구역(시군)별(1)', ex_col, im_col]].copy()
        year_df.columns = ['행정구역', '수출액', '수입액']
        year_df['무역수지'] = year_df['수출액'] - year_df['수입액']
        
        # 원본에서 깨져있던 람다 함수 구문을 한 줄로 깔끔하게 처리했습니다.
        year_df['상태'] = year_df['무역수지'].apply(lambda x: "🟢 흑자" if x >= 0 else "🔴 적자")

        # 요약 계산
        total_export = year_df['수출액'].sum()
        total_import = year_df['수입액'].sum()
        trade_balance = total_export - total_import

        st.markdown("---")
        st.subheader(f"🎯 {year}년 경상남도 농림수산물 무역 실적")

        # KPI 카드
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💰 총 수출액",
                f"{total_export:,.0f} 달러"
            )

        with col2:
            st.metric(
                "🛒 총 수입액",
                f"{total_import:,.0f} 달러"
            )

        with col3:
            st.metric(
                "📊 무역수지",
                f"{trade_balance:,.0f} 달러"
            )

        st.markdown("---")

        # 데이터 테이블
        st.subheader("🏙️ 시군별 세부 현황")

        st.dataframe(
            year_df,
            use_container_width=True,
            height=500


        # AI 분석
        max_import_city = year_df.sort_values(by='수입액', ascending=False).iloc[0]['행정구역']
        max_export_city = year_df.sort_values(by='수출액', ascending=False).iloc[0]['행정구역']

        st.markdown("---")
        st.subheader("🤖 AI 경제 분석")

        with st.container():
            st.markdown(
                f"""
                <div class="analysis-box">
                <h4>📌 {year}년 분석 결과</h4>
                <b>① 최대 수입 지역</b><br>
                ▶ <b>{max_import_city}</b>이(가) 가장 많은 농림수산물을 수입했습니다.<br>
                해외 공급망과 국제 가격 변동의 영향을 크게 받을 가능성이 있습니다.
                <br><br>
                <b>② 최대 수출 지역</b><br>
                ▶ <b>{max_export_city}</b>이(가) 가장 많은 수출을 기록했습니다.<br>
                지역 경제 활성화와 외화 획득에 중요한 역할을 수행했습니다.
                <br><br>
                <b>③ 종합 평가</b><br>
                </div>
                """,
                unsafe_allow_html=True
            )

            if trade_balance < 0:
                st.warning(
                    f"{year}년은 수입이 수출보다 많아 무역적자를 기록했습니다.\n\n"
                    "고물가 상황에서 지역 내 생산 확대와 유통 효율화 정책이 필요합니다."
                )
            else:
                st.success(
                    f"{year}년은 수출이 수입보다 많아 무역흑자를 기록했습니다.\n\n"
                    "지역 농림수산업의 경쟁력이 높은 시기로 평가할 수 있습니다."
                )

        st.balloons()
