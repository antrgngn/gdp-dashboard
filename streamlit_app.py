import streamlit as st
import pandas as pd
import plotly.express as px

# Pages



def about_us():
    st.title("Inequality Tutorial Dashboard -- USA")
    st.header(":information_source: About Us")
    st.write("We are a team of students passionate about economic inequality and its implications on society. This project was developed as part of our coursework to apply theoretical concepts of inequality and mobility to real-world data. Through this tool, we aim to shed light on the nuances of wealth distribution, particularly focusing on homeownership across U.S. states.")

    st.write("Our mission is to make complex inequality data accessible and actionable, fostering data-driven discussions and promoting awareness of wealth disparities. We hope this tool serves as an educational resource and a starting point for meaningful conversations about economic inequality.")


def about_project():
    st.title("Inequality Tutorial Dashboard -- USA")
    st.header(":bulb: About This Project")

    st.write("This project is an interactive data visualization tool designed to explore homeownership inequality across the United States from 1978 to 2023. By leveraging choropleth maps and interactive filters, the tool highlights disparities in wealth distribution both in absolute terms (homeownership rates) and relative terms (inequality ratios).")

    st.write("### Key Objectives")
    st.write("- Make inequality data accessible through intuitive visualizations.")
    st.write("- Analyze trends in homeownership over five decades.")
    st.write("- Compare wealth distribution among different income groups to highlight disparities.")
    st.write("- Facilitate evidence-based discussions around housing policies and inequality.")

    st.write("### Features")
    st.write("- **Interactive year selection**: Explore data over five decades.")
    st.write("- **Multiple metrics**: Switch between absolute rates and relative ratios.")
    st.write("- **State-level granularity**: Understand regional disparities.")
    st.write("- **Educational insights**: Each graph is accompanied by explanatory text.")

    st.write("### Expected Impact")
    st.write("- Support policymakers in crafting equitable housing policies.")
    st.write("- Enable community organizations to understand local challenges.")
    st.write("- Foster public awareness of wealth disparities.")
    st.write("- Provide educators with a practical tool for teaching about inequality.")


def who_is_this_for():
    st.title("Inequality Tutorial Dashboard -- USA")
    st.header(":busts_in_silhouette: Who Is This For?")

    st.write("This tool is designed for anyone interested in understanding wealth inequality, including:")
    st.write("- **Policymakers**: To craft informed, data-driven housing policies.")
    st.write("- **Researchers and students**: To analyze long-term trends and regional disparities.")
    st.write("- **Community organizations**: To identify and address local challenges in housing inequality.")
    st.write("- **Concerned citizens**: To gain insights into economic inequality and its implications on society.")

    st.write("The tool is beginner-friendly, requiring no technical expertise, while also offering sufficient depth for academic and policy analysis. By visualizing data across income groups and states, we hope to empower users with a clear understanding of homeownership disparities and inspire action to address them.")

def data_limitations():
    st.title("Inequality Tutorial Dashboard -- USA")
    st.header(":clipboard: Data Limitations & Methodology")
    
    # Data Sources Section
    st.write("### Data Sources")
    st.write("The data is obtained from the Luxembourg Income Study, taking the household datasets of the United States. "
             "The data is accessed through the LISSY software of the Luxembourg Income Study, where we extracted summary "
             "statistics of home ownership at relevant income percentiles. This data, extracted using R, is then collected "
             "into a dataset, in which we used Python to analyze and Streamlit to deploy.")
    
    # Strengths Section
    st.write("### Strengths of Our Data & Analysis")
    st.write("- Long-term historical perspective spanning over 45 years (1978-2023)")
    st.write("- Consistent measurement methodology across states and time periods")
    st.write("- Multiple inequality metrics providing different perspectives on wealth gaps")
    st.write("- State-level granularity allows for regional comparison and analysis")
    st.write("- Focus on homeownership as a concrete, measurable indicator of wealth inequality")
    
    # Limitations Section
    st.write("### Limitations & Considerations")
    st.write("- Does not capture within-state variations or city-level differences")
    st.write("- Homeownership alone doesn't tell the complete story of wealth inequality")
    st.write("- Quality of housing and property values not reflected in ownership rates")
    st.write("- Doesn't account for cultural or regional differences in housing preferences")
    st.write("- Five-year intervals may miss short-term fluctuations")
    st.write("- Does not include data on racial disparities in homeownership")
    st.write("- May not fully reflect alternative forms of property ownership or housing arrangements")
    
    # Future Improvements Section
    st.write("### Future Improvements")
    st.write("- Addition of metropolitan area data for finer geographic detail")
    st.write("- Integration of housing quality and property value metrics")
    st.write("- Inclusion of racial and ethnic demographic data")
    st.write("- More frequent data updates where available")
    st.write("- Addition of complementary wealth inequality indicators")

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
    menu = ["About Us", "About this project", "Who is this for?", "Data", "Product Evaluation"]
    choice = st.sidebar.radio("Go to:", menu)

    if choice == "About Us":
        about_us()
    elif choice == "About this project":
        about_project()
    elif choice == "Who is this for?":
        who_is_this_for()
    elif choice == "Data":
        data_page()
    elif choice == "Product Evaluation":
        data_limitations()


def data_page():
    st.title("Inequality Tutorial Dashboard -- USA")
    st.header(":bar_chart: Data Visualization")

    st.write("This dashboard provides an interactive exploration of inequality metrics across the United States. The graphs below highlight different aspects of wealth distribution, such as homeownership rates and inequality ratios. Each graph is accompanied by an explanatory section to help you understand its significance and interpret the data effectively.")

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
        label_visibility="hidden"
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

        # Explanatory section for ownership rates
        st.write(f"The **{selected_variable_label}** graph shows the proportion of homeownership across different states in the US. A higher value indicates a greater percentage of residents who own homes. This metric helps to identify regions with high or low homeownership, often linked to economic conditions, housing affordability, and income levels. For instance, states with higher ownership rates might reflect strong housing markets or more equitable wealth distribution.")

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

        # Explanatory section for ownership ratios
        st.write(f"The **{selected_ratio_label}** graph illustrates inequality in homeownership distribution between different economic groups. A higher ratio indicates a larger disparity between the wealthiest and less affluent segments of the population. For example, a ratio of 2 means the top group owns twice as much as the lower group. Understanding these ratios helps to analyze wealth concentration and the effectiveness of policies aimed at reducing economic inequality.")

if __name__ == "__main__":
    main()
