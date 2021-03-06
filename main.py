import platform
import sys

import jdatetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from unidecode import unidecode


def get_browser():
    if platform.system() == 'Linux':
        service = Service(executable_path="web_drivers/chromedriver_linux64")
    elif platform.system() == 'Windows':
        service = Service(executable_path="web_drivers/chromedriver_win32.exe")
    elif platform.system() == 'Darwin':
        service = Service(executable_path="web_drivers/chromedriver_mac64")
    else:
        raise Exception('Unsupported OS')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"')

    return webdriver.Chrome(service=service, options=chrome_options)


def process_result(elements):
    file_name = 'results/' + jdatetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.csv'
    sum = 0.0
    count = 0

    for element in elements:
        try:
            div = element.find_element(By.TAG_NAME, value='div')
            name = div.get_attribute('data-name')
            value = unidecode(div.get_attribute('data-display-color').replace('%', ''))

            file_object = open(file_name, 'a')
            file_object.write(name + ',' + value + '\n')
            file_object.close()

            sum += float(value)
            count += 1
        except:
            print(sys.exc_info())
            pass

    average = round(sum / count, 2)

    file_object = open(file_name, 'a')
    file_object.write('Sum' + ',' + str(round(sum, 2)) + '\n')
    file_object.write('Count' + ',' + str(count) + '\n')
    file_object.write('Average' + ',' + str(average) + '\n')
    file_object.close()

    if average > 2:
        print('Result: Positive', str(average))
    elif average < -2:
        print('Result: Negative', str(average))
    else:
        print('Result: Neutral', str(average))


print('Starting ...')
browser = get_browser()

print('Open Rahavard365 market map url in browser ...')
browser.get("http://rahavard365.com/marketmap")

print('Process results ...')
elements = browser.find_elements(By.CLASS_NAME, value='leaf')
process_result(elements)

browser.close()
