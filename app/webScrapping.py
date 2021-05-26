from tools.logger import Logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import typing


def string_to_value(val: str) -> typing.Tuple[int, float]:
    if val == '':
        return 0
    else:
        if val.find('.') == -1:
            val = int(val.replace(',', '').replace('+',''))
        else: 
            val = float(val.replace(',', '').replace('+',''))
        return val

def web_scrapping() -> json:
    logger = Logger('Web-Scrapper')
    data = []
    
    logger.log_entry('Open chromium in headless mode')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.worldometers.info/coronavirus')

    logger.log_entry('Getting data from table')
    elements = driver.find_elements_by_xpath('//table[@id="main_table_countries_today"]/tbody/tr')
    
    if len(elements) == 0:
        logger.log_entry('Table/Element not found', 'err')
        exit(1)

    for element in elements:
        get_inner_elements = element.find_elements_by_xpath('td')

        if get_inner_elements[1].text == '':
            continue

        inner_data = {
            'country': get_inner_elements[1].text,
            'total_cases': string_to_value(get_inner_elements[2].text),
            'new_cases': string_to_value(get_inner_elements[3].text),
            'total_deaths': string_to_value(get_inner_elements[4].text),
            'new_deaths': string_to_value(get_inner_elements[5].text),
            'total_recovered': string_to_value(get_inner_elements[5].text),
            'active_cases': string_to_value(get_inner_elements[6].text),
            'serious_cases': string_to_value(get_inner_elements[7].text),
            'total_tests': string_to_value(get_inner_elements[11].text),
            'population': string_to_value(get_inner_elements[13].text),
        }
        data.append(inner_data)

    logger.log_entry('Close chromium')
    driver.close()

    return json.dumps(data)