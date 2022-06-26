from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
import datetime as dt


def scrape_all():
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph, 
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    

    browser.quit()
    return data



def mars_news(browser):
    
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    news_soup = bs(html, 'html.parser')

    try:
    
        slide_elem = news_soup.select_one('div.list_text')

        news_title = slide_elem.find('div', class_='content_title').get_text()

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p


def featured_image(browser):

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = bs(html, 'html.parser')

    try:
    
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        
    except AttributeError:
        return None
    
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url



def mars_facts():
    
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        
    except BaseException:
        return None
    
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()


def hemispheres(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_img_urls = []

    html = browser.html
    hemisphere_soup = bs(html, 'html.parser')


    hemis = hemisphere_soup.find('div', class_="item")

    for x in range(0,4):
        hemispheres = {}
        
        full_image_elem = hemis.find('img', class_='thumb')
        
        full_image_elem = browser.find_by_tag('h3')[x]
        full_image_elem.click()
        
        html = browser.html
        img_soup = bs(html, 'html.parser')
        
        img_elem = img_soup.find('div', class_='downloads')
        img_url_rel = img_elem.find('a').get('href')
        img_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{img_url_rel}'
        
        
        title = img_soup.find('h2', class_="title").get_text()
        
        hemispheres = {
            'img_url': img_url, 
            'title' : title
        }
        
        hemisphere_img_urls.append(hemispheres)

        
        browser.back()

    return hemisphere_img_urls



if __name__ == "__main__":
    print(scrape_all())