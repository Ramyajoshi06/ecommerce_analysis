# Ecommerce Customer Analytics Dashboard

An interactive dashboard built with Streamlit for analyzing ecommerce customer behavior, purchase patterns, spending trends, and customer segmentation using the provided dataset.

---

## 📌 Project Description
This project helps businesses understand customer value and engagement by analyzing purchase history, transaction frequency, monetary value, browsing behavior, time spent on site, and engagement scores. It provides a simple way to explore customer segments, summarize key metrics, and check data quality without modifying the original dataset.

---

## 🎯 Objective & Problem Statement
- Analyze customer spending and engagement patterns.
- Compare key behavioral metrics across customer segments.
- Identify which customer attributes are most related to monetary value.
- Perform a data-quality check for missing values, duplicates, invalid entries, and outliers.
- Provide an easy-to-use dashboard for business analysts and ecommerce teams.

---

## 📊 Dataset Description
- **Dataset File:** `ecommerce_user_dataset.csv`
- **Dataset Source:** [Kaggle: E-Commerce Customer Behavior Dataset](https://www.kaggle.com/datasets/zara2099/e-commerce-customer-behavior-dataset)
- **Rows:** 1,000
- **Columns:** 8
- **Key Fields:**
  - `Customer_ID`: Unique customer identifier
  - `Purchase_History`: Purchase count or history value
  - `Transaction_Frequency`: Frequency of transactions
  - `Monetary_Value`: Total spend amount
  - `Browsing_Behavior`: Browsing activity or website behavior score
  - `Engagement_Score`: Customer engagement score
  - `Time_on_Site`: Time spent on the website in minutes
  - `Customer_Segment`: Customer grouping such as `Copp` and `Iron`

---

## 🛠️ Technologies Used & Python Version
- **Python Version:** Python 3.11+
- **Streamlit:** Dashboard UI and interactive application
- **Pandas:** Data processing and analytics
- **SciPy:** Correlation calculations
- **NumPy:** Numeric operations

---

## 🚀 Installation & Setup Instructions

### 1. Prerequisites
Ensure **Python 3.11+** is installed on your system.

### 2. Create and Activate Virtual Environment
```bash
# Navigate to the project directory
cd intern

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (Command Prompt):
.\.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run ecommerce_customer_analytics.py
```

The dashboard will open in your browser at `http://localhost:8501`.

---

## 🖥️ Main Dashboard Sections
1. **Overview (`📊 Overview`)**: Total customers, average spend, median spend, site time, and duplicate count.
2. **Customer Behavior (`🛍️ Customer Behavior`)**: Transaction patterns, browsing behavior, engagement score, and time-on-site trends.
3. **Segment Analysis (`📊 Segment Analysis`)**: Summary of customer segments and average spend/engagement by segment.
4. **Key Insights (`💡 Key Insights`)**: High-impact behavioral features and segment comparisons.
5. **Data Quality (`🔍 Data Quality`)**: Missing values, duplicate rows, invalid ranges, and outlier analysis.

---

## ⚠️ Analytical Notes
- Customer segments are grouped into categories such as `Copp` and `Iron`.
- Monetary value, browsing behavior, and engagement metrics are used to compare customer profiles.
- Duplicate records are reported but not removed automatically.
- Outlier detection is based on IQR thresholds for continuous numeric columns.

---

## 📁 Repository Structure
```
intern/
├── ecommerce_customer_analytics.py    # Main Streamlit dashboard
├── ecommerce_user_dataset.csv         # Ecommerce customer dataset
├── requirements.txt                   # Project dependencies
├── README.md                          # Project overview and run guide
└── .venv                              # Optional virtual environment
```
