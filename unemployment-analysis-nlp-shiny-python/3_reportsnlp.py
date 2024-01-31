# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:08:47 2022

@author: saiom
"""

import os
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import nltk
from nltk import word_tokenize, pos_tag
from textblob import TextBlob
import wordcloud
from wordcloud import WordCloud, STOPWORDS
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('spacytextblob');
nltk.download('brown')
nltk.download('punkt')


count = 0

reports_path = os.getcwd() + '/reports'
figures_path = os.getcwd() + '/plots'
cleaned_data_path = os.getcwd() + '/cleaned_data' 


report_names = os.listdir(reports_path)

sentiment_table = pd.DataFrame(columns = ['Report Date', 'Polarity', 'Subjectivity'])

def read_reports(file_path, fname):   
    pdf = PyPDF2.PdfFileReader(os.path.join(file_path, fname))
    text = []
    for pnum in range(pdf.getNumPages()):
        page = pdf.getPage(pnum)
        text.append(page.extractText())
    return text[0]

def get_senti_scores(text):
    nlp_text = nlp(text)
    text_polarity_value = nlp_text._.blob.polarity
    text_subjectivity_value = nlp_text._.blob.subjectivity
    return text_polarity_value, text_subjectivity_value

    
def generate_table(count, fname, polarity, subjectivity):
    sentiment_table.loc[count] = [fname, polarity, subjectivity]
    

def plot_sentiment(table, sentiment_type):
    table.plot(x = 'Report Date', y = sentiment_type, kind = 'bar')    
    plt.title('Sentiment trend from Employment Situation News Release ')

    plt.savefig(os.path.join(figures_path, fname + sentiment_type + 'trend.png'))

  

def get_words(text):
    text = TextBlob(text) 
    words = []
    for np in text.noun_phrases:
        words.append(np)
    return words


def generate_wordcloud(fname, text):
    text = [item.text.strip().lower().replace(' ', '_') for item in text]
    text = ' '.join(text)
    stopwords = set(STOPWORDS)
    more_words = ['percent', 'gov', 'bls', '_', 
                  'www', '_www', '_bls','gov_', 'news_release', 
                  'economic_news', 'cps_ces','news']
    stopwords.update(more_words)
    wordcloud = WordCloud(width = 1600, height = 800,
                          background_color ='Black',
                          stopwords = stopwords,
                          min_font_size = 10, 
                          include_numbers = True, 
                          prefer_horizontal = 1,
                          max_words= 1500,
                          margin = 0,
                          mode = 'RGBA',
                          contour_color= 'firebrick').generate_from_text(text)
    
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud,interpolation = 'bilinear')
    plt.axis("off")
    plt.title('Word cloud from Employment Situation News Release : ' + fname)
    plt.savefig(os.path.join(figures_path, fname + '_wordcloud.png'))





for fname in report_names:
    text = read_reports(reports_path, fname)
    polarity, subjectivity = get_senti_scores(text)
    generate_table(count, fname.rsplit('.', 1)[0], polarity, subjectivity)
    words = get_words( text)
    generate_wordcloud(fname.rsplit('.',1)[0], list(nlp(text)))
    count += 1
    
    
plot_sentiment(sentiment_table, 'Polarity')
plot_sentiment(sentiment_table, 'Subjectivity')
sentiment_table.to_csv(os.path.join(cleaned_data_path, '2022_sentiment_table.csv'))
    

