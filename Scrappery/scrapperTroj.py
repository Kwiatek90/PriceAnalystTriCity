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
driver.get('https://ogloszenia.trojmiasto.pl/nieruchomosci-rynek-wtorny/mieszkanie/f1i,1_2_3.html#')

time.sleep(2)

#potwierdz ciasteczka ns stronie
cookies_button = driver.find_element(by=By.XPATH, value='//button[@id="onetrust-accept-btn-handler"]')
cookies_button.click()

time.sleep(2)

#lista do umiejscownie danych
lokacja = []
cena = []
m2_cena = []
m2 = []
pokoje = []
pietro = []


def scrape():

    #scrolluje całą strone
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    
    #wyszukiwanie informacji ( w detalach klasa z poszczególnych elementów)
    lok = driver.find_elements(by=By.XPATH, value='//p[@class="list__item__content__subtitle"]')
    price = driver.find_elements(by=By.XPATH, value='//p[@class="list__item__price__value"]')
    pricePerM2 = driver.find_elements(by=By.XPATH, value='//p[@class="list__item__details__info details--info--price"]')
    powierzchnia = driver.find_elements(by=By.XPATH, value='//li[@class="list__item__details__icons__element details--icons--element--powierzchnia"]//p[@class="list__item__details__icons__element__desc"]')
    room = driver.find_elements(by=By.XPATH, value='//li[@class="list__item__details__icons__element details--icons--element--l_pokoi"]//p[@class="list__item__details__icons__element__desc"]')
    floor = driver.find_elements(by=By.XPATH, value='//li[@class="list__item__details__icons__element details--icons--element--pietro"]//p[@class="list__item__details__icons__element__desc"]')
    
    #lista z lokacjami
    for t in lok:
        lokacja.append(t.text)
        
    #lista z cenami
    for p in price:
        cena.append(p.text)
    
    #lista z cenami za m2
    for pm2 in pricePerM2:
        m2_cena.append(pm2.text)
        
    for d in powierzchnia:
        m2.append(d.text)
        
    for r in room:
        pokoje.append(r.text) 
        
    for f in floor:
        pietro.append(f.text)
 
    #przejście na nastepną stronę
    next_button = driver.find_element(by=By.XPATH, value='//a[@class="pages__controls__next"]')
    driver.execute_script("arguments[0].click();", next_button)

    time.sleep(5)

#uruchomienie funckji na kolejnej stronie (num_of_pages)
i = 1
while i < 204:
    scrape()
    i += 1

#przekonwertowanie listy w dataframe
df = pd.DataFrame(list(zip(lokacja, cena, m2_cena, m2, pokoje, pietro)),
               columns =['Lokacja', 'Cena', 'Cena za m2', 'M2', 'Pokoje', 'Pietro'])

#zapisanie danych w excelu
df.to_csv("data.csv", index=False)

#zamknięcie przeglądarki
driver.quit()