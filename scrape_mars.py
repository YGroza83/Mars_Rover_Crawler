from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    one_py_dict ={}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title =soup.find("div", "list_text").get_text()
    news_body = soup.find("div", "article_teaser_body").get_text()
    news_title = news_title.replace(news_body, '')
    one_py_dict['news_title'] = news_title
    one_py_dict['news_body'] = news_body
    
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    relative_url =soup.find("img", "headerimage")["src"]
    featured_image_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/" + relative_url
    one_py_dict['featured_image_url'] = featured_image_url

    tables = pd.read_html('https://space-facts.com/mars/')[0].to_html()
    one_py_dict['tables'] = tables

    hemisphere_image_urls=[]
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    for i in range(4):
        links = browser.links.find_by_partial_text('Enhanced') 
        links[i].click()
        tmp1 = browser.title
        tmp1 = tmp1.replace(' | USGS Astrogeology Science Center', '')
        browser.links.find_by_text('Sample').click()
        time.sleep(1)
        tmp2 = browser.windows[i+1].url
        tmp_dict = {"title": tmp1, "img_url": tmp2}
        hemisphere_image_urls.append(tmp_dict)
        browser.back()
    one_py_dict['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return one_py_dict

