from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import os


s = Service('chromedriver.exe')


browser = webdriver.Chrome(service=s)


heading_class = ".mr-2.text-label-1"
body_class = ".px-5.pt-4"

cnt = 1
qfolder = "questions"


def getlinks() :
    file_path = "clean_problems.txt"
    with open(file_path, 'r') as file:
        content = file.readlines()
    my_ans = [line.strip() for line in content]
    return my_ans


def add_text_to_index_file(text):
    index_file_path = os.path.join(qfolder, "index.txt")
    with open(index_file_path, "a") as index_file:
        index_file.write(text + "\n")


def add_link_to_Qindex_file(text):
    index_file_path = os.path.join(qfolder, "Qindex.txt")
    with open(index_file_path, "a", encoding="utf-8", errors="ignore") as Qindex_file:
        Qindex_file.write(text + "\n")


def create_and_add_text_to_file(file_name, text):
    folder_path = os.path.join(qfolder, file_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name + ".txt")
    with open(file_path, "w", encoding="utf-8", errors="ignore") as new_file:
        new_file.write(text)




def getPagaData(url, index):
    try:
        browser.get(url)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, body_class)))
        time.sleep(1)

        heading = browser.find_element(By.CSS_SELECTOR, heading_class)
        body = browser.find_element(By.CSS_SELECTOR, body_class)

        if (heading.text):
            add_text_to_index_file(heading.text)
            add_link_to_Qindex_file(url)
            create_and_add_text_to_file(str(cnt), body.text)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False


arr = getlinks()
for link in arr:
    attempt = getPagaData(link,cnt)
    if(attempt):
        cnt = cnt + 1

browser.quit()
