# -*- coding: utf-8 -*-

# Required code to convert Colab to HTML
# %%shell
# jupyter nbconvert --to html /content/TwitterMulticalssificationCyberbulying.ipynb

import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.linear_model import LogisticRegression
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

#import seaborn as sns
#from wordcloud import WordCloud
#import matplotlib.pyplot as plt
#the required libraries for clustering
#from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.decomposition import PCA
#from sklearn.manifold import TSNE
#import collections
#from pathlib import Path
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')

"""# Load the dataset"""

def openTextasList(filename):
  with open(filename, encoding="utf8") as file_in:
    lines = []
    for line in file_in:
      # remove whitespace characters like `\n` at the end of each line
      line=line.strip()
      lines.append(line)
  return(lines)

ethnicity=openTextasList("/content/8000ethnicity.txt")
religion=openTextasList("/content/8000religion.txt")
notcb=openTextasList("/content/8000notcb.txt")
alldoc=notcb + ethnicity + religion
print("there are %d ethencity twittes\n %s " % (len(ethnicity),ethnicity[0:5]))
print("there are %d religion twittes\n %s " % (len(religion),religion[0:5]))
print("there are %d notcb twittes\n %s " % (len(notcb),notcb[0:5]))

alldoc[0:2]

# define training labels
class_label = np.array(["notcb"for _ in range(8000)] + ["ethencity"for _ in range(8000)]+["religion"for _ in range(8000)])

class_label.shape

# Construct a dataframe
# list of strings
lst = alldoc

# list of int
lst2 = class_label

# Calling DataFrame constructor after zipping
# both lists, with columns specified
df = pd.DataFrame(list(zip(lst, lst2)),
			columns =['tweet_text', 'cyberbullying_type'])
df

df['cyberbullying_type'].value_counts()

import seaborn as sns
sns.countplot(x = 'cyberbullying_type', data = df)

"""# Pre-processing

1. Convert all texts to lower case
2. Remove numbers
3. Remove contractions (websites, hashtags, numbers, links, emails)
4. Remove mentions
5. Remove punctuations
6. Remove repeating characters
7. Remove stopwords
8. Remove white spaces
9. Stemming and lemmetization
10. Tokenize
"""

df.info()

np.sum(df.isnull())

# storing the data in lists
tweet, type = list(df['tweet_text']), list(df['cyberbullying_type'])
print(tweet)

# Encoding the labels
labelencoder = LabelEncoder()

df['cyberbullying_type_encoded'] = labelencoder.fit_transform(df['cyberbullying_type'])

#df[['cyberbullying_type', 'cyberbullying_type_encoded']].value_counts()

df.cyberbullying_type_encoded = df.cyberbullying_type_encoded.replace([0,1,2], [1,0,2])

df[['cyberbullying_type', 'cyberbullying_type_encoded']].value_counts()

# converting tweet text to lower case
df['tweet_text'] = df['tweet_text'].str.lower()
df.head()

def remove_stopwords(input_text):
    stopwords_list = stopwords.words('english')
    # Some words which might indicate a certain sentiment are kept via a whitelist
    whitelist = ["n't", "not", "no"]
    words = input_text.split()
    clean_words = [word for word in words if (word not in stopwords_list or word in whitelist) and len(word) > 1]
    return " ".join(clean_words)

df.tweet_text = df["tweet_text"].apply(remove_stopwords)
df.tweet_text.head()

# cleaning and removing URLs

def clean_URLs(text):
    return re.sub(r"((www.[^s]+)|(http\S+))","",text)

df['tweet_text'] = df['tweet_text'].apply(lambda x : clean_URLs(x))
df.tweet_text.head()

def remove_mentions(input_text):
    '''
    Function to remove mentions, preceded by @, in a Pandas Series

    Parameters:
        input_text : text to clean
    Output:
        cleaned Pandas Series
    '''
    return re.sub(r'@\w+', '', input_text)

df.tweet_text = df["tweet_text"].apply(remove_mentions)
df.tweet_text.head()

# cleaning and removing numeric data

def clean_numeric(text):
    return re.sub('[0-9]+', '', text)

df['tweet_text'] = df['tweet_text'].apply(lambda x: clean_numeric(x))
df.tweet_text.head()

# cleaning and removing punctuations
english_puctuations = string.punctuation

def clean_puctuations(text):
    translator = str.maketrans('','', english_puctuations)
    return text.translate(translator)

df['tweet_text'] = df['tweet_text'].apply(lambda x : clean_puctuations(x))
df.tweet_text.head()

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

df['tweet_text'] = df['tweet_text'].apply(lambda x : deEmojify(x))
df.tweet_text.head(50)

df.tweet_text = df.tweet_text.tolist()

TokenizeText = [word_tokenize(i) for i in df.tweet_text]
for i in TokenizeText:
    print(i)

df.tweet_text = TokenizeText
print(df.tweet_text)

# lemmatization

lm = WordNetLemmatizer()

def text_lemmatization(text):
    text = [lm.lemmatize(word) for word in text]
    return text


df['tweet_text'] = df['tweet_text'].apply(lambda x: text_lemmatization(x))
print(df['tweet_text'].head(50))

df

# clean_df=df.to_csv("STA5703_cleantweets.csv")
# files.download('STA5703_cleantweets.csv')bb

df['tweet_text'] = df['tweet_text'].apply(lambda x : " ".join(x))
df

# Splitting the data
X, y = df['tweet_text'], df['cyberbullying_type_encoded']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.3, random_state= 111)

print(X.shape)
print(y.shape)
print(X_train.shape)
print(X_test.shape)

from sklearn.feature_extraction.text import CountVectorizer

BoW = CountVectorizer(ngram_range= (1,1))
x = BoW.fit_transform(df['tweet_text'])
Terms = BoW.get_feature_names()
len(Terms)

# Transforming the data using TF-IDF Vectorizer
vectoriser = TfidfVectorizer(ngram_range=(1,1), max_features= 200000)
vectoriser.fit(X_train)
print("Length of features(words): ",len(vectoriser.get_feature_names()))
Features = vectoriser.get_feature_names()
Features

# transforming the data
X_train = vectoriser.transform(X_train)
X_test = vectoriser.transform(X_test)

logit = LogisticRegression(C=5e1, solver='lbfgs', multi_class='multinomial', random_state=111, n_jobs=-1)

logit.fit(X_train, y_train)

y_prediction = logit.predict(X_test)

from sklearn import metrics
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
ConfMat = confusion_matrix(y_test, y_prediction)
display = ConfusionMatrixDisplay(confusion_matrix= ConfMat)
display.plot()
plt.show()

Accuracy = metrics.accuracy_score(y_test, y_prediction)
print(Accuracy)

