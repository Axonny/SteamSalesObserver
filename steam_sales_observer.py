import requests
from bs4 import BeautifulSoup
from limited_dict import LimitedDict


class SteamSalesObserver:

    __slots__ = {"session", "old_sales"}

    url = "https://steamdb.info/sales/"
    headers = {
        "authrity": "steamdb.info",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36"
    }

    def __init__(self):
        self.session = requests.session()
        self.old_sales = LimitedDict(20)

    def get_current_sales(self):
        results = []
        r = self.session.get(self.url, headers=self.headers)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"class": "table-sales"})
        table2 = table.find("tbody")

        for tr in table2.find_all('tr'):
            link = tr.find('a', {'class': "info-icon"}).get('href')
            name = tr.select_one('td:nth-child(3) > a').text
            discount = int(tr.select_one('td:nth-child(4)').text[:-1])
            if discount < -95:
                results.append((name, link))

        return results

    def get_new_sales(self):
        current_sales = self.get_current_sales()
        new_sales = []
        for game_name, url in current_sales:
            if game_name not in self.old_sales:
                new_sales.append((game_name, url))
                self.old_sales[game_name] = url
        return new_sales
