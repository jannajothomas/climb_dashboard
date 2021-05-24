import csv
import re

import bs4
import requests
from selenium import webdriver


# op = webdriver.ChromeOptions()
# op.add_argument('headless')
# driver = webdriver.Chrome(options=op)


def get_user_data(search_term):
    # driver = webdriver.Chrome()

    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)

    driver.get("https://www.mountainproject.com/search?q=" + search_term)
    # load the page code in beautiful soup
    jspagedata = bs4.BeautifulSoup(driver.page_source, 'html.parser')

    jsIDsearch = re.compile(r'\<a href="\/u\/(\d+)"')
    jsthreadIDs = jsIDsearch.findall(str(jspagedata))

    idTuple = []
    for my_id in jsthreadIDs:
        this_tuple = (search_term, my_id)
        idTuple.append(this_tuple)
    return idTuple


def get_tick_url(user_info):
    (name, id_num) = user_info
    ticks_url = 'https://www.mountainproject.com/user/' + id_num + '/' + name + '/tick-export'
    return ticks_url


def get_csv_reader_from_url(url):
    r = requests.get(url)
    text = r.iter_lines()
    gen = (line.decode('utf-8') for line in text)
    reader = csv.reader(gen, delimiter=",", quotechar='"')
    return reader
