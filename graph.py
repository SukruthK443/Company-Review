import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

# Load the CSV file into a DataFrame
file_path = r'D:\wResearch_Project\company_data\company_data.csv'
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

# Add totals and select top 20 companies
highly_rated_df['Total'] = highly_rated_df.sum(axis=1)
critically_rated_df['Total'] = critically_rated_df.sum(axis=1)

# Create top 20 DataFrames and add "Others" category
top_highly_rated = highly_rated_df.sort_values('Total', ascending=False).head(20)
others_highly_rated = highly_rated_df.iloc[20:].sum()
others_highly_rated.name = 'Others'
top_highly_rated = pd.concat([top_highly_rated, others_highly_rated.to_frame().T])

top_critically_rated = critically_rated_df.sort_values('Total', ascending=False).head(20)
others_critically_rated = critically_rated_df.iloc[20:].sum()
others_critically_rated.name = 'Others'
top_critically_rated = pd.concat([top_critically_rated, others_critically_rated.to_frame().T])

# Set up the plot style
sns.set(style="whitegrid")

# Plot the data for each company
fig, axs = plt.subplots(2, 1, figsize=(14, 16), sharex=True)

# Highly Rated For
top_highly_rated.drop(columns=['Total']).plot(kind='barh', stacked=True, ax=axs[0], colormap='viridis')
axs[0].set_title('Top 20: Highly Rated For', fontsize=16)
axs[0].set_xlabel('Count', fontsize=14)
axs[0].set_ylabel('Company Name', fontsize=14)
axs[0].legend(loc='upper right', title='Aspects', fontsize=12)
axs[0].tick_params(axis='both', which='major', labelsize=12)
axs[0].set_yticklabels(axs[0].get_yticklabels(), rotation=0)

# Critically Rated For
top_critically_rated.drop(columns=['Total']).plot(kind='barh', stacked=True, ax=axs[1], colormap='plasma')
axs[1].set_title('Top 20: Critically Rated For', fontsize=16)
axs[1].set_xlabel('Count', fontsize=14)
axs[1].set_ylabel('Company Name', fontsize=14)
axs[1].legend(loc='upper right', title='Aspects', fontsize=12)
axs[1].tick_params(axis='both', which='major', labelsize=12)
axs[1].set_yticklabels(axs[1].get_yticklabels(), rotation=0)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig(r'D:\wResearch_Project\company_data\highly_critically_rated.png', dpi=300)
plt.show()

# Calculate total counts for each aspect
highly_rated_total = highly_rated_df.drop(columns=['Total'], errors='ignore').sum(axis=1)
critically_rated_total = critically_rated_df.drop(columns=['Total'], errors='ignore').sum(axis=1)

# Create a summary DataFrame
standings_df = pd.DataFrame({
    'Total Highly Rated': highly_rated_total,
    'Total Critically Rated': critically_rated_total,
    'Net Score': highly_rated_total - critically_rated_total  # Higher is better
}).sort_values('Net Score', ascending=False)

# Display top companies
print("Company Standings (Top 10):")
print(standings_df.head(10))

# Save standings to a CSV file
standings_file = r'D:\wResearch_Project\company_data\company_standings.csv'
standings_df.to_csv(standings_file, index=True)
print(f"Company standings saved to {standings_file}")
