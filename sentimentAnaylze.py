#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 17:11:18 2023

@author: shaymo
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

df = pd.read_csv('news.csv')

analyzer = SentimentIntensityAnalyzer()

negative = []
neutral = []
positive = []
compound = []

for n in range(df.shape[0]):
    title = df.iloc[n,0]
    snippet = df.iloc[n,2]
    title_analyzed = analyzer.polarity_scores(title)
    snippet_analyzed = analyzer.polarity_scores(snippet)
    negative.append(((title_analyzed['neg'])+(snippet_analyzed['neg']))/2)
    neutral.append(((title_analyzed['neu'])+(snippet_analyzed['neu']))/2)
    positive.append(((title_analyzed['pos'])+(snippet_analyzed['pos']))/2)
    compound.append(((title_analyzed['compound'])+(snippet_analyzed['compound']))/2)
    
df['Negative Score'] = negative
df['Neutral Score'] = neutral
df['Positive Score'] = positive
df['compound'] = compound

#lable data
score = df['compound']
sentiment = []
for i in score:
    if i>=0.05:
        sentiment.append('Positive')
    elif i <=-0.05:
        sentiment.append('Negative')
    else:
        sentiment.append('Neutral')
        
df['sentiment'] = sentiment

df.to_csv('sentiment_analysis_news.csv')
