import threading
import time

from bs4 import BeautifulSoup
from hdfs3 import HDFileSystem
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import json

URL = 'https://www.wynikilotto.net.pl/lotto/wyniki/'
data = {'Numer loterii': [],
        'Data loterii': [],
        'Zwycięskie numery': [],
        'Rozpoczęcie pobierania danych': [],
        'Zakończenie pobierania danych': []
        }


def web_scraping():
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome("chromium.chromedriver", options=chrome_options)
    driver.get(URL)

    time_in = datetime.now().time()

    try:
        cookie = driver.find_element_by_id('accept-cookies-checkbox')
        cookie.click()
    except:
        pass

    # set DropDown as max results
    select = Select(driver.find_element_by_name('ile'))
    select.select_by_value('max')

    # button to refresh table to get max results
    button = driver.find_element_by_xpath('//*[@id="mainl"]/section/form[1]/fieldset/button')
    button.click()

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, features='html.parser')

    # Scraping table
    for table in soup.find_all('tbody'):
        time_out = datetime.now().time()
        for results in table:
            rows = results.get_text().strip('\n')

            lottery_no = rows[:4]
            lottery_date = rows[4:14]
            lottery_winner_no = rows[14:31]

            data['Numer loterii'].append(lottery_no)
            data['Data loterii'].append(lottery_date)
            data['Zwycięskie numery'].append(lottery_winner_no.split())
            data['Rozpoczęcie pobierania danych'].append(time_in)
            data['Zakończenie pobierania danych'].append(time_out)

    return data


def create_DF(result):
    df = pd.DataFrame(data=result, columns=[
        'Numer loterii',
        'Data loterii',
        'Zwycięskie numery',
        'Rozpoczęcie pobierania danych',
        'Zakończenie pobierania danych'
    ])

    return df


def connect_HDFS(df):
    df.to_csv('lotto_results.csv', sep='\t', index=False)
    client_hdfs = HDFileSystem(host='localhost', port=9000)


    print(client_hdfs.ls('/'))
    # client_hdfs.mkdir('/lotto-data')
    # print(client_hdfs.ls('/'))
    with client_hdfs.open('/lotto-data/lotto_results.csv', 'wb') as f:
        f.write(df.to_csv(sep='\t', index=False))


def connect_MongoDB(data):
    client = MongoClient(
        "mongodb+srv://marwoj:Test1234@cluster0.5p3vw.mongodb.net/web_scraping?retryWrites=true&w=majority")
    database = client['web_scraping']
    collection = database['lotto_results']

    collection.drop({})
    records = json.loads(data.T.to_json()).values()
    collection.insert_many(records)


### periodic run test
WAIT_SECONDS = 1
def foo():
    print(time.ctime())
    threading.Timer(WAIT_SECONDS, foo).start()
    

if __name__ == '__main__':
    #foo() #periodic run test

    result = web_scraping()
    df = create_DF(result)

    connect_HDFS(df)
    # connect_MongoDB(df)
