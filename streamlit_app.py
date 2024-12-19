import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(
    page_title="US Mobility Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# Load and cache data
@st.cache_data
def load_data():
    """Load and preprocess mobility data."""
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtpT3y3Opo5yIBBbA4i3SNYzp-soN8836j3KnCgbn3yx1dF9WEpkHAe2FhnlrPKkiajlWL-7kbo_Xv/pub?gid=1245097650&single=true&output=csv"
    data = pd.read_csv(url)
    # Extract state names from the region_c column
    if 'region_c' in data.columns:
        data["State"] = data["region_c"].str.extract(r'\](.*)')
    return data

def main():
    # Load data
    data = load_data()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    menu = ["Dashboard", "About Us", "About this project", "Who is this for?"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Dashboard":
        display_dashboard(data)
    elif choice == "About Us":
        about_us()
    elif choice == "About this project":
        about_project()
    elif choice == "Who is this for?":
        who_is_this_for()

def display_dashboard(data):
    st.title("US Intergenerational Mobility Dashboard")
    st.subheader("Home Ownership Across States")

    # Statistic selector
    statistic_options = {
        "Home Ownership: Top 10%": "ownership_rate_top_10",
        "Home Ownership: Bottom 40%": "ownership_rate_bottom_40",
        "Ratio (Top 10% / Bottom 40%)": "ownership_ratio_90_40"
    }
    
    statistic_choice = st.selectbox(
        "Select Statistic",
        list(statistic_options.keys())
    )

    # Process data based on selection
    column_to_display = statistic_options[statistic_choice]
    display_data = data[["State", column_to_display]].copy()
    display_data = display_data.rename(columns={column_to_display: "Value"})

    # Create choropleth map
    fig = px.choropleth(
        display_data,
        locations="State",
        locationmode="USA-states",
        color="Value",
        scope="usa",
        title=f"{statistic_choice} by State",
        color_continuous_scale="Viridis",
        labels={"Value": statistic_choice}
    )

    st.plotly_chart(fig, use_container_width=True)

    # Summary statistics
    st.subheader("Summary Statistics")
    summary = display_data["Value"].describe().round(2)
    st.dataframe(pd.DataFrame(summary))

    # Add a data table view
    st.subheader("State-by-State Data")
    st.dataframe(display_data.sort_values("Value", ascending=False))

def about_us():
    st.title("About Us")
    st.write("""
    We are a team of researchers and data scientists dedicated to understanding and 
    visualizing intergenerational mobility in the United States.
    """)

def about_project():
    st.title("About This Project")
    st.write("""
    This dashboard visualizes intergenerational mobility data through the lens of 
    home ownership rates across different income groups in US states.
    """)

def who_is_this_for():
    st.title("Who Is This For?")
    st.write("""
    This tool is designed for:
    - Researchers studying economic mobility
    - Policy makers and analysts
    - Students and educators
    - Anyone interested in understanding home ownership disparities in the US
    """)

if __name__ == "__main__":
    main()