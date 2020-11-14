# Imports

import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup
import os

##### functions created in colab demo
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

