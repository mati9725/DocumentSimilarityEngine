from text_preprocessing import preprocess_data
from gensim.models.doc2vec import Doc2Vec
from gensim.test.utils import common_texts
import pprint

import pandas as pd

#load model
model = Doc2Vec.load("Model/d2v.model")

# Load test data
file_path = 'Model/Data/1.txt'
f = open(file_path, "r")
text = f.read()
data = preprocess_data(text)

# Inferr vector
inferred_vector = model.infer_vector(data)
n = model.docvecs.most_similar([inferred_vector], topn = 15)

# Print output
for n_ in n:
    print(n_)