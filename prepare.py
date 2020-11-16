import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import acquire



def basic_clean(text):
    '''
    Initial basic cleaning/normalization of text string
    '''
    # change to all lowercase
    low_case = text.lower()
    # remove special characters, encode to ascii and recode to utf-8
    recode = unicodedata.normalize('NFKD', low_case).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    # Replace anything that is not a letter, number, whitespace or a single quote
    cleaned = re.sub(r"[^a-z0-9'\s]", '', recode)
    return cleaned

def tokenize(text):
    '''
    Use NLTK TlktokTokenizer to seperate/tokenize text
    '''
    # create the NLTK tokenizer object
    tokenizer = nltk.tokenize.ToktokTokenizer()
    return tokenizer.tokenize(text, return_str=True)

def stem(text):
    '''
    Apply NLTK stemming to text to remove prefix and suffixes
    '''
    # Create the nltk stemmer object, then use it
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in text.split()]
    article_stemmed = ' '.join(stems)
    return article_stemmed

def lemmatize(text):
    '''
    Apply NLTK lemmatizing to text to remove prefix and suffixes
    '''
    # Create the nltk lemmatize object, then use it
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in text.split()]
    article_lemmatized = ' '.join(lemmas)
    return article_lemmatized

def remove_stopwords(text, extra_words=[], exclude_words=[]):
    '''
    Removes stopwords from text, allows for additional words to exclude, or words to not exclude
    '''
    # define initial stopwords list
    stopword_list = stopwords.words('english')
    # add additional stopwords
    for word in extra_words:
        stopword_list.append(word)
    # remove stopwords to exclude from stopword list
    for word in exclude_words:
        stopword_list.remove(word)
    # split the string into words
    words = text.split()
    # filter the words
    filtered_words = [w for w in words if w not in stopword_list]
    # print number of stopwords removed
    # print('Removed {} stopwords'.format(len(words) - len(filtered_words)))
    # produce string without stopwords
    article_without_stopwords = ' '.join(filtered_words)
    return article_without_stopwords

### instructor version
def prep_article_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)\
                            .apply(lemmatize)
    
    df['stemmed'] = df[column].apply(basic_clean).apply(stem)
    
    df['lemmatized'] = df[column].apply(basic_clean).apply(lemmatize)
    
    return df[['title', column, 'stemmed', 'lemmatized', 'clean']]

###### my version
def prep_data(df, column, extra_words=[], exclude_words=[]):
    '''
    This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the text article title, original text, stemmed text,
    lemmatized text, cleaned, tokenized, & lemmatized text with stopwords removed.
    '''
    # create column with text cleaned
    df['clean'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)
    # basic clean, tokenize, remove_stopwords, and stem text
    df['stemmed'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)\
                            .apply(stem)
    # basic clean, tokenize, remove_stopwords, and lemmatize text
    df['lemmatized'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)\
                            .apply(stem)
    # return only exercise requested columns
    return df[['title', column, 'clean', 'stemmed', 'lemmatized']]
