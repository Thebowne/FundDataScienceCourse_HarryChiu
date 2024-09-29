from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

url = 'https://worldpopulationreview.com/'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

rows = soup.find_all('tr')

data = []

for row in rows:
    cols = row.find_all('td')

    if cols:
        country = cols[0].find('a').text.strip() if cols[0].find('a') else 'No Country Name'

        population_2024 = population_2023 = area = land_area = density = growth = worldp = rank = 'N/A'

        if len(cols) > 1:
            population_2024 = cols[1].text.strip()
        if len(cols) > 2:
            population_2023 = cols[2].text.strip()
        if len(cols) > 3:
            area = cols[3].text.strip()
        if len(cols) > 4:
            land_area = cols[4].text.strip()
        if len(cols) > 5:
            density = cols[5].text.strip()
        if len(cols) > 6 and cols[6].find('span'):
            growth = cols[6].find('span').text.strip()
        if len(cols) > 7 and cols[7].find('span'):
            worldp = cols[7].find('span').text.strip()
        if len(cols) > 8:
            rank = cols[8].text.strip()

        data.append({
            'Rank': rank,
            'Country': country,
            'Population 2024': population_2024,
            'Population 2023': population_2023,
            'Area': area,
            'Land area': land_area,
            'Density': density,
            'Growth': growth,
            'World %': worldp
        })

df = pd.DataFrame(data)

print(df.head())

df.to_csv('Worldpopulation.csv', index=False)