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
pageurl = "https://leetcode.com/problemset/all/?page="



def get_a_tags(link) :

    browser.get(link)
    time.sleep(7)

    reqEle = browser.find_elements(By.TAG_NAME,"a")
    ans = []


    for i in reqEle :
        try :
            if "/problems/" in i.get_attribute("href"):
                ans.append(i.get_attribute("href"))

        except :
            pass

    ans = list(set(ans)) #removing duplicates
    return ans
    


def make_file(arr) :

    file_path = "problems.txt"
    with open(file_path, 'a' if os.path.exists(file_path) else 'w') as file:
        for link in arr:
            file.write(link + "\n")
        file.close()


my_ans = []

for i in range(1,57) :
    xx = pageurl + str(i)
    my_ans += (get_a_tags(xx))

my_ans = list(set(my_ans))
make_file(my_ans)

browser.quit()



# halt = WebDriverWait(driver,12)
# halt.until(EC.presence_of_all_elements_located(('a',url)))