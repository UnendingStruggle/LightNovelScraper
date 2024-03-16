import os
import time
import cloudscraper
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
Scraper = cloudscraper.create_scraper(delay=2)

# Function to remove special characters from a string for sanitization


def remove_special_characters(input_string):
    pattern = re.compile(r'[^a-zA-Z0-9- ]')
    return re.sub(pattern, '', input_string)

# Function to convert content to a text file and save it


def convert_to_txt(content, chap, FinalPath):
    try:
        chap = remove_special_characters(chap)
        path = os.path.join(FinalPath, chap)
        file = open(f'{path}.txt', 'w+', encoding="utf-8")
        for item in content:
            file.write(item+'\n')
        file.close()
    except FileNotFoundError:
        pass

# Function to scrape chapter links from the search result


def ChapterScrape(searchresult):
    URL = searchresult[1]
    driver.get(f'{URL}#tab-chapters-title')
    time.sleep(5)
    print("\033[1;32m.\033[0;37m", end='')
    ChapterLinks = []
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    chap = soup.find("div", class_="panel-body").find_all('a')
    print("\033[1;32m.\033[0;37m", end='')
    for link in chap:
        ChapterLinks.append(link['href'])
    driver.quit()
    print("\033[1;32m.\033[0;37m")
    print(f"Total {len(ChapterLinks)} Chapters\n")
    return ChapterLinks

# Function to download chapters from ChapterLinks within the specified index range


def ChapterDownloadFunction(ChapterLinks, chapter_index, FinalPath):
    for i in range(chapter_index[0]-1, chapter_index[1]):
        try:
            page = Scraper.get(ChapterLinks[i], stream=True)
        except:
            print("\033[0;31mSite Not responding. Reconnecting...\033[0;37m")
            ChapterDownloadFunction(ChapterLinks, chapter_index)
        else:
            soup = BeautifulSoup(page.content, "html.parser")
            ch_con = soup.find("div", class_="chr-c").find_all('p')
            info = []
            title = soup.find("div", class_='col-xs-12').h2.a["title"]
            print(title)
            info.append(title)
            for item in ch_con:
                info.append(item.get_text().strip())
            convert_to_txt(info, title, FinalPath)

# Function to search for a light novel on the specified source


def SearchFunction(source, LightNovelName):
    searchresult = []
    print("\033[1;32m \nSearching.\033[0;37m", end='')
    time.sleep(1)
    response = Scraper.get(
        f"{source}search?keyword={LightNovelName}")
    Soup = BeautifulSoup(response.content, "html.parser")
    search = Soup.find_all(
        "h3", class_="novel-title")
    latest = Soup.find_all(
        "div", class_="col-xs-2 text-info")
    print("\033[1;32m.\033[0;37m", end='')
    time.sleep(1)
    for i, item in enumerate(search):
        searchresult.append(
            [item.a["title"], item.a["href"], latest[i].a["href"], latest[i].a["title"]])
    print("\033[1;32m.\033[0;37m")
    time.sleep(1)
    return searchresult
