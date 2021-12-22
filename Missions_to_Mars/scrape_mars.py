#!/usr/bin/env python
# coding: utf-8

# ## This is a Missions to Mars Web Scaping Project

#Import Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from splinter import Browser
import pandas as pd
import time


    
def scrape():
    
    #Setup Chrome driver(splinter)
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # ## *Scrape Top Article Title and Teaser Body

    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(5)
    html=browser.html
    soup=bs(html,'html.parser')


    # Retrieve the latest news title
    news_title=soup.find_all('div', class_='content_title')[0].text
    # Retrieve the latest news paragraph
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text
    #Retrieve Date of article release
    news_date = soup.find_all('div', class_='list_date')[0].text
    #Display news Title, article teaser body and article date
    print("This is the latest article found on http://redplanetsceince.com/")
    print(news_title)
    print(news_p)
    print(news_date)





    # ## Obtain Featured Image URL from https://spaceimages-mars.com

    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)


    #This is kind of redundant knowing that there is only one featured image, but for the practice of for loop:)
    for x in range(5):

        html2 = browser.html
        soup = bs(html2, 'html.parser')
        results = soup.find_all('img', class_='headerimage fade-in')
    results
    image_url = results[0]['src']
    image_url


    #Combine url2 and image_url to get full featured_image url
    featured_image_url = url2+image_url
    print("Featured Image URL: " + featured_image_url)


    # ## Obtain HTML Table for Mars Facts

    #Go to third url3 and import the data into pandas dataframe
    url3 = "https://galaxyfacts-mars.com"
    browser.visit(url3)


    html3 = browser.html
    table_mars = pd.read_html(url3)[1]

    table_mars


    table_mars.columns = ['mars_parameter', 'mars_value']
    table_mars.set_index('mars_parameter', inplace=True)
    #return table_mars


    table_mars=table_mars.to_html(classes='table table-striped')
    #table_mars1


    table_mars.replace('\n','')
    #print(table_mars1)


    # ## Scrape https://marshemispheres.com/ and Obtain Hemisphere Image URLs

    # Scrape https://marshemispheres.com/ url to obtain information on Mars hemispheres 
    url4='https://marshemispheres.com/'
    browser.visit(url4)
    html=browser.html
    soup=bs(html,'html.parser')


    # Use BeautifulSoup to get basic breakdown on 4 hemispheres
    mars_hemispheres=soup.find('div',class_='collapsible results')
    mars_parts=mars_hemispheres.find_all('div',class_='item')
    hemisphere_image_urls=[]
    #return mars_parts


    hemisphere_image_urls = []
    for item in mars_parts:
        try:
            #Obtain title of each hemisphere description
            hemisphere = item.find('div', class_='description')
            title = hemisphere.h3.text
            #print(title)
            #Obtain hemispheres image url
            hemi_url = hemisphere.a['href']
            hemi_add_url = url4+hemi_url
            print(hemi_add_url)
            browser.visit(hemi_add_url)
            html4 = browser.html
            soup = bs(html4, 'html.parser')
            img_url = url4 + soup.find('img', class_='wide-image')['src']
            if title and img_url:
                hemisphere_dict = {"title": title, "img_url": img_url}
                
                print('-'*100)
                print(f"Title is: " + title)
                print(f"Full Image URL is: " + img_url)
                print('-'*100)
                
            hemisphere_image_urls.append(hemisphere_dict)
                
        except Exception as error:
            print(error)
        #print(hemi_add_url)

    
    #return hemisphere_image_urls


    # ## Create Dictionary for Mongo DB

    # Dictionary of all scraped data
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_table":table_mars,
        "hemisphere_image_urls":hemisphere_image_urls
    }


    
    browser.quit()
    return mars_dict
if __name__ == '__main__':
    scrape()







