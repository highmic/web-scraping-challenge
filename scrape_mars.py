from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
import time 

#Initialize Browser:
#set time to sleep with timer prevent browser overlap and to ensure end-to-end application performance 

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser= init_browser()

    #NASA Mars News Scrape
    mars_news_url = 'https://mars.nasa.gov/news'
    response = requests.get(mars_news_url)
    soup = BeautifulSoup(response.text, 'lxml')
    #add next lines into Mission_to_Mars_dict
    news_title= soup.find('div', class_='content_title').text
    news_p= soup.find('div', class_='rollover_description_inner').text

    #JPL Mars Space Images 
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    base_url = "https://www.jpl.nasa.gov"
    time.sleep(3)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    browser.click_link_by_partial_text("more info")
    time.sleep(2)
    image_html=browser.html
    soup = BeautifulSoup(image_html, "lxml")
    image = soup.find("img", class_="main_image")['src']
    #add next lines into Mission_to_Mars_dict
    feature_image_url = base_url + image

    #Mars Weather Tweet
    twt_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twt_url)
    time.sleep(5)
    mars_weather = browser.find_by_css('#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-1tlfku8.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div > div > div > div:nth-child(3) > section > div > div > div > div:nth-child(1) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(2) > div:nth-child(1) > div > span')
    #add next line to Mission_to_mars_dict
    mars_weather_twt = mars_weather[0].text

    #Mars Facts
    marsfacts_url = 'https://space-facts.com/mars/'
    browser.visit(marsfacts_url)
    time.sleep(5)
    marsfacts_data = pd.read_html(marsfacts_url, index_col=None)
    marsfacts_data_df = marsfacts_data[0]
    marsfacts_data_df.rename(columns = {0:"description",1:"value"}, inplace=True)
    marsfacts_data_df.set_index("description", inplace=True)
    marsfacts = marsfacts_data_df.to_html()

    
    #Mars Hemispheres Images 
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)
    html= browser.html
    time.sleep(2)
    soup_usgs = BeautifulSoup(html, 'html.parser')
    mars_hemisphere =[]
    usgs_base_url = 'https://astrogeology.usgs.gov'
    results = soup_usgs.find_all('div', class_='description')
    for result in results:
        link = result.find('a', class_='product-item')
        href= link['href']
        title = link.find('h3').text
        partial_link = usgs_base_url + href
        response1 = requests.get(partial_link)
        soup_usgs1 = BeautifulSoup(response1.text, 'html.parser')
        images = soup_usgs1.find_all('div', class_='downloads')
        for image in images:
            full_url = image.find('a')['href']
            mars_hemisphere.append({'title':title,'image_url':full_url})
    #add mars_hemisphere ln 61 to dictionary


    Mission_to_mars_dict = {"News_Title":news_title,"News_Text":news_p,"Featured_Image":feature_image_url,
                            "Mars_Tweet":mars_weather_twt,"More_Facts":marsfacts,
                            "Hemisphere_Images":mars_hemisphere}
    browser.quit()
    return Mission_to_mars_dict
    






