import requests
from bs4 import BeautifulSoup
import pandas as pd

#Pobieranie zawartosci strony
url="https://www.knf.gov.pl/dla_konsumenta/ostrzezenia_publiczne"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")

#Znajdz i parsuj tabele 
knf_table = soup.find_all("table", attrs={"class": "warningList"})

parsed_data = []
for knf_table_data in knf_table:
    knf_table_data = knf_table_data.tbody.find_all("tr")
    for tr in knf_table_data:
        line = []
        for td in tr:
            if td != '\n':
                td = td.text.replace("\n","")
                td = td.replace("\n2","")
                #print(td)
                line.append(td)
        parsed_data.append(line)

#print(parsed_data[0])
df = pd.DataFrame(parsed_data)

#Usuwanie zbędnej kolumny z numerem  i zmiana nazw kolumn 
df = df.drop(columns=0)
df = df.set_axis(['Nazwa podmiotu','Numer identyfikujący','Właściwa prokuratura','Wzmianki','Informacje istotne'], axis=1)

#Zapis do CSV
df.to_csv("export.csv", index=False, sep=";", encoding='utf-8')