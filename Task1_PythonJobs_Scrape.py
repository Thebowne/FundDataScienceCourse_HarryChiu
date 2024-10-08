import pandas as pd
from bs4 import BeautifulSoup
import requests

data = []

# This is used to filter out skills that you're unfamiliar
print('Filter out unfamiliar skills (Separated by comma): ')
print("Example= 'django' or 'css, html'")
user_input = input('>')

# split the string into a list
skill_filter = user_input.split(",")
print(f'Filtering out {skill_filter}')

html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text

'print(html_text) #<Response [200]> mean success in request'

soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

for job in jobs:
    published_date = job.find('span', 'sim-posted').span.text

    # Filter out the dates with the words 'few days'
    if 'few' in published_date:
        job_names = job.header.h2.a.text

        # Clean out using whitespace .text.replace(' ', '')
        company_names = job.find('h3', 'joblist-comp-name').text.replace(' ', '')

        # Clean out using whitespace .text.strip() and adding commas to format
        skill = job.find('span', 'srp-skills').text.strip()
        skill_list = skill.split()
        skills = ', '.join(skill_list)

        job_link = job.header.h2.a['href']

        bar_ul = job.find('ul', 'top-jd-dtl clearfix')
        location = bar_ul.find_all('li')[1].find('span').get_text(strip=True)

        job_experience = bar_ul.find_all('li')[0].get_text(strip=True).replace("card_travel", " ").strip()

        print(job_names)

        # .lower().strip() to format the text, so it's case insensitive and remove whitespace
        if all(i.lower().strip() not in skills.lower().strip() for i in skill_filter):
            data.append({
                'Job title': job_names.strip(),
                'Company': company_names.strip(),
                'Job experience': job_experience,
                'Location': location,
                'Key skills': skills,
                'More Info': job_link,
            })

df = pd.DataFrame(data)

print(df.head())

df.to_csv('Python_jobs.csv', index=False)

'''if all(i.lower().strip() not in skills.lower().strip() for i in skill_filter):
        print(f"Company Name: {company_names.strip()}")
        print(f"Job skills: {skills}")
        print(f"More Info: {job_link}")
        print(' ')'''
