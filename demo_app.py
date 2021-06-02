import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import urllib.request
from re import sub, match
import nltk
from nltk.corpus import stopwords
from PIL import Image
from io import BytesIO
from wordcloud import WordCloud, ImageColorGenerator

with st.echo(code_location='below'):
    books = pd.read_csv("goodreads_books.csv")
    nltk.download('stopwords')
    sw = stopwords.words('english')
    words = []

    for text in books["description"]:
        if type(text) == type(float("nan")):
            continue
        text = text.lower()
        text = sub(r'\[.*?\]', '', text)
        text = sub(r'([.!,?])', r' \1 ', text)
        text = sub(r'[^a-zA-Z.,!?]+', r' ', text)
        text = [i for i in text.split() if i not in sw]
        for word in text:
            words.append(word)

    word_freq = nltk.FreqDist([i for i in words if len(i) > 2])
    # plt.figure(figsize=(16, 6))
    # word_freq.plot(50)

    book_img = 'https://www.pinclipart.com/picdir/middle/365-3651885_book-black-and-white-png-peoplesoft-learn-peoplesoft.png'
    with urllib.request.urlopen(book_img) as url:
        f = BytesIO(url.read())
    img = Image.open(f)

    mask = np.array(img)
    img_color = ImageColorGenerator(mask)

    wc = WordCloud(background_color='white',
                   mask=mask,
                   max_font_size=2000,
                   max_words=2000,
                   random_state=42)
    wcloud = wc.generate_from_frequencies(word_freq)
    plt.figure(figsize=(16, 10))
    plt.axis('off')
    plt.imshow(wc.recolor(color_func=img_color), interpolation="bilinear")
    plt.show()

