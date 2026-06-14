import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

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

# 데이터 불러오기
df = pd.read_csv("exim.csv")

# 제목
st.markdown(
    "<h1 class='title'>📊 연도별 농림수산물 수출입 분석 시스템</h1>",
    unsafe_allow_html=True
)

st.markdown("""
### 🔍 조회 안내

2010년 ~ 2022년 사이의 연도를 선택하면

- 총 수출액
- 총 수입액
- 시군별 현황
- 미래 무역 예측

을 확인할 수 있습니다.
""")

# 연도 선택
year = st.selectbox(
    "조회할 연도 선택",
    [str(i) for i in range(2010, 2023)]
)

# 컬럼명 생성
ex_col = f"{year}수출"
im_col = f"{year}수입"

# 분석 버튼
if st.button("📈 분석 시작", use_container_width=True):

    if ex_col not in df.columns or im_col not in df.columns:
        st.error(f"{year}년 데이터가 존재하지 않습니다.")

    else:

        # 해당 연도 데이터 추출
        year_df = df[['행정구역(시군)별(1)', ex_col, im_col]].copy()
        year_df.columns = ['행정구역', '수출액', '수입액']

        # 숫자 변환
        year_df['수출액'] = pd.to_numeric(
            year_df['수출액'],
            errors='coerce'
        ).fillna(0)

        year_df['수입액'] = pd.to_numeric(
            year_df['수입액'],
            errors='coerce'
        ).fillna(0)

        # 총합 계산
        total_export = year_df['수출액'].sum()
        total_import = year_df['수입액'].sum()

        # KPI
        st.markdown("---")
        st.subheader(f"🎯 {year}년 경상남도 농림수산물 무역 실적")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "💰 총 수출액",
                f"{total_export:,.0f}"
            )

        with col2:
            st.metric(
                "🛒 총 수입액",
                f"{total_import:,.0f}"
            )

        # 표
        st.markdown("---")
        st.subheader("🏙️ 시군별 세부 현황")

        st.dataframe(
            year_df,
            use_container_width=True,
            height=500
        )

        # ======================
        # 미래 무역 예측 모델
        # ======================

        years = []
        exports = []
        imports = []

        for y in range(2010, 2023):

            ex_model = f"{y}수출"
            im_model = f"{y}수입"

            if ex_model in df.columns and im_model in df.columns:

                total_ex = pd.to_numeric(
                    df[ex_model],
                    errors='coerce'
                ).fillna(0).sum()

                total_im = pd.to_numeric(
                    df[im_model],
                    errors='coerce'
                ).fillna(0).sum()

                years.append(y)
                exports.append(total_ex)
                imports.append(total_im)

        X = np.array(years).reshape(-1, 1)

        export_model = LinearRegression()
        export_model.fit(X, exports)

        import_model = LinearRegression()
        import_model.fit(X, imports)

        # ======================
        # 예측 UI
        # ======================

        st.markdown("---")
        st.subheader("🔮 미래 무역 예측")

        future_year = st.number_input(
            "예측할 연도를 입력하세요",
            min_value=2023,
            max_value=2050,
            value=2025
        )

        if st.button("🚀 미래 무역 예측"):

            predicted_export = export_model.predict(
                [[future_year]]
            )[0]

            predicted_import = import_model.predict(
                [[future_year]]
            )[0]

            predicted_balance = (
                predicted_export
                - predicted_import
            )

            st.markdown("### 📈 예측 결과")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "예상 수출액",
                    f"{predicted_export:,.0f}"
                )

            with col2:
                st.metric(
                    "예상 수입액",
                    f"{predicted_import:,.0f}"
                )

            with col3:
                st.metric(
                    "예상 무역수지",
                    f"{predicted_balance:,.0f}"
                )

            st.markdown("---")

            if predicted_balance > 0:

                st.success(
                    f"""
                    📈 {future_year}년은 무역흑자가 예상됩니다.

                    예상 무역수지:
                    {predicted_balance:,.0f}
                    """
                )

            elif predicted_balance < 0:

                st.error(
                    f"""
                    📉 {future_year}년은 무역적자가 예상됩니다.

                    예상 무역수지:
                    {predicted_balance:,.0f}
                    """
                )

            else:

                st.info(
                    f"""
                    ⚖️ {future_year}년은 수출과 수입이
                    거의 동일할 것으로 예상됩니다.
                    """
                )
