from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By


""" 
Takes in a URL that is the desired website to scrape
Gathers all cookies from the website, and adds them to the driver
Returns driver
"""
def getDriverWithCookies(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    cookies = driver.get_cookies()
    for cookie in cookies:
        driver.add_cookie(cookie)

    return driver


"""
Collects news and blog articles from Finviz.com.
Returns the articles as a 
"""
def scrapeNewsFromFinviz():
    finvizURL = 'https://finviz.com/news.ashx'
    driver = getDriverWithCookies(finvizURL)
    newsAndBlogs = driver.find_elements(By.CLASS_NAME, "nn-tab-link")

    for title in newsAndBlogs:
        print(title.text)

    driver.close()


def scrapeNewsFromBloomberg():
    bloombergURL = 'https://www.bloomberg.com/'
    driver = getDriverWithCookies(bloombergURL)
    newsArticles = driver.find_elements(By.CLASS_NAME, "hub-main")

    for title in newsArticles:
        print(title.text)

    driver.close()

if __name__ == '__main__':
    scrapeNewsFromFinviz()
    scrapeNewsFromBloomberg()
