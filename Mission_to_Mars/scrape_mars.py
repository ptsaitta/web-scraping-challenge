import pandas as pd
from bs4 import BeautifulSoup as soup
from splinter import Browser
import time
import requests



def scrape_new_data():
    #start up browser
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    mars_title, mars_blurb = mars_news_nasa(browser)

    #store scraped data in dictionary
    data = {
        "News_title": mars_title
        "News_blurb": mars_blurb
        "Featured_image": featured_image(browser)
        "Mars Facts": mars_facts()
        "Hemispheres": hemispheres(browser)
    }

    #quit browser after scraping and return scraped data
    browser.quit()
    return data

def mars_news_nasa(browser):
    
    #Go to NASA website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #convert html to soup
    html = browser.html
    NASA_soup = soup(html, "html.parser")

    #If an error occurs, the whole thing won't work, so I should do try/except so it can handle this
    try:
        slide = NASA_soup.select_one("ul.item_list li.slide")

    #Title is anchored div class="content_title"
        slide.find("div", class_="content_title")

    #Target locked, but there is extra text/tags we don't want. Cleaning...
        dirty_title = slide.find("div", class_="content_title")
        title = dirty_title.get_text()

    #Bingo. Now we need accompanying story blurb, found in div class_="article_teaser_body", cleaned too
        blurb = slide.find("div", class_="article_teaser_body")
        blurb = blurb.get_text()
    
    #except errors for both title and blurb, returning none if encountered
    except (AttributeError, TypeError):
        return None, None
    
    #return scraped data
    return mars_title, mars_blurb

def featured_image(browser):
    #visit url
    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_2)

    #click on full image
    full_img = browser.links.find_by_partial_text('FULL IMAGE')
    full_img.click()

    #time so next click doesn't execute before page can load
    time.sleep(3)

    #click on more info
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()
    time.sleep(3)

    #parse with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        rel_img_url = soup.find('figure', class_='lede').a['href']

    except AttributeError:
        return None

    featured_image_url = f'https://www.jpl.nasa.gov{rel_img_url}'

    return featured_image_url
