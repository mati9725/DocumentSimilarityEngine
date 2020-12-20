from text_preprocessing import preprocess_data
from gensim.models.doc2vec import Doc2Vec
from gensim.test.utils import common_texts

import pandas as pd

# load data
path = 'Model/Data/wiki_data.csv'
df = pd.read_csv(path, delimiter=';', usecols = ['url'])

#load model
model = Doc2Vec.load("Model/d2v.model")

# Test
file_path = 'Model/Data/1.txt'
f = open(file_path, "r")
text = f.read()
data = preprocess_data(text)

inferred_vector = model.infer_vector(data)
n = model.docvecs.most_similar([inferred_vector], topn= 3)
print(df.iloc[n[0][0]])
print(df.iloc[n[1][0]])
print(df.iloc[n[2][0]])