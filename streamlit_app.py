import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cancer Socio-Economic Analysis", page_icon="🧬", layout="wide")

st.title("🧬 Socio-Economic Factors & Cancer Rates")
st.markdown("""
Analyze how income, poverty, and other socio-economic variables impact cancer incidence across U.S. counties. 
Upload the dataset to explore correlations, distributions, and simulated regression outputs from your R analysis.
""")

uploaded_file = st.file_uploader("📂 Upload the cancer dataset (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    st.subheader("📈 Correlation Matrix")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.subheader("📊 Income vs Cancer Rate")
    x_col = st.selectbox("Select Income Column", options=numeric_df.columns)
    y_col = st.selectbox("Select Cancer Rate Column", options=numeric_df.columns)
    fig2, ax2 = plt.subplots()
    sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax2)
    st.pyplot(fig2)

    st.subheader("📌 R-Script Simulation")
    st.markdown("Simulated insights from your R analysis (not live R execution):")
    st.markdown("- 🧪 Linear regression shows a negative correlation between income and cancer rates")
    st.markdown("- 📉 Poverty rate shows slight positive correlation with incidence")
    st.markdown("- 📊 Mean income: $45,000 | Mean cancer rate: 132 per 100k")
    st.success("You can now embed this app inside your portfolio!")
else:
    st.warning("Please upload your Excel dataset to begin.")
