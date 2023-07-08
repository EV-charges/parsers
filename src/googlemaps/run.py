import contextlib
import re
import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from settings import ApiSettings, GooglemapsSettings
from src.utils.make_request import RequestMethod, make_request

options = webdriver.ChromeOptions()
options.add_argument('--headless')
api_settings = ApiSettings()
settings = GooglemapsSettings()
s = Service(executable_path='chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)


def start_and_search_places() -> None:
    driver.set_window_size(1920, 1080)
    driver.get(settings.PLACES_URL)
    time.sleep(2)

    search_input = driver.find_element(By.ID, 'searchboxinput')
    search_input.clear()
    search_input.send_keys('charging stations ' + settings.SEARCH_CITY)
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="ydp1wd-haAclf"]/div[1]').click()
    time.sleep(5)


def scroll_palaces_list() -> list[WebElement]:
    while True:
        places_list = driver.find_elements(By.CLASS_NAME, "hfpxzc")
        driver.execute_script(
            "arguments[0].scrollTo(0, arguments[0].scrollHeight);",
            driver.find_element(
                By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]'
            )
        )
        time.sleep(3)
        try:
            driver.find_element(By.CLASS_NAME, "HlvSq")
            return places_list
        except NoSuchElementException:
            continue


def data_processing_and_save_db(places_list: list[WebElement]) -> None:
    for place in places_list:
        try:
            place.click()
            time.sleep(2)
        except ElementClickInterceptedException:
            continue

        place_url = driver.current_url

        uid = re.search(r"(0x.+?):", place_url)
        inner_id = int(uid.group(1), 16)

        coordinates = re.search(r"!3d(.+)!4d(.+)!15", place_url)
        lat = float(coordinates.group(1))
        lng = float(coordinates.group(2))

        soup = BeautifulSoup(driver.page_source, "lxml")
        address = soup.find("div", class_="Io6YTe fontBodyMedium kR99db").text
        name = soup.find("h1", class_="DUwDvf fontHeadlineLarge").text
        data = {
            'inner_id': inner_id,
            'coordinates': {
                'lat': lat,
                'lng': lng
            },
            'street': address,
            'city': settings.SEARCH_CITY.title(),
            'name': name,
            'source': settings.SOURCE_NAME
        }

        make_request(url=api_settings.get_or_post_places_url, json=data, method=RequestMethod.POST)

        parsing_comments(inner_id)


def parsing_comments(inner_id: int) -> None:
    try:
        driver.find_elements(By.CLASS_NAME, 'hh2c6')[1].click()
        time.sleep(3)
    except IndexError:
        return

    count_comments_str = driver.find_element(By.CLASS_NAME, 'jANrlb').find_element(By.CLASS_NAME, 'fontBodySmall').text
    count_comments = int(re.findall(r'\d+', count_comments_str)[0])
    comments = driver.find_elements(By.CLASS_NAME, 'jJc9Ad')
    while len(comments) < count_comments:
        driver.execute_script(
            "arguments[0].scrollTo(0, arguments[0].scrollHeight);",
            driver.find_element(
                By.XPATH,
                '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]'
            )
        )
        comments = driver.find_elements(By.CLASS_NAME, 'jJc9Ad')
        time.sleep(2)
    for comment in comments:
        with contextlib.suppress(NoSuchElementException):
            comment.find_element(
                By.CLASS_NAME,
                'oqftme').click()


        try:
            comment_text = comment.find_element(By.CLASS_NAME, 'wiI7pd').text
        except NoSuchElementException:
            continue

        comment_date = comment.find_element(By.CLASS_NAME, 'rsqaWe').text
        author = comment.find_element(By.CLASS_NAME, 'd4r55').text
        comment_id = comment.find_element(By.CLASS_NAME, 'MyEned').get_attribute('id')
        publication_date = convert_string_to_date(comment_date)

        data = {
            "place_id": inner_id,
            "comment_id": comment_id,
            "author": author,
            "text": comment_text,
            "publication_date": publication_date,
            "source": settings.SOURCE_NAME
        }
        make_request(url=api_settings.post_comments_url, json=data, method=RequestMethod.POST)


def convert_string_to_date(date_str: str) -> datetime:
    try:
        count = int(date_str[0])
    except ValueError:
        count = 1

    if 'year' in date_str:
        comment_date = datetime.utcnow() - timedelta(days=365 * count)
    elif 'month' in date_str:
        comment_date = datetime.utcnow() - timedelta(days=30 * count)
    elif 'week' in date_str:
        comment_date = datetime.utcnow() - timedelta(weeks=count)
    elif 'day' in date_str:
        comment_date = datetime.utcnow() - timedelta(days=count)
    elif 'hour' in date_str:
        comment_date = datetime.utcnow() - timedelta(hours=count)
    elif 'minute' in date_str:
        comment_date = datetime.utcnow() - timedelta(minutes=count)

    return comment_date


def googlemaps_parser() -> None:
    start_and_search_places()
    places = scroll_palaces_list()
    data_processing_and_save_db(places)
    driver.close()
    driver.quit()


def run() -> None:
    googlemaps_parser()


run()
