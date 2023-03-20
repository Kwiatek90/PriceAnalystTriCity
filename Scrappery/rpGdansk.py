from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import re
import time
import pandas as pd

#tajny agent
options = Options()
ua = UserAgent()
user_agent = ua.random
print(user_agent)
options.add_argument(f'user-agent={user_agent}')

#przechodzi na strone
s = Service('C:\TestFiles\chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)
driver.maximize_window()
driver.get('https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/gdansk/rynek-pierwotny?distanceRadius=0&page=1&limit=72&locations=%5Bcities_6-40%5D&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing')

time.sleep(2)

#potwierdz ciasteczka ns stronie
cookies_button = driver.find_element(by=By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]')
cookies_button.click()

time.sleep(2)

#zbiera inforamcje o sumie wyników wyszukanych
total = driver.find_element(by=By.XPATH, value='//strong[@data-cy="search.listing-panel.label.ads-number"]')
total_num = re.findall(r'\d+', total.text)

print("Ilość ogłoszeń:", total_num)

#oblicza ilość stron z ogłoszeniami (72 - na stronie musi być to manualnie zaznaczone)
num_of_pages = round(int(total_num[0]) / 72)

#lista to umiejscownie danych
lokacja = []
cena = []
m2_cena = []
pokoje = []
m2 = []

#funkcja do scrapowania danych
def scrape():

    #scrolluje całą strone
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    #wyszukiwanie informacji ( w detalach klasa z poszczególnych elementów)
    lok = driver.find_elements(by=By.XPATH, value='//span[@class="css-17o293g es62z2j8"]')
    detale = driver.find_elements(by=By.XPATH, value='//span[@class="css-s8wpzb e1brl80i1"]')

    #tworzenie listy z lokacjami
    for t in lok:
        lokacja.append(t.text)

    #tworzenie listy z detalami
    x = 0
    while x < len(detale):
        cena.append(detale[x].text)
        m2_cena.append(detale[x + 1].text)
        pokoje.append(detale[x + 2].text)
        m2.append(detale[x + 3].text)
        x += 4

    #przejście na nastepną stronę
    next_button = driver.find_element(by=By.XPATH, value='//button[@data-cy="pagination.next-page"]')
    driver.execute_script("arguments[0].click();", next_button)

    #next_button.click()

    time.sleep(5)

#uruchomienie funckji na kolejnej stronie (num_of_pages)
i = 1
while i < 2:
    scrape()
    i += 1

#przekonwertowanie listy w dataframe
df = pd.DataFrame(list(zip(lokacja, cena, m2_cena, m2, pokoje)),
               columns =['Lokacja', 'Cena', 'Cena za m2', 'm2', 'Pokoje'])

#zapisanie danych w excelu
df.to_csv("rpGdansk.csv", index=False)

#zamknięcie przeglądarki
driver.quit()
