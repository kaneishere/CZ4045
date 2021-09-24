import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
  

# Data Import
data = pd.read_json('reviewSelected100.json',lines=True, 
                    orient='records',encoding = "ISO-8859-1")

# Select business b1 and prepare B1
uniqueBusiness = data['business_id'].unique()
b1 = uniqueBusiness[0]
B1 = data.loc[data['business_id'] == b1]
B1 = pd.DataFrame(B1, columns = ['text'])
B1.rename(columns={"text": "unstemmed_text"}, inplace = True)

# Stemming
ps = PorterStemmer()
B1['stemmed_text'] = B1['unstemmed_text'].apply(lambda x: ps.stem(x))

# Word Frequency Before Stemming
countsBefore = B1.unstemmed_text.str.split(expand=True).stack().value_counts()

plt.plot(countsBefore.head(10))
plt.yscale("log")

# Word Frequency After Stemming
countsAfter = B1.stemmed_text.str.split(expand=True).stack().value_counts()

plt.plot(countsBefore.head(10))
plt.yscale("log")

# =================================================================================

# Select business b2 and prepare B2
uniqueBusiness = data['business_id'].unique()
b2 = uniqueBusiness[1]
B2 = data.loc[data['business_id'] == b2]
B2 = pd.DataFrame(B2, columns = ['text'])
B2.rename(columns={"text": "unstemmed_text"}, inplace = True)

# Stemming
ps = PorterStemmer()
B2['stemmed_text'] = B2['unstemmed_text'].apply(lambda x: ps.stem(x))

# Word Frequency Before Stemming
countsBefore = B2.unstemmed_text.str.split(expand=True).stack().value_counts()

plt.plot(countsBefore.head(10))
plt.yscale("log")

# Word Frequency After Stemming
countsAfter = B2.stemmed_text.str.split(expand=True).stack().value_counts()

plt.plot(countsBefore.head(10))
plt.yscale("log")

