import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

# Load the CSV file
file_path = r'D:\wResearch_Project\company_data\company_data.csv'
df = pd.read_csv(file_path)

# Extract data for processing
highly_rated = df['Highly Rated For'].dropna().tolist()
critically_rated = df['Critically Rated For'].dropna().tolist()
company_names = df['Company Name'].tolist()

# Create dictionaries for counts
highly_rated_dict = {}
critically_rated_dict = {}

for company, highly, critically in zip(company_names, highly_rated, critically_rated):
    highly_rated_dict[company] = Counter([item.strip() for item in highly.split(',')])
    critically_rated_dict[company] = Counter([item.strip() for item in critically.split(',')])

# Create DataFrames for plotting
highly_rated_df = pd.DataFrame(highly_rated_dict).fillna(0).T
critically_rated_df = pd.DataFrame(critically_rated_dict).fillna(0).T
highly_rated_df['Total'] = highly_rated_df.sum(axis=1)
critically_rated_df['Total'] = critically_rated_df.sum(axis=1)

# Helper Functions
def plot_stacked_bar(filtered_df):
    # Ensure filtered_df is a DataFrame
    top_highly_rated = filtered_df.drop(columns=['Total'], errors='ignore')
    top_critically_rated = critically_rated_df.loc[filtered_df.index]  # Match the filtered companies

    fig, axs = plt.subplots(2, 1, figsize=(20, 18), sharex=True)  # Adjust figure size for better visibility

    # Highly Rated
    top_highly_rated.plot(kind='barh', stacked=True, ax=axs[0], colormap='viridis')
    axs[0].set_title('Highly Rated For (Paginated)', fontsize=18)
    axs[0].set_xlabel('Count', fontsize=16)
    axs[0].set_ylabel('Company Name', fontsize=16)

    # Critically Rated
    top_critically_rated.drop(columns=['Total'], errors='ignore').plot(kind='barh', stacked=True, ax=axs[1], colormap='plasma')
    axs[1].set_title('Critically Rated For (Paginated)', fontsize=18)
    axs[1].set_xlabel('Count', fontsize=16)
    axs[1].set_ylabel('Company Name', fontsize=16)

    st.pyplot(fig)


def plot_lollipop(filtered_df):
    # Sort the data by "Total Highly Rated" for visualization
    sorted_df = filtered_df.sort_values('Total', ascending=False)

    # Create the lollipop chart
    fig, ax = plt.subplots(figsize=(20, 10))  # Adjust size for better visibility
    ax.stem(sorted_df['Total'], linefmt='gray', markerfmt='o', basefmt=' ')

    # Set labels and title
    ax.set_xticks(range(len(sorted_df)))
    ax.set_xticklabels(sorted_df.index, rotation=90, fontsize=10)
    ax.set_title('Lollipop Chart: Total Highly Rated by Company', fontsize=18)
    ax.set_xlabel('Company Name', fontsize=14)
    ax.set_ylabel('Total Highly Rated', fontsize=14)

    st.pyplot(fig)

    

def paginate_data(df, page, companies_per_page):
    start = (page - 1) * companies_per_page
    end = start + companies_per_page
    return df.iloc[start:end]

def download_data(filtered_data):
    csv = filtered_data.to_csv(index=True)
    st.download_button("Download Filtered Data as CSV", csv, "filtered_data.csv", "text/csv")

def plot_radar_chart(top_n):
    top_companies = highly_rated_df.sort_values('Total', ascending=False).head(top_n)
    metrics = highly_rated_df.drop(columns=['Total'], errors='ignore').columns  # Metrics from the DataFrame
    categories = metrics.tolist()

    # Prepare the data for the radar chart
    company_data = top_companies.drop(columns=['Total'], errors='ignore')

    # Create radar chart
    fig, ax = plt.subplots(figsize=(14, 14), subplot_kw=dict(polar=True))  # Increased figure size

    # Set up the angles for the radar chart
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Close the circle

    # Plot data for each top company
    for company in company_data.index:
        values = company_data.loc[company].values.flatten().tolist()
        values += values[:1]  # Close the circle
        ax.fill(angles, values, alpha=0.25, label=company)
        ax.plot(angles, values, linewidth=2, label=f'{company}')

    # Set the category labels around the circle
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)

    # Add title and legend
    ax.set_title('Radar Chart: Highly Rated Aspects by Top Companies', fontsize=16)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), fontsize=12)
    plt.tight_layout()

    st.pyplot(fig)

# Streamlit App Layout
st.title("Interactive Company Ratings Visualization")

# Controls for Filtering
st.sidebar.header("Filter Options")
search_term = st.sidebar.text_input("Search for a company:")
num_companies = st.sidebar.slider("Select Number of Companies to Display", 5, 100, 10)  # Top N companies
companies_per_page = st.sidebar.slider("Companies per Page", 10, 50, 20)  # Pagination
page = st.sidebar.number_input("Page Number", min_value=1, step=1)

# Filter data based on search term
filtered_df = highly_rated_df[highly_rated_df.index.str.contains(search_term, case=False)] if search_term else highly_rated_df
paginated_df = paginate_data(filtered_df, page, companies_per_page)

# Display Filtered Data
st.subheader(f"Displaying Page {page}")
st.dataframe(paginated_df)

# Dropdown for Plot Selection
plot_type = st.selectbox("Select Visualization Type", 
                         ['Stacked Bar Chart', 'Radar Chart', 'Lollipop Chart'])

# Generate the selected plot
if plot_type == 'Stacked Bar Chart':
    plot_stacked_bar(paginated_df)
elif plot_type == 'Radar Chart':
    plot_radar_chart(num_companies)
elif plot_type == 'Lollipop Chart':
    plot_lollipop(paginated_df)

# Download Option
download_data(filtered_df)
