import requests
from bs4 import BeautifulSoup

class Scrapper:
    URL = "https://www.worldometers.info/coronavirus"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # Select headers table
    headers = soup.find_all("thead")[0].find_all("th")
    #Select content in body
    contents = soup.find_all("tbody")[0].find_all("tr")

    def iterate_and_insert_data(self, headers, td, country):
        dic_a = {}
        list_keys_dic = list(headers.keys())
        dic_a[list_keys_dic[0]] = country.text.rstrip('\n')
        for index in range(0, len(td) - 1):
            if not td[index].text == "" or not " ":
                dic_a[list_keys_dic[index]] = td[index].text if not "+" in td[index].text else td[index].text.split("+")[1]
                continue
            dic_a[list_keys_dic[index]] = "0"
        return dic_a

    def scrapping(self):
        response = []
        dic = {}
        contintent_data = []
        for index in range(len(self.headers)-1):
            t = self.headers[index].text.lower()
            title = t if not "," in t else t.split(",")[0]
            title = title if not "/" in title else title.split("/")[0]
            if not title == "": 
                dic[title] = ""
                continue
        for content in self.contents:
            td = content.find_all('td')
            country = td[0].find("a")
            if country == None:
                # Data for continents
                country = td[0].find("nobr")
                if not country == None:
                    # dic['name'] = dic.pop(list(dic.keys())[0])
                    contintent_data.append(self.iterate_and_insert_data(headers=dic, td=td, country=country))
                    continue
                country = td[0].find("span")
                if not country == None:
                    response.append(self.iterate_and_insert_data(headers=dic, td=td, country=country))
                    continue
                continue
            response.append(self.iterate_and_insert_data(headers=dic, td=td, country=country))
        return response, contintent_data

    def iterate_in_console(self):
        for item in self.scrapping():
            for key, value in item.items():
                print(key, '->', value)