import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# =========================
# 페이지 설정
# =========================

st.set_page_config(
    page_title="농림수산물 무역 예측 시스템",
    page_icon="📊",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.title {
    text-align:center;
    color:#1f4e79;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 데이터 불러오기
# =========================

df = pd.read_csv("exim.csv")

# =========================
# 제목
# =========================

st.markdown(
    "<h1 class='title'>📊 경상남도 농림수산물 무역 예측 시스템</h1>",
    unsafe_allow_html=True
)

st.markdown("""
### 🔍 시스템 소개

본 시스템은 2010년~2022년 경상남도 농림수산물 수출입 데이터를 학습하여

- 미래 수출액 예측
- 미래 수입액 예측
- 미래 무역수지 예측
- 흑자·적자 여부 분석

을 수행합니다.
""")

# =========================
# 연도별 총합 계산
# =========================

years = []
exports = []
imports = []

for y in range(2010, 2023):

    ex_col = f"{y}수출"
    im_col = f"{y}수입"

    if ex_col in df.columns and im_col in df.columns:

        total_export = pd.to_numeric(
            df[ex_col],
            errors="coerce"
        ).fillna(0).sum()

        total_import = pd.to_numeric(
            df[im_col],
            errors="coerce"
        ).fillna(0).sum()

        years.append(y)
        exports.append(total_export)
        imports.append(total_import)

# =========================
# 실제 데이터 그래프
# =========================

st.markdown("---")
st.subheader("📈 2010~2022 수출입 추세")

chart_df = pd.DataFrame({
    "연도": years,
    "수출액": exports,
    "수입액": imports
})

st.line_chart(
    chart_df.set_index("연도"),
    use_container_width=True
)

# =========================
# 머신러닝 학습
# =========================

X = np.array(years).reshape(-1, 1)

export_model = LinearRegression()
export_model.fit(X, exports)

import_model = LinearRegression()
import_model.fit(X, imports)

# =========================
# 미래 예측
# =========================

st.markdown("---")
st.subheader("🔮 미래 무역 예측")

future_year = st.number_input(
    "예측할 연도를 입력하세요",
    min_value=2023,
    max_value=2050,
    value=2025,
    step=1
)

if st.button(
    "🚀 미래 무역 예측",
    use_container_width=True
):

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

    st.markdown("---")
    st.subheader(f"📊 {future_year}년 예측 결과")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 예상 수출액",
            f"{predicted_export:,.0f} 달러"
        )

    with col2:
        st.metric(
            "🛒 예상 수입액",
            f"{predicted_import:,.0f} 달러"
        )

    with col3:
        st.metric(
            "📈 예상 무역수지",
            f"{predicted_balance:,.0f} 달러"
        )

    st.markdown("---")

    if predicted_balance > 0:

        st.success(
            f"""
            📈 {future_year}년은 무역흑자가 예상됩니다.

            예상 무역수지:
            {predicted_balance:,.0f} 달러
            """
        )

    elif predicted_balance < 0:

        st.error(
            f"""
            📉 {future_year}년은 무역적자가 예상됩니다.

            예상 무역수지:
            {predicted_balance:,.0f} 달러
            """
        )

    else:

        st.info(
            f"""
            ⚖️ {future_year}년은 수출과 수입이
            거의 동일할 것으로 예상됩니다.
            """
        )

    # =========================
    # 예측 포함 그래프
    # =========================

    future_years = list(range(2023, future_year + 1))

    future_exports = [
        export_model.predict([[y]])[0]
        for y in future_years
    ]

    future_imports = [
        import_model.predict([[y]])[0]
        for y in future_years
    ]

    graph_years = years + future_years

    graph_exports = exports + future_exports
    graph_imports = imports + future_imports

    prediction_df = pd.DataFrame({
        "연도": graph_years,
        "수출액": graph_exports,
        "수입액": graph_imports
    })

    st.markdown("---")
    st.subheader("📉 실제 데이터 + 미래 예측")

    st.line_chart(
        prediction_df.set_index("연도"),
        use_container_width=True
    )
