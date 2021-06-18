import csv
import io
import zipfile

import mechanicalsoup
import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from .models import Stocks


class StockLoader():

    def load_stocks(self, year, month, day):

        link = self._get_file_link(year, month, day)

        if link:

            headers = {
                'Host': "www1.nseindia.com",
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
                'sec-ch-ua-mobile': '?0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Referer': 'https://www1.nseindia.com/products/content/equities/equities/archieve_eq.htm',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6',
                'Cookie': 'NSE-TEST-1=1927290890.20480.0000; bm_mi=185655B0A2288A973BBE7EEFC5D93AE7~d3CmXXXFb5ntCRt0y8Ot7It0szkaWcKlIaPqAvirkg+HbaJAzZwwsBE5PBXFYFd9Ho9eDTdWLbNLy7aJgA9gNns/SZIfQRnRuSHIyo8QY/IRHc5ahH6+kWkpcCjuiUzvNwHBniDCcLeDSQTj7S1I6yvvJltwESvPOfLI7T0ZowPP2SGkb0tbvBZ1Fj7FmKo8sN3VI9+M1Hj5dyutArhK0zEsBL8JrTJFAOBEe95BVszjxBJdZM1PLRm7yYy7BDWFsKb+OXy+cp05zFcDhUKZZOT6RyVoiGvMNuExJlgMgLlAP8cdQF3Vjrdkbpyem/pUALckRRN21rg81yD/a6rRrteMbDdNPhDcTjaxMpbI9zk=; ak_bmsc=B676E8454D373B61E7CBE8C25EC1256C58DD359F130D0000358BCB6000412562~pl3SawOy0K6BMt/8nUVh75badlYXx5DZu3kLh2BA5AkO5kgF5xifbcfnu92gzX1kkB2S8kvAGgQaDnv+X+s7W47HEOUxMslxNy8plCr/jd64xQuD45HpCMHbvGRku/A6W/Cz9VauozRso1gppy6BsPppAk43weypWf2EnUOBFYi+2MNxtdHoOBaTLB99ZFtNMnbPCIVeIwbpfgAPAY1kfMb066fL5uiiy3OeCoEz41GnQNuPW0gjSuoPhd2nHvdu6+; bm_sv=04063E7B2BC897FEE2C92E43FA3C2C45~4alSlSfwgO+qqLILtwl3aVOKn/P2izvX7RkTiLHTz3BOD/P/BdR357Ul3/0R+NzwRYuuCkCg1M6POWY0n5Hobvr+cR5WCZvNRG9BRo0Ke3SsycEYQ7GMDrE5ly+Bo8G+AFoj1CvKEhTDTlEFbKFKKYG2XdB/ig2sfHRS3nQc9a0=; RT="z=1&dm=nseindia.com&si=0b67b9e3-c32d-493c-8c19-4761ae38c9bc&ss=kq181855&sl=0&tt=0&bcn=%2F%2F684dd304.akstat.io%2F&ld=13hu5&nu=7bed9755d19c0345caa5d664f453b080&cl=3krj&ul=3t2v"'
            }

            response = requests.get(link, headers=headers)

            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                file_names = zip_file.namelist()
                zip_file.extractall('./')

                if file_names:
                    file_name = file_names[0]
                    date = timezone.datetime(year, month, day)
                    self._load_data(file_name, date)

    def _load_data(self, file_path, date):

        with open(file_path) as file:
        
            reader = csv.reader(file)
            count = 0
            for line in reader:
                
                if count > 0:
                        
                    symbol = line[0]
                    open_price = line[2]
                    high = line[3]
                    low = line[4]
                    close = line[5]

                    if not Stocks.objects.filter(symbol=symbol, open_price=open_price, high=high, low=low, close=close, date=date).exists():

                        Stocks.objects.create(symbol=symbol, high=high, open_price=open_price, low=low, close=close, date=date)

                count += 1

    def _get_file_link(self, year:int, month:int, day:int):

        if month < 10:
            month = f"0{month}"

        if day < 10:
            day = f"0{day}"

        date = f"{day}-{month}-{year}"

        url = f'https://www1.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date={date}&section=EQ'

        browser = mechanicalsoup.StatefulBrowser(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")

        response = browser.open(url)
        
        soup = BeautifulSoup(response.content, 'lxml')

        link = soup.find('a')

        link = link.get('href') if link else ''

        if link:

            return "https://www1.nseindia.com" + link