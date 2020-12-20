import os
import pandas as pd

from text_preprocessing import preprocess_data
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import common_texts

def count_accuracy(model, data):
    correct = 0
    for i, text in enumerate(data):
        inferred_vector = model.infer_vector(text)
        n = model.docvecs.most_similar([inferred_vector], topn = 3)
        x = []
        for n_ in n:
            x.append(n_[0])
        if i in x:
            correct += 1
    return 100*correct/len(data)
    
# Load data
path = 'Model/Data/wiki_data.csv'
df = pd.read_csv(path, delimiter=';', usecols = ['text'])

# Data preprocessing
data = []
for index, row in df.iterrows():
    data.append(preprocess_data(row.text))

documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(data)]

# Training
model = Doc2Vec(documents, vector_size=600, workers=4, window=20)
model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)

# Count accuracy
acc = count_accuracy(model, data)
print(acc)

# Save model
model.save("Model/d2v.model")





