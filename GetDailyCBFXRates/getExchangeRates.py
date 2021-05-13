import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import regex as re

class getExchangeRates:
    def returnExchangeRates(date):
        url = "https://www.centralbank.ae/en/fx-rates"
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, "html.parser")
        print(type(soup))

        # Print the first 10 rows for sanity check
        rows = soup.find_all('tr')
        country_code = []
        exchange_rate = []

        for row in rows:
            cells = row.find_all('td')
            str_cells = str(cells)
            clean = re.compile('<.*?>')
            clean2 = (re.sub(clean, '', str_cells))
            clean3 = clean2.replace('[', '').replace(']', '')
            clean4 = clean3.split(',')
            if clean4[0] != '':
                country_code.append(clean4[0])
            if clean4[-1] != '':
                exchange_rate.append(clean4[-1])

        ratesDF = pd.DataFrame(list(zip(country_code, exchange_rate)), columns=['country_code', 'exchange_rate'])
        df_str = ratesDF.to_csv(index=False)
        print(df_str)
        # ratesDF.to_csv("C:\\PycharmProjects\\WebScrap\\ExchangeRate.csv")
        return df_str