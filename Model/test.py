from text_preprocessing import preprocess_data
from gensim.models.doc2vec import Doc2Vec
from gensim.test.utils import common_texts

titles = ['Football', 'Basketball', 'Horse', 'USA', 'Dog']

#load model
model = Doc2Vec.load("Model/d2v.model")

# Test
text = 'Balls'
data = preprocess_data(text)

inferred_vector = model.infer_vector(data)
n = model.docvecs.most_similar([inferred_vector], topn= 1)
print(titles[n[0][0]])