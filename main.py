from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import config
import smtplib

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


def getTextAndLinksFromWebElements(webElements):
    list = {}
    for i in webElements:
        list[i.text] = i.get_attribute("href")

    return list


"""
Collects news and blog articles from Finviz.com.
Returns the article titles and links as a dictionary
"""
def scrapeFinvizNews():
    finvizURL = 'https://finviz.com/news.ashx'
    driver = getDriverWithCookies(finvizURL)
    webElements = driver.find_elements(By.CLASS_NAME, 'nn-tab-link')

    articlesAndLinks = getTextAndLinksFromWebElements(webElements)
    driver.close()
    return articlesAndLinks


"""
Collects news and blog articles from Bloomberg.com.
Returns the article titles and links as a dictionary
"""
def scrapeBloombergNews():
    bloombergURL = 'https://www.bloomberg.com/'
    driver = getDriverWithCookies(bloombergURL)

    # Multiple elements contain news articles
    webElements = driver.find_elements(By.CLASS_NAME, 'story-list-story__info__headline')
    webElements += driver.find_elements(By.CLASS_NAME, 'single-story-module__related-story-link')

    articlesAndLinks = getTextAndLinksFromWebElements(webElements)
    driver.close()
    return articlesAndLinks

"""Sends an email using config file contents """
def sendEmail(emailContents):
    smtp_server = 'smtp.gmail.com'
    content =  f'SUBJECT: {config.message}\n\n{emailContents}'
    server = smtplib.SMTP(smtp_server, 587)
    try:
        server.ehlo()
        server.starttls()

        server.login(config.username, config.password)
        server.sendmail(config.sender, config.recipient, content)
        server.close()

    except Exception as e:
        print(e)
        server.close()


if __name__ == '__main__':
    news = {}
    news.update(scrapeFinvizNews())
    news.update(scrapeBloombergNews())

    for key, value in news.items():
        if key != None and value != None:
            print(key + " " + value)
