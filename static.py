import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_holidays(start_year, end_year):
    base_url = "https://www.officeholidays.com/countries/taiwan/"
    all_holidays = []

    for year in range(start_year, end_year + 1):
        url = f"{base_url}{year}"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'class': 'country-table'})
            
            if table:
                rows = table.find_all('tr')[1:]  # Skip header row
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        day = cols[0].text.strip()
                        date = cols[1].text.strip()
                        holiday_name = cols[2].text.strip()
                        holiday_type = cols[3].text.strip()
                        
                        all_holidays.append({
                            'Year': year,
                            'Day': day,
                            'Date': date,
                            'Holiday Name': holiday_name,
                            'Type': holiday_type
                        })
        else:
            print(f"Failed to fetch data for year {year}")

    return pd.DataFrame(all_holidays)

holidays_df = fetch_holidays(2015, 2026)

holidays_df.to_csv('static.csv', index=False)
