import logging
import os
import urllib.parse
from time import sleep

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

logging.getLogger().setLevel(logging.INFO)

BASE_URL = 'https://www.google.com/'


def get_title(key):
    display = Display(visible=0, size=(800, 600))
    display.start()
    logging.info('Initialized virtual display..')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')

    chrome_options.add_experimental_option('prefs', {
        'download.default_directory': os.getcwd(),
        'download.prompt_for_download': False,
    })
    logging.info('Prepared chrome options..')

    driver = webdriver.Chrome(chrome_options=chrome_options)
    logging.info('Initialized chrome driver..')

    base_url = 'https://www.youtube.com/results?search_query='
    url_search = base_url + urllib.parse.quote(key)
    driver.get(url_search)
    sleep(3)
    html = driver.find_element_by_tag_name('html')
    for i in range(5):
        html.send_keys(Keys.END)
        sleep(3)
    ele_titles = driver.find_elements_by_css_selector(
        '#video-title > yt-formatted-string')
    titles = []
    for e in ele_titles:
        print(e.text)
        titles.append(f'{key} - {e.text}')
    
    with open('title_video', 'a+') as f:
        f.write('\n'.join(titles))

    driver.quit()
    display.stop()


def firefox_example():
    display = Display(visible=0, size=(800, 600))
    display.start()
    logging.info('Initialized virtual display..')

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('driver.download.folderList', 2)
    firefox_profile.set_preference('driver.download.manager.showWhenStarting', False)
    firefox_profile.set_preference('driver.download.dir', os.getcwd())
    firefox_profile.set_preference('driver.helperApps.neverAsk.saveToDisk', 'text/csv')

    logging.info('Prepared firefox profile..')

    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    logging.info('Initialized firefox driver..')

    driver.get(BASE_URL)
    logging.info('Accessed %s ..', BASE_URL)

    logging.info('Page title: %s', driver.title)

    driver.quit()
    display.stop()




def main():
    with open('diykey.txt', 'r', encoding='utf-8') as f:
        list_key = f.read().split('\n')
    for key in list_key:
        get_title(key)


if __name__ == '__main__':
    main()


