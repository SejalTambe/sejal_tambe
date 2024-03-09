import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("Startup_Cleaned.csv")

# Function to display overall analysis
def overall():
    st.title("Overall Startup Funding Analysis")
    
    # Total funding amount
    total_funding = df['amount'].sum()
    st.subheader("Total Funding Amount:")
    st.write(f"${total_funding:,.2f}")

    # Number of funded startups
    num_startups = df['startup'].nunique()
    st.subheader("Number of Funded Startups:")
    st.write(num_startups)

    # Top sectors by funding amount
    st.subheader("Top Sectors by Funding Amount:")
    top_sectors_sum = df.groupby('vertical')['amount'].sum().nlargest(5)
    st.bar_chart(top_sectors_sum)

    # Type of funding
    st.subheader("Type of Funding:")
    funding_types = df['round'].value_counts()
    st.bar_chart(funding_types)

# Function to display startup details
def load_startup_details(startup_name):
    st.title(f"Details for {startup_name}")
    
    # Filter data for selected startup
    startup_data = df[df['startup'] == startup_name]
    
    # Display basic information
    st.subheader("Basic Information:")
    st.write(startup_data.iloc[0][['startup', 'vertical', 'city', 'amount']])
    
    # Display funding rounds
    st.subheader("Funding Rounds:")
    st.write(startup_data[['date', 'round', 'investors', 'amount']])

# Function to display investor details
def load_investor_details(investor):
    st.title(f"Details for Investor: {investor}")
    
    # Filter data for selected investor
    investor_data = df[df['investors'].str.contains(investor, na=False)]
    
    # Display most recent investments
    st.subheader("Most Recent Investments:")
    st.write(investor_data[['date', 'startup', 'vertical', 'city', 'round', 'amount']].head(5))

    # Display maximum investment
    max_investment = investor_data.groupby('startup')['amount'].sum().nlargest(1)
    st.subheader("Maximum Investment:")
    st.write(max_investment)

# Sidebar options
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select Analysis', ['Overall Analysis', 'Startup Details', 'Investor Details'])

# Based on selected option, display corresponding analysis
if option == 'Overall Analysis':
    overall()
elif option == 'Startup Details':
    startup_name = st.sidebar.selectbox('Select Startup', df['startup'].unique())
    load_startup_details(startup_name)
else:
    investor_name = st.sidebar.selectbox('Select Investor', df['investors'].unique())
    load_investor_details(investor_name)
