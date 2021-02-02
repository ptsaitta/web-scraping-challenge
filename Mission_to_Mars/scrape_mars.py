import pandas as pd
from bs4 import BeautifulSoup as soup
from splinter import Browser
import time
import requests



def scrape_new_data():
    #start up browser
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    #store scraped data in dictionary
    data = {
        "News_title": title
        "News_paragraph": blurb
        "Featured_image": featured_image(browser)
        "Mars Facts": mars_facts()
        "Hemispheres": hemispheres(browser)
    }

    #quite browser after scraping and return scraped data
    browser.quit()
    return data


