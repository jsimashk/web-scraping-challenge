from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

mars_collection = {}


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    #executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    executable_path = {"executable_path": "C:/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    scrape_nasa_info()
    scrape_featured_image()
    scrape_twitter()
    scrape_space_facts()
    scrape_astrogeology()

    return mars_collection



def scrape_nasa_info ():
    url = 'https://mars.nasa.gov/news'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    #results = soup.find_all('div', class_="image_and_description_container")
    
    results = soup.find_all('div', class_="content_title")
    news_title = results[0].text

    results = soup.find_all('div', class_="rollover_description_inner")
    news_p = results[0].text

    mars_collection["title"]=news_title
    mars_collection["news"]=news_p

def scrape_featured_image():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://www.jpl.nasa.gov"
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    button = browser.find_by_id('full_image')
    button.click()
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    button = browser.find_link_by_partial_text('more info')
    button.click()
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    # Interact with elements
    relative_image_path = soup.find_all('img', class_="main_image")[0]["src"]
    img_url = base_url + relative_image_path

    browser.quit()
    
    mars_collection["featured_img"]=img_url

def scrape_twitter():
    response = requests.get("https://twitter.com/marswxreport?lang=en")
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_="js-tweet-text-container")[0]
    p = results.find('p').text
    
    mars_collection["weather_info"]=p

def scrape_space_facts():
    response = requests.get("https://space-facts.com/mars/")
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('tr')

    
    mars_facts = []
    i = 0

    # Loop through returned results
    while 1:
        # Error handling
        try:
            measure = results[i].find_all('td')[0].text
            value = results[i].find_all('td')[1].text
            mars_facts.append({"measure":measure, "value":value})
            i = i + 1
        except IndexError as e:
            break

    df = pd.DataFrame(mars_facts)
    html = df.to_html()
    
    mars_collection["facts_table"]=html

def scrape_astrogeology():
    browser = init_browser()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov"
    browser.visit(url)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    i = 0
    
    titles = []
    hemisphere_image_urls = []
    
    #find number of images
    count = soup.find_all('div', class_='accordian')[0].find('span').text.split()[0]
    count = int(count)
    
    while i < count:
        title = soup.find_all('div', class_='collapsible results')[0].find_all('h3')[i].text
        titles.append(title)
        i = i + 1
    
    #print (titles)
    
    i = 0
    
    while i < count:
        link = browser.find_link_by_partial_text('Enhanced')[i]
        link.click()
        
        html = browser.html
        soup = bs(html, "html.parser")
        
        relative_image_path = soup.find_all('img', class_='wide-image')[0]["src"]
        img_url = base_url + relative_image_path
        
        #print (img_url)
        
        mars_collection["hem_title"+str(i)]=titles[i]
        mars_collection["hem_img_url"+str(i)]=img_url
        
        browser.back()
        
        i = i + 1
        
    browser.quit() 

    
