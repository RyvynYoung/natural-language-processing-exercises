# Imports

import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup
import os
# scroll down for exercise functions

##### functions created in colab demo ######
def make_soup(url):
    '''
    This helper function takes in a url and requests and parses HTML
    returning a soup object.
    '''
    # set headers and response variables
    headers = {'User-Agent': 'Codeup Data Science'} 
    response = get(url, headers=headers)
    # use BeartifulSoup to make object
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Create a list containing a dictionary, card_dict, for each each of the 11 article cards on the main blog page.
def get_card_info(card):
    '''
    This function gets summary info from each card on the main page at https://ryanorsinger.com
    returning a card dictionary with title, content, relative url, and read time
    '''
    # get these items from the card
    title = card.find('h2').text
    content = card.find('p').text
    relative_url = card.find('a').get('href')
    read_time = card.find('span', class_='reading-time')
    # make a dictionary from the items
    card_dict = {'title':title, 'content':content, 'relative_url':relative_url, 'read_time':read_time}
    return card_dict

def make_card_df(url):
    ''' Gets a list of all cards, uses get_card_info function to get the card dictionary
    then converts list of card dictionaries into a pandas df.
    '''
    # use the make_soup function to create the soup object from the url
    soup = make_soup(url)
    # make a list of all the cards on the page to get data from 
    card_list = soup.find_all('article')
    # create and empty list to hold the dictionaries
    dict_list = []
    # iterate though the list of cards using the get_card_info to collect information on cards
    for card in card_list:
        card_info = get_card_info(card)
        # add each card dictionary to the list
        dict_list.append(card_info)
    # use pandas to make the dataframe from the list of dictionaries
    card_df = pd.DataFrame(dict_list)
    # add the base_url to the df for future use
    card_df['base_url'] = url
    return card_df


def get_article_info(url):
    '''
    Takes in the url for each article and gets info on the article and creates dictionary of the info
    '''
    # use the make_soup function to create the object from the url
    soup = make_soup(url)
    # gets these items from the article
    article_title = soup.find('h1').text
    article_content = soup.find('div', class_="kg-card-markdown").text
    article_date = soup.find('time').attrs['datetime']
    art_copy = soup.find('section', class_="copyright").text
    # creates a dictionary of the info collected
    art_dict = {'art_title': article_title, 'art_content': article_content, 'art_date': article_date, 'art_copyright': art_copy}
    return art_dict

def make_article_df(card_df):
    '''
    makes the article_df and writes it to local json file for future use
    '''
    # first make column of each article url
    card_df['article_url'] = card_df.base_url + card_df.relative_url
    # get a list of these urls
    art_url_list = card_df.article_url.to_list()
    # make an empty list to hold dictionaries
    art_dict_list = []
    #iterate through list of article urls and get info for each article
    for url in art_url_list:
        art_info = get_article_info(url)
        art_dict_list.append(art_info)
    # use pandas to make a df of the article dictionaries
    article_df = pd.DataFrame(art_dict_list)
    # write the df to local for future use
    article_df.to_json('article_df.json')
    print("article.json file created use pd.read_json('article_df.json') to open the file")

####### functions created in data acquisition exercises #########

def get_blog_info(url):
    '''
    Takes in the url for article and gets info on the article and creates dictionary of the info
    '''
    # use the make_soup function to create the object from the url
    soup = make_soup(url)
    # gets these items from the article
    article_title = soup.find('title').text
    article_content = soup.find('div', class_='jupiterx-post-content').text
    article_date = soup.find('time').attrs['datetime']
    # creates a dictionary of the info collected
    art_dict = {'article_title': article_title, 'article_content': article_content, 'article_date': article_date}
    return art_dict

def get_blog(url_list):
    '''
    Get the article content for all of the urls in the lists
    '''
    # make an empty list to hold dictionaries
    art_dict_list = []
    #iterate through list of article urls and get info for each article
    for url in url_list:
        art_info = get_blog_info(url)
        art_dict_list.append(art_info)
    # use pandas to make a df of the article dictionaries
    article_df = pd.DataFrame(art_dict_list)
    # write the df to local for future use
    article_df.to_json('codeup_article_df.json')
    print("article.json file created use pd.read_json('codeup_article_df.json') to open the file")
    # for exercises adding return of dictionary list and dataframe
    return art_dict_list, article_df


####### from instructor ##########
# Helper function that scrapes the blog urls from the main codeup blog page.

def get_all_urls():
    '''
    This function scrapes all of the Codeup blog urls from
    the main Codeup blog page and returns a list of urls.
    '''
    # The base url for the main Codeup blog page
    url = 'https://codeup.com/resources/#blog'
    
    # Make request and soup object using helper
    soup = make_soup(url)
    
    # Create a list of the anchor elements that hold the urls.
    urls_list = soup.find_all('a', class_='jet-listing-dynamic-link__link')
    
    # I'm using a set comprehension to return only unique urls because list contains duplicate urls.
    urls = {link.get('href') for link in urls_list}

    # I'm converting my set to a list of urls.
    urls = list(urls)
        
    return urls

# Function to create a DataFrame of article, title, and content and write to a json file.

def get_blog_articles(urls, cached=False):
    '''
    This function takes in a list of Codeup Blog urls and a parameter
    with default cached == False which scrapes the title and text for each url, 
    creates a list of dictionaries with the title and text for each blog, 
    converts list to df, and returns df.
    If cached == True, the function returns a df from a json file.
    '''
    if cached == True:
        df = pd.read_json('big_blogs.json')
        
    # cached == False completes a fresh scrape for df     
    else:

        # Create an empty list to hold dictionaries
        articles = []

        # Loop through each url in our list of urls
        for url in urls:

            # Make request and soup object using helper
            soup = make_soup(url)

            # Save the title of each blog in variable title
            title = soup.find('h1').text

            # Save the text in each blog to variable text
            content = soup.find('div', class_="jupiterx-post-content").text

            # Create a dictionary holding the title and content for each blog
            article = {'title': title, 'content': content}

            # Add each dictionary to the articles list of dictionaries
            articles.append(article)
            
        # convert our list of dictionaries to a df
        df = pd.DataFrame(articles)

        # Write df to a json file for faster access
        df.to_json('big_blogs.json')
    
    return df

def get_news_articles(cached=False):
    '''
    This function with default cached == False does a fresh scrape of inshort pages with topics 
    business, sports, technology, and entertainment and writes the returned df to a json file.
    cached == True returns a df read in from a json file.
    '''
    # option to read in a json file instead of scrape for df
    if cached == True:
        df = pd.read_json('articles.json')
        
    # cached == False completes a fresh scrape for df    
    else:
    
        # Set base_url that will be used in get request
        base_url = 'https://inshorts.com/en/read/'
        
        # List of topics to scrape
        topics = ['business', 'sports', 'technology', 'entertainment']
        
        # Create an empty list, articles, to hold our dictionaries
        articles = []

        for topic in topics:
            
            # Create url with topic endpoint
            topic_url = base_url + topic
            
            # Make request and soup object using helper
            soup = make_soup(topic_url)

            # Scrape a ResultSet of all the news cards on the page
            cards = soup.find_all('div', class_='news-card')

            # Loop through each news card on the page and get what we want
            for card in cards:
                title = card.find('span', itemprop='headline' ).text
                author = card.find('span', class_='author').text
                content = card.find('div', itemprop='articleBody').text

                # Create a dictionary, article, for each news card
                article = ({'topic': topic, 
                            'title': title, 
                            'author': author, 
                            'content': content})

                # Add the dictionary, article, to our list of dictionaries, articles.
                articles.append(article)
            
        # Create a DataFrame from list of dictionaries
        df = pd.DataFrame(articles)
        
        # Write df to json file for future use
        df.to_json('articles.json')
    
    return df