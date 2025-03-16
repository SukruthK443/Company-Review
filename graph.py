import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

# Load the CSV file into a DataFrame
file_path = r'D:\webscrapping_projects\company_data\company_data.csv'
df = pd.read_csv(file_path)

# Extract the elements from "Highly Rated For" and "Critically Rated For" columns
highly_rated = df['Highly Rated For'].dropna().tolist()
critically_rated = df['Critically Rated For'].dropna().tolist()
company_names = df['Company Name'].tolist()

# Create dictionaries to store the counts for each company
highly_rated_dict = {}
critically_rated_dict = {}

# Populate the dictionaries
for company, highly, critically in zip(company_names, highly_rated, critically_rated):
    highly_rated_dict[company] = Counter([item.strip() for item in highly.split(',')])
    critically_rated_dict[company] = Counter([item.strip() for item in critically.split(',')])

# Create DataFrames for plotting
highly_rated_df = pd.DataFrame(highly_rated_dict).fillna(0).T
critically_rated_df = pd.DataFrame(critically_rated_dict).fillna(0).T

# Set up the plot style
sns.set(style="whitegrid")

# Plot the data for each company
fig, axs = plt.subplots(2, 1, figsize=(14, 16), sharex=True)

# Highly Rated For
highly_rated_df.plot(kind='barh', stacked=True, ax=axs[0], colormap='coolwarm')
axs[0].set_title('Highly Rated For', fontsize=16)
axs[0].set_xlabel('Count', fontsize=14)
axs[0].set_ylabel('Company Name', fontsize=14)
axs[0].legend(loc='upper right', title='Aspects', fontsize=12)
axs[0].tick_params(axis='both', which='major', labelsize=12)

# Critically Rated For
critically_rated_df.plot(kind='barh', stacked=True, ax=axs[1], colormap='coolwarm')
axs[1].set_title('Critically Rated For', fontsize=16)
axs[1].set_xlabel('Count', fontsize=14)
axs[1].set_ylabel('Company Name', fontsize=14)
axs[1].legend(loc='upper right', title='Aspects', fontsize=12)
axs[1].tick_params(axis='both', which='major', labelsize=12)

# Add grid lines for better readability
for ax in axs:
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.set_facecolor('#f9f9f9')

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
