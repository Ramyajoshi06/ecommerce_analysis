import streamlit as st
import pandas as pd

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ecommerce Customer Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
html, body, [class*="css"] {
    font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
}
[data-testid="stSidebar"] {
    background: #111827 !important;
}
[data-testid="stSidebar"] .stButton button {
    width: 100%;
}
@keyframes page-fade-slide-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.page-transition {
  animation: page-fade-slide-in 0.28s ease-out both;
}
</style>
""",
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════
df = pd.read_csv("ecommerce_user_dataset.csv")
rows, cols = df.shape
missing = int(df.isnull().sum().sum())
dup_count = int(df.duplicated().sum())

numeric_cols = [
    col for col in df.columns
    if col not in ["Customer_ID", "Customer_Segment"] and pd.api.types.is_numeric_dtype(df[col])
]

def safe_numeric_rule_count(series: pd.Series, lo=None, hi=None):
    if lo is not None and hi is not None:
        return int(((series < lo) | (series > hi)).sum())
    if lo is not None:
        return int((series < lo).sum())
    if hi is not None:
        return int((series > hi).sum())
    return 0

numeric_rules = {
    "Purchase_History": (0, 100),
    "Transaction_Frequency": (0, 50),
    "Monetary_Value": (0, None),
    "Browsing_Behavior": (0, 100),
    "Engagement_Score": (0, 1),
    "Time_on_Site": (0, 100),
}
invalid_rows = {}
for col, (lo, hi) in numeric_rules.items():
    invalid_rows[col] = safe_numeric_rule_count(df[col], lo=lo, hi=hi)

total_invalid_numeric = sum(invalid_rows.values())

categorical_rules = {"Customer_Segment": {"Copp", "Iron"}}
invalid_cat = {}
for col, valid_set in categorical_rules.items():
    invalid_cat[col] = int((~df[col].isin(valid_set)).sum())

total_invalid_categorical = sum(invalid_cat.values())

# IQR outlier counts for numeric variables
outlier_rows = []
for col in numeric_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    count = int(((df[col] < lower) | (df[col] > upper)).sum())
    outlier_rows.append(
        {
            "Column": col,
            "Q1": float(q1),
            "Q3": float(q3),
            "Outlier count": count,
            "Lower fence": float(lower),
            "Upper fence": float(upper),
        }
    )
outlier_df = pd.DataFrame(outlier_rows)
total_outliers = int(outlier_df["Outlier count"].sum())

avg_monetary = float(df["Monetary_Value"].mean())
median_monetary = float(df["Monetary_Value"].median())
avg_engagement = float(df["Engagement_Score"].mean())
avg_time = float(df["Time_on_Site"].mean())
avg_browsing = float(df["Browsing_Behavior"].mean())

# ══════════════════════════════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def page_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
<div style="margin-bottom: 0.9rem;">
  <div style="font-size:1.4rem; font-weight:700; color:#f3f4f6; letter-spacing:-0.02em; line-height:1.2;">{title}</div>
  <div style="font-size:0.78rem; color:#9ca3af; margin-top:0.2rem;">{subtitle}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def section_title(text: str) -> None:
    st.markdown(
        f"""
<div style="font-size:0.72rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase; color:#9ca3af; margin: 1.0rem 0 0.5rem;">{text}</div>
""",
        unsafe_allow_html=True,
    )


def kpi_card(col, label: str, value: str, sub: str) -> None:
    col.markdown(
        f"""
<div style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px; padding:0.95rem 1.0rem 0.85rem; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
  <div style="font-size:0.64rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; color:#9ca3af; margin-bottom:0.28rem;">{label}</div>
  <div style="font-size:1.65rem; font-weight:800; color:#111827; line-height:1.05; letter-spacing:-0.02em;">{value}</div>
  <div style="font-size:0.66rem; color:#9ca3af; margin-top:0.2rem;">{sub}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def simple_hist_chart(series: pd.Series, title: str, color: str) -> None:
    tmp = series.value_counts().sort_index()
    tmp_df = tmp.reset_index()
    tmp_df.columns = [series.name, "count"]
    chart = tmp_df.set_index(series.name)
    st.markdown(
        f"<div style='font-size:0.78rem; font-weight:800; text-transform:uppercase; color:#6b7280; margin-bottom:0.35rem;'>{title}</div>",
        unsafe_allow_html=True,
    )
    st.bar_chart(chart, use_container_width=True, color=color)


PAGES = [
    ("Overview", "📊 Overview"),
    ("Customer Behavior", "🛍️ Customer Behavior"),
    ("Segment Analysis", "📊 Segment Analysis"),
    ("Key Insights", "💡 Key Insights"),
    ("Data Quality", "🔍 Data Quality"),
]

if "page" not in st.session_state:
    st.session_state.page = "📊 Overview"

with st.sidebar:
    st.markdown(
        """
<div style="padding: 0.7rem 0.9rem 0.4rem;">
  <div style="font-size:1.05rem; font-weight:700; color:#f9fafb; letter-spacing:-0.01em;">🛒 Ecommerce Analytics</div>
  <div style="font-size:0.65rem; color:#6b7280; margin-top:0.06rem; letter-spacing:0.02em;">ecommerce_user_dataset.csv · 1,000 records</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border:none;border-top:1px solid #1f2937;margin:0.15rem 0 0.55rem;' />", unsafe_allow_html=True)

    current_group = None
    group_labels = {"Spend": "SPEND", "Behavior": "BEHAVIOR", "Data": "DATA"}
    page_to_group = {
        "📊 Overview": "Spend",
        "🛍️ Customer Behavior": "Behavior",
        "📊 Segment Analysis": "Behavior",
        "💡 Key Insights": "Spend",
        "🔍 Data Quality": "Data",
    }

    for label, page_key in PAGES:
        group = page_to_group.get(page_key, "Spend")
        if group != current_group:
            current_group = group
            st.markdown(f"<div class='sb-section'>{group_labels[group]}</div>", unsafe_allow_html=True)

        is_active = st.session_state.page == page_key
        btn_type = "primary" if is_active else "secondary"

        if st.button(
            f"{label}",
            key=f"nav_{page_key}",
            type=btn_type,
            use_container_width=True,
        ):
            st.session_state.page = page_key
            st.rerun()

page = st.session_state.page

st.markdown("<div class='page-transition'>", unsafe_allow_html=True)

if page == "📊 Overview":
    page_header("Ecommerce Customer Analytics", "Quick snapshot of customer value and engagement")

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, "Customers", f"{rows:,}", "records")
    kpi_card(c2, "Avg Spend", f"${avg_monetary:,.2f}", "per customer")
    kpi_card(c3, "Median Spend", f"${median_monetary:,.2f}", "per customer")
    kpi_card(c4, "Avg Time", f"{avg_time:.1f} min", "on site")
    kpi_card(c5, "Duplicates", f"{dup_count:,}", "exact rows")

    st.markdown("<hr style='border:none;border-top:1px solid #e5e7eb;margin:1.1rem 0;' />", unsafe_allow_html=True)

    left, right = st.columns([3, 2])
    with left:
        section_title("Monetary value distribution")
        bins = pd.cut(df["Monetary_Value"], bins=[0, 1000, 3000, 5000, 8000, 12000], right=False)
        bucket_counts = bins.value_counts(sort=False).reset_index()
        bucket_counts.columns = ["Spend range", "Count"]
        bucket_counts["Spend range"] = bucket_counts["Spend range"].astype(str)
        st.bar_chart(bucket_counts.set_index("Spend range"), use_container_width=True)

    with right:
        st.info(
            f"Missing values: {missing}. Outlier rows (IQR): {total_outliers:,}. "
            f"Valid customer segments: {rows - invalid_cat['Customer_Segment']:,}/{rows:,}."
        )

elif page == "🛍️ Customer Behavior":
    page_header("Customer Behavior", "Patterns in spending, browsing, and engagement")

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, "Avg Transaction", f"{df['Transaction_Frequency'].mean():.2f}", "freq")
    kpi_card(c2, "Avg Browse", f"{avg_browsing:.1f}%", "behavior")
    kpi_card(c3, "Avg Engagement", f"{avg_engagement:.2f}", "score")
    kpi_card(c4, "Avg Site Time", f"{avg_time:.1f}", "minutes")

    st.markdown("<hr style='border:none;border-top:1px solid #e5e7eb;margin:1.1rem 0;' />", unsafe_allow_html=True)

    colA, colB = st.columns(2)
    with colA:
        section_title("Monetary value")
        st.bar_chart(df["Monetary_Value"].value_counts().sort_index(), use_container_width=True)
    with colB:
        section_title("Browsing behavior")
        st.line_chart(df["Browsing_Behavior"].sort_values().reset_index(drop=True), use_container_width=True)

    colC, colD = st.columns(2)
    with colC:
        section_title("Engagement score")
        st.bar_chart(df["Engagement_Score"].value_counts().sort_index(), use_container_width=True)
    with colD:
        section_title("Time on site")
        st.line_chart(df["Time_on_Site"].sort_values().reset_index(drop=True), use_container_width=True)

elif page == "📊 Segment Analysis":
    page_header("Segment Analysis", "Spend and engagement by customer segment")

    segment_summary = df.groupby("Customer_Segment").agg(
        Customers=("Customer_ID", "count"),
        Avg_Spend=("Monetary_Value", "mean"),
        Median_Spend=("Monetary_Value", "median"),
        Avg_Engagement=("Engagement_Score", "mean"),
        Avg_Browsing=("Browsing_Behavior", "mean"),
        Avg_Time=("Time_on_Site", "mean"),
    ).reset_index()

    st.dataframe(segment_summary, use_container_width=True, hide_index=True)

    st.markdown("\n")
    section_title("Average spend by segment")
    st.bar_chart(segment_summary.set_index("Customer_Segment")["Avg_Spend"], use_container_width=True, color="#3b82f6")

    st.markdown("\n")
    section_title("Average engagement by segment")
    st.bar_chart(segment_summary.set_index("Customer_Segment")["Avg_Engagement"], use_container_width=True, color="#10b981")

elif page == "💡 Key Insights":
    page_header("Key Insights", "What stands out in the customer data")

    driver_cols = [
        "Purchase_History",
        "Transaction_Frequency",
        "Browsing_Behavior",
        "Engagement_Score",
        "Time_on_Site",
    ]
    corrs = [(c, float(df[c].corr(df["Monetary_Value"], method="spearman"))) for c in driver_cols]
    corrs.sort(key=lambda x: abs(x[1]), reverse=True)
    top_feat, top_rho = corrs[0]
    max_abs = abs(top_rho)

    spend_gap = float(
        df[df["Customer_Segment"] == "Copp"]["Monetary_Value"].mean()
        - df[df["Customer_Segment"] == "Iron"]["Monetary_Value"].mean()
    )
    engagement_gap = float(
        df[df["Customer_Segment"] == "Copp"]["Engagement_Score"].mean()
        - df[df["Customer_Segment"] == "Iron"]["Engagement_Score"].mean()
    )

    st.markdown(
        f"- The strongest relationship with spend is **{top_feat}** with Spearman ρ = **{top_rho:+.3f}** (largest observed |ρ| ≈ {max_abs:.3f})."
    )
    st.markdown(
        f"- Average spending is **${df[df['Customer_Segment'] == 'Copp']['Monetary_Value'].mean():,.2f}** for Copp vs **${df[df['Customer_Segment'] == 'Iron']['Monetary_Value'].mean():,.2f}** for Iron, a gap of **${abs(spend_gap):,.2f}**."
    )
    st.markdown(
        f"- Average engagement score is **{df[df['Customer_Segment'] == 'Copp']['Engagement_Score'].mean():.3f}** for Copp vs **{df[df['Customer_Segment'] == 'Iron']['Engagement_Score'].mean():.3f}** for Iron, a gap of **{abs(engagement_gap):.3f}**."
    )
    st.markdown(f"- There are **{missing} missing values** across the dataset and **{dup_count:,}** exact duplicate rows.")

elif page == "🔍 Data Quality":
    page_header("Data Quality", "Basic checks on missing values, duplicates, and outliers")

    q1, q2, q3, q4 = st.columns(4)
    kpi_card(q1, "Missing values", str(missing), "across dataset")
    kpi_card(q2, "Duplicate rows", f"{dup_count:,}", "exact matches")
    kpi_card(q3, "IQR outliers", f"{total_outliers:,}", "numeric cols")
    kpi_card(q4, "Invalid values", str(total_invalid_numeric + total_invalid_categorical), "range + category checks")

    st.markdown("<hr style='border:none;border-top:1px solid #e5e7eb;margin:1.0rem 0;' />", unsafe_allow_html=True)

    section_title("What we found")
    st.markdown(
        """
- Segment labels are checked against the expected values: Copp and Iron.
- Duplicates are retained and reported but not removed.
- Numeric outliers are identified using IQR fences on continuous fields.
"""
    )

    section_title("Details")

    with st.expander("Invalid values", expanded=False):
        invalid_numeric_df = pd.DataFrame(
            [{"Column": k, "Invalid count": v, "Check": "documented numeric range"} for k, v in invalid_rows.items()]
        )
        invalid_cat_df = pd.DataFrame(
            [{"Column": k, "Invalid count": v, "Check": "allowed category values"} for k, v in invalid_cat.items()]
        )
        st.dataframe(invalid_numeric_df, use_container_width=True)
        st.dataframe(invalid_cat_df, use_container_width=True)

    with st.expander("IQR outliers", expanded=False):
        st.dataframe(outlier_df.round(3), use_container_width=True)

    with st.expander("Missing values", expanded=False):
        st.dataframe(
            df.isnull().sum().reset_index().rename(columns={"index": "Column", 0: "Missing values"}),
            use_container_width=True,
        )

else:
    st.error("Unknown page state.")

st.markdown("</div>", unsafe_allow_html=True)
