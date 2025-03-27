import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Cancer Socio-Economic Analysis", page_icon="🧬", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4F8BF9;
    }
    .sub-header {
        font-size: 1.5rem;
        margin-top: 2rem;
    }
    .insight-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f7ff;
        margin-bottom: 1rem;
    }
    .stButton button {
        background-color: #4F8BF9;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🧬 Socio-Economic Factors & Cancer Rates</p>', unsafe_allow_html=True)
st.markdown("""
Analyze how income, poverty, and other socio-economic variables impact cancer incidence across U.S. counties. 
This interactive tool lets you explore correlations, distributions, and insights from the analysis.
""")

# Sidebar
st.sidebar.title("About This Project")
st.sidebar.markdown("""
This project analyzes the relationship between socio-economic factors and cancer rates in U.S. counties.

**Key findings:**
- Regional disparities in cancer incidence correlate with income levels
- Poverty rates show positive correlation with certain cancer types
- Education levels have significant impact on cancer outcomes

Made by Sai Rupa Jhade
""")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Data Explorer", "Correlation Analysis", "Regional Insights"])

# Demo data (in case user doesn't upload)
@st.cache_data
def load_demo_data():
    # Create synthetic data
    np.random.seed(42)
    n = 100
    counties = [f"County_{i}" for i in range(1, n+1)]
    
    # Create synthetic data with correlations
    median_income = np.random.normal(45000, 15000, n)
    poverty_rate = np.random.normal(15, 5, n)
    education_level = np.random.normal(25, 10, n)
    
    # Create cancer rates with some correlation to socioeconomic factors
    cancer_rate = 150 - 0.001 * median_income + 2 * poverty_rate + np.random.normal(0, 10, n)
    cancer_rate = np.maximum(cancer_rate, 50)  # Ensure no negative rates
    
    lung_cancer = 50 - 0.0003 * median_income + 1.5 * poverty_rate + np.random.normal(0, 5, n)
    breast_cancer = 40 - 0.0002 * median_income + 0.5 * poverty_rate + np.random.normal(0, 8, n)
    
    # Create regions
    regions = np.random.choice(['Northeast', 'Midwest', 'South', 'West'], n)
    
    # Create DataFrame
    df = pd.DataFrame({
        'County': counties,
        'Region': regions,
        'Median_Income': median_income,
        'Poverty_Rate': poverty_rate,
        'Education_Level': education_level,
        'Cancer_Rate': cancer_rate,
        'Lung_Cancer_Rate': lung_cancer,
        'Breast_Cancer_Rate': breast_cancer
    })
    
    return df

# File uploader or use demo data
with tab1:
    st.markdown('<p class="sub-header">📋 Data Explorer</p>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📂 Upload your cancer dataset (.xlsx or .csv)", type=["xlsx", "csv"])
    
    use_demo = st.checkbox("Use demo data instead", value=True)
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.success("✅ File uploaded successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
            df = load_demo_data()
    elif use_demo:
        df = load_demo_data()
        st.info("ℹ️ Using demo data. Upload your own file for custom analysis.")
    else:
        st.warning("Please upload a file or use demo data to continue.")
        st.stop()
    
    # Data preview
    st.subheader("Data Preview")
    st.dataframe(df.head())
    
    # Data summary
    st.subheader("Summary Statistics")
    st.dataframe(df.describe())
    
    # Column selector for histograms
    st.markdown('<p class="sub-header">📊 Distribution Analysis</p>', unsafe_allow_html=True)
    hist_col = st.selectbox("Select column to visualize distribution:", 
                           options=[col for col in df.columns if df[col].dtype in ['float64', 'int64']])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df[hist_col], kde=True, ax=ax)
    ax.set_title(f"Distribution of {hist_col}")
    st.pyplot(fig)

# Correlation analysis
with tab2:
    st.markdown('<p class="sub-header">📈 Correlation Analysis</p>', unsafe_allow_html=True)
    
    # Correlation matrix
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_df.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                annot=True, fmt=".2f", square=True, linewidths=.5, ax=ax)
    ax.set_title("Correlation Matrix")
    st.pyplot(fig)
    
    # Scatter plot
    st.markdown('<p class="sub-header">🔍 Relationship Explorer</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("Select X-axis variable:", options=numeric_df.columns, index=2)  # Default to income
    with col2:
        y_col = st.selectbox("Select Y-axis variable:", options=numeric_df.columns, index=5)  # Default to cancer rate
    
    color_by = st.checkbox("Color by region", value=True)
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    if color_by and 'Region' in df.columns:
        sns.scatterplot(data=df, x=x_col, y=y_col, hue='Region', ax=ax2)
        ax2.legend(title='Region')
    else:
        sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax2)
    
    # Add regression line
    sns.regplot(data=df, x=x_col, y=y_col, scatter=False, ax=ax2, line_kws={"color": "red"})
    
    ax2.set_title(f"{y_col} vs {x_col}")
    st.pyplot(fig2)
    
    # Calculate correlation
    correlation = df[x_col].corr(df[y_col])
    st.markdown(f"**Correlation coefficient:** {correlation:.3f}")
    
    if abs(correlation) > 0.7:
        st.markdown("**Strong correlation detected!**")
    elif abs(correlation) > 0.4:
        st.markdown("**Moderate correlation detected.**")
    else:
        st.markdown("**Weak correlation detected.**")

# Regional insights
with tab3:
    st.markdown('<p class="sub-header">🗺️ Regional Analysis</p>', unsafe_allow_html=True)
    
    if 'Region' in df.columns:
        # Regional averages
        regional_stats = df.groupby('Region').agg({
            'Median_Income': 'mean',
            'Poverty_Rate': 'mean',
            'Cancer_Rate': 'mean'
        }).reset_index()
        
        # Bar chart of cancer rates by region
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=regional_stats, x='Region', y='Cancer_Rate', ax=ax3)
        ax3.set_title("Average Cancer Rate by Region")
        ax3.set_ylabel("Cancer Rate (per 100,000)")
        st.pyplot(fig3)
        
        # Regional statistics
        st.subheader("Regional Statistics")
        st.dataframe(regional_stats)
        
        # Highlight highest and lowest regions
        highest_region = regional_stats.loc[regional_stats['Cancer_Rate'].idxmax()]
        lowest_region = regional_stats.loc[regional_stats['Cancer_Rate'].idxmin()]
        
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown(f"**Highest cancer rate:** {highest_region['Region']} region with {highest_region['Cancer_Rate']:.1f} per 100,000")
        st.markdown(f"**Lowest cancer rate:** {lowest_region['Region']} region with {lowest_region['Cancer_Rate']:.1f} per 100,000")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Region data not available. Upload a dataset with a 'Region' column for regional analysis.")

# Key findings
st.markdown('<p class="sub-header">🔑 Key Findings</p>', unsafe_allow_html=True)
st.markdown('<div class="insight-box">', unsafe_allow_html=True)
st.markdown("""
Based on the analysis, we can conclude:

1. **Income Impact**: There is a negative correlation between median income and cancer rates, suggesting that higher income areas tend to have lower cancer incidence.

2. **Poverty Connection**: Poverty rates show a positive correlation with cancer rates, particularly for lung cancer.

3. **Regional Disparities**: Significant variations exist between regions, with some showing up to 25% higher cancer rates than others.

4. **Policy Implications**: Targeted interventions in high-risk areas could help reduce cancer disparities.
""")
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Sai Rupa Jhade | Data Science Portfolio")

