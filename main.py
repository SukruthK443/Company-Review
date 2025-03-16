import os
import requests
import random
import time
import html5lib
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

# Directory path
path = r'D:\wResearch_Project\company_data'

# File name
file_name = 'company_data.csv'

# Function to split the "Rated For" column
def split_rated_for(text):
    highly_rated_start = text.find("Highly Rated For")
    critically_rated_start = text.find("Critically Rated For")
    
    if highly_rated_start != -1 and critically_rated_start != -1:
        highly_rated_text = text[highly_rated_start + len("Highly Rated For"):critically_rated_start].strip()
        critically_rated_text = text[critically_rated_start + len("Critically Rated For"):].strip()
    else:
        highly_rated_text = ''
        critically_rated_text = ''
    
    return highly_rated_text, critically_rated_text

if os.path.exists(os.path.join(path, file_name)):
    # If filepath already exists, read the file and set page number value equal to maximum page_number value
    print(f'{os.path.join(path, file_name)} filepath is available')
    df = pd.read_csv(os.path.join(path, file_name))
    page_no = df['page_no'].max()
else:
    if not os.path.exists(path):
        directory = os.makedirs(path)
    df = pd.DataFrame()
    page_no = 1

# Iterate over each page using for loop
for i in range(page_no, 501):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    url = f'https://www.ambitionbox.com/list-of-companies?campaign=desktop_nav&page={i}'
    webpage = requests.get(url, headers=header)
    if webpage.status_code == 200:

        soup = BeautifulSoup(webpage.text, 'html5lib')
        # Initialize the empty list to store data.
        comp_name = []
        rate = []
        comp_type = []
        desc = []
        review = []
        salary = []
        interview = []
        job = []
        benefit = []

        for j in soup.find_all('div', class_='companyCardWrapper'):
            company_name = j.find('h2').text.strip()
            rating = j.find('div', class_='rating_text rating_text--md').text.strip()
            company_type = j.find('span', class_='companyCardWrapper__interLinking').text.strip()

            try:
                rated_for = j.find('div', class_='companyCardWrapper__ratingComparisonWrapper').text.strip()
            except:
                rated_for = 'missing'
                print(f'{company_name} is not rated by employees')

            list_1 = j.find_all('span', class_='companyCardWrapper__ActionCount')
            reviews = list_1[0].text.strip()
            salaries = list_1[1].text.strip()
            interviews = list_1[2].text.strip()
            jobs = list_1[3].text.strip()
            benefits = list_1[4].text.strip()

            comp_name.append(company_name)
            rate.append(rating)
            comp_type.append(company_type)
            desc.append(rated_for)
            review.append(reviews)
            salary.append(salaries)
            interview.append(interviews)
            job.append(jobs)
            benefit.append(benefits)

        # Create temporary dataframe to store the data from the webpage
        temp_df = pd.DataFrame({'Company Name': comp_name,
                                'Rating': rate,
                                'Company Type': comp_type,
                                'Rated For': desc,
                                'Reviews': review,
                                'Salaries': salary,
                                'Interviews': interview,
                                'Jobs': job,
                                'Benefits': benefit,
                                'page_no': i})

        df = pd.concat([df, temp_df], ignore_index=True)

        # Split the "Rated For" column and create new columns
        df[['Highly Rated For', 'Critically Rated For']] = df['Rated For'].apply(lambda x: pd.Series(split_rated_for(x)))

        # Remove the "Rated For," "Photos," and "Page number" columns
        df.drop(columns=['Rated For', 'page_no'], inplace=True)

        file = df.to_csv(os.path.join(path, file_name), index=False)
        print(f'page_number {i} is completed')

        time.sleep(np.random.choice(range(2, 5)))
    else:
        print(f"Invalid response. Status code: {webpage.status_code}")

# Save the final DataFrame to the CSV file
df.to_csv(os.path.join(path, file_name), index=False)
