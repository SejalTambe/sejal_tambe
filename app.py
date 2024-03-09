import streamlit as st
import pandas as pd

# Load data
startup_data = pd.read_csv("Startup_Cleaned.csv")

# Function to display overall analysis
def display_overall_analysis():
    st.title("Comprehensive Startup Funding Analysis")
    
    # Total funding amount
    total_funding_amount = startup_data['Amount'].sum()
    st.subheader("Total Funding Amount:")
    st.write(f"${total_funding_amount:,.2f}")

    # Number of funded startups
    num_of_startups = startup_data['Startup Name'].nunique()
    st.subheader("Number of Funded Startups:")
    st.write(num_of_startups)

    # Top sectors by funding amount
    st.subheader("Top Sectors by Funding Amount:")
    top_sectors_funding = startup_data.groupby('Industry Vertical')['Amount'].sum().nlargest(5)
    st.bar_chart(top_sectors_funding)

    # Type of funding
    st.subheader("Type of Funding:")
    funding_types = startup_data['Investment Type'].value_counts()
    st.bar_chart(funding_types)

# Function to display startup details
def display_startup_details(selected_startup):
    st.title(f"Details for Startup: {selected_startup}")
    
    # Filter data for selected startup
    selected_startup_data = startup_data[startup_data['Startup Name'] == selected_startup]
    
    # Display basic information
    st.subheader("Basic Information:")
    st.write(selected_startup_data.iloc[0][['Startup Name', 'Industry Vertical', 'City', 'Amount']])
    
    # Display funding rounds
    st.subheader("Funding Rounds:")
    st.write(selected_startup_data[['Date', 'Investment Type', 'Investors Name', 'Amount']])

# Function to display investor details
def display_investor_details(selected_investor):
    st.title(f"Details for Investor: {selected_investor}")
    
    # Filter data for selected investor
    selected_investor_data = startup_data[startup_data['Investors Name'].str.contains(selected_investor, na=False)]
    
    # Display most recent investments
    st.subheader("Most Recent Investments:")
    st.write(selected_investor_data[['Date', 'Startup Name', 'Industry Vertical', 'City', 'Investment Type', 'Amount']].head(5))

    # Display maximum investment
    max_investment = selected_investor_data.groupby('Startup Name')['Amount'].sum().nlargest(1)
    st.subheader("Maximum Investment:")
    st.write(max_investment)

# Sidebar options
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select Analysis', ['Overall Analysis', 'Startup Details', 'Investor Details'])

# Based on selected option, display corresponding analysis
if option == 'Overall Analysis':
    display_overall_analysis()
elif option == 'Startup Details':
    selected_startup = st.sidebar.selectbox('Select Startup', startup_data['Startup Name'].unique())
    display_startup_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor', startup_data['Investors Name'].unique())
    display_investor_details(selected_investor)
