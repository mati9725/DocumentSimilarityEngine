import os
import pandas as pd

from text_preprocessing import preprocess_data, accuracy
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import common_texts
import pickle
    
# Load data
path = 'Model/Data/wiki_data.csv'
df = pd.read_csv(path)

# Data preprocessing
documents = []
for index, row in df.iterrows():
    documents.append(TaggedDocument(preprocess_data(row.text), [row.url]))

# Training
model = Doc2Vec(dm=1, dbow_words=1, vector_size=300, min_count=1, workers=4, window=5, epochs=20)
model.build_vocab(documents)
model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)

# Count accuracy
acc = accuracy(model, documents, 3)
print(acc)

# Save model
# model.save("Model/d2v.model")
pickle.dump(model, open("Model/d2v.model", "wb" ))





