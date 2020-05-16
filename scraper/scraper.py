import requests
from bs4 import BeautifulSoup

class Scraper:
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
        dic_a[list_keys_dic[0]] = country.text.replace("\n", "")
        for index in range(0, len(td) - 1):
            if not td[index].text == "" or not " ":
                dic_a[list_keys_dic[index]] = td[index].text if not "+" in td[index].text else td[index].text.split("+")[1]
                continue
            dic_a[list_keys_dic[index]] = "0"
        return dic_a

    def scraping(self):
        response = []
        dic = {}
        contintent_data = []
        for index in range(len(self.headers)-1):
            t = self.headers[index].text.lower()
            title = t if not "," in t else t.split(",")[0]
            title = title if not "/" in title else title.split("/")[0]
            # NOTA: Eso que esta dentro de las comillas no es un espacio, no tengo ni idea de que es, pero bueno, xd
            title = title if not " " in title else title.replace(" ","")
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
                    contintent_data.append(self.iterate_and_insert_data(headers=dic, td=td, country=country))
                    continue
                # Data for Diamond Princess ? xd
                country = td[0].find("span")
                if not country == None:
                    response.append(self.iterate_and_insert_data(headers=dic, td=td, country=country))
                    continue
                # Data for World
                country = td[0].text
                if not country == None:
                    country = td[0]
                    response.append(self.iterate_and_insert_data(headers=dic, td=td, country=country))
                    continue
                continue
            # Data for all countries
            response.append(self.iterate_and_insert_data(headers=dic, td=td, country=country))
        return response, contintent_data

    def iterate_in_console(self):
        response, contintent_data = self.scraping()
        print(" ############## CONTINENTS ############## ")
        for item in contintent_data:
            for key, value in item.items():
                print(key, '->', value)
        print(" ############## COUNTRIES ############## ")
        for item in response:
            for key, value in item.items():
                print(key, '->', value)