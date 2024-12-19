import streamlit as st
import pandas as pd
import plotly.express as px

# Set the title and favicon that appear in the browser's tab bar
st.set_page_config(
    page_title="Interactive US Inequality Map",
    page_icon=":bar_chart:",
    layout="wide"
)

# Load and cache data
@st.cache_data
def load_data():
    """Load and preprocess data for the dashboard."""
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtpT3y3Opo5yIBBbA4i3SNYzp-soN8836j3KnCgbn3yx1dF9WEpkHAe2FhnlrPKkiajlWL-7kbo_Xv/pub?gid=1245097650&single=true&output=csv"
    raw_data = pd.read_csv(url)
    return raw_data

data = load_data()

# Determine global color scale limits for all variables
color_scales = {
    "ownership_rate_total": (data["ownership_rate_total"].min(), data["ownership_rate_total"].max()),
    "ownership_rate_top_10": (data["ownership_rate_top_10"].min(), data["ownership_rate_top_10"].max()),
    "ownership_rate_bottom_40": (data["ownership_rate_bottom_40"].min(), data["ownership_rate_bottom_40"].max()),
    "ownership_rate_bottom_10": (data["ownership_rate_bottom_10"].min(), data["ownership_rate_bottom_10"].max()),
    "ownership_ratio_90_40": (data["ownership_ratio_90_40"].min(), data["ownership_ratio_90_40"].max()),
    "ownership_ratio_90_10": (data["ownership_ratio_90_10"].min(), data["ownership_ratio_90_10"].max())
}

# Main function to set up the app
def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    menu = ["About Us", "About this project", "Who is this for?", "Data"]
    choice = st.sidebar.radio("Go to:", menu)

    if choice == "About Us":
        about_us()
    elif choice == "About this project":
        about_project()
    elif choice == "Who is this for?":
        who_is_this_for()
    elif choice == "Data":
        data_page()

# Pages
def about_us():
    st.title(":information_source: About Us")
    st.write("This page provides information about the creators and their mission.")


def about_project():
    st.title(":bulb: About This Project")
    st.write("Details about the project, its objectives, and its impact.")


def who_is_this_for():
    st.title(":busts_in_silhouette: Who Is This For?")
    st.write("Identify the target audience and who can benefit from this project.")


def data_page():
    st.title(":bar_chart: Data Visualization")

    st.write("Explore inequality metrics across US states interactively.")

    # Dropdown for variable selection
    variable_options = {
        "Ownership Rate (Total)": "ownership_rate_total",
        "Ownership Rate (Top 10%)": "ownership_rate_top_10",
        "Ownership Rate (Bottom 40%)": "ownership_rate_bottom_40",
        "Ownership Rate (Bottom 10%)": "ownership_rate_bottom_10"
    }
    selected_variable_label = st.selectbox("Select Variable", list(variable_options.keys()))
    selected_variable = variable_options[selected_variable_label]

    # Ownership rates visualization
    st.write("#### Ownership Rates Visualization")

    # Filtered year slider
    years = sorted(data['year'].unique())
    filtered_years = [year for year in years if year % 5 == 0 or year == 1978 or year == 2023]
    ownership_selected_year = st.slider(
        "Select Year for Ownership Rates",
        min_value=min(filtered_years),
        max_value=max(filtered_years),
        step=5,
        value=min(filtered_years),
        key="ownership_year_slider",
        label_visibility="collapsed"
    )

    st.write("Year Selected: ", ownership_selected_year)

    # Filter data by selected year
    ownership_filtered_data = data[data['year'] == ownership_selected_year]

    if ownership_filtered_data.empty:
        st.warning("No data available for the selected year.")
    else:
        # Get the global color scale limits for the selected variable
        color_min, color_max = color_scales[selected_variable]

        # Format the legend values
        ownership_filtered_data[selected_variable] = ownership_filtered_data[selected_variable].round(2)

# Create and display an interactive choropleth map for ownership rates
        ownership_fig = px.choropleth(
            ownership_filtered_data,
            locations="state_code",
            locationmode="USA-states",
            color=selected_variable,
            hover_name="region_c",
            scope="usa",
            title=f"{selected_variable_label} by State in {ownership_selected_year}",
            color_continuous_scale="Blues",
            range_color=(0.3, 1)  # Fix the color scale
        )

        st.plotly_chart(ownership_fig, use_container_width=True)

    # Ownership ratios visualization
    st.write("#### Ownership Ratios Visualization")

    # Dropdown for ownership ratio selection
    ratio_options = {
        "Ownership Ratio (90/40)": "ownership_ratio_90_40",
        "Ownership Ratio (90/10)": "ownership_ratio_90_10"
    }
    selected_ratio_label = st.selectbox("Select Ownership Ratio", list(ratio_options.keys()))
    selected_ratio = ratio_options[selected_ratio_label]

    # Filtered year slider for ratios
    ratio_selected_year = st.slider(
        "Select Year for Ownership Ratios",
        min_value=min(filtered_years),
        max_value=max(filtered_years),
        step=5,
        value=min(filtered_years),
        key="ratio_year_slider",
        label_visibility="hidden"
        )

    st.write("Year Selected: ", ratio_selected_year)

    # Filter data by selected year for ratios
    ratio_filtered_data = data[data['year'] == ratio_selected_year]

    if ratio_filtered_data.empty:
        st.warning("No data available for the selected year.")
    else:
        # Get the global color scale limits for the selected ratio
        ratio_min, ratio_max = color_scales[selected_ratio]

        # Format the legend values for ratios
        ratio_filtered_data[selected_ratio] = ratio_filtered_data[selected_ratio].round(2)

        # Create and display an interactive choropleth map for ownership ratios
        ratio_fig = px.choropleth(
            ratio_filtered_data,
            locations="state_code",
            locationmode="USA-states",
            color=selected_ratio,
            hover_name="region_c",
            scope="usa",
            title=f"{selected_ratio_label} by State in {ratio_selected_year}",
            color_continuous_scale="Reds",
            range_color=(1, 3)  # Fix the color scale
        )

        st.plotly_chart(ratio_fig, use_container_width=True)

if __name__ == "__main__":
    main()