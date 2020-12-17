import os
from text_preprocessing import preprocess_data
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.test.utils import common_texts

# Data Preprocessing
files = []
path = 'Model/Data'
for filename in os.listdir(path): 
    files.append(os.path.join(path, filename))

data = []
for file in files:
    f = open(file, "r")
    data.append(preprocess_data(f.read()))

documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(data)]

# Training
max_epochs = 300
model = Doc2Vec(documents, vector_size=100, window=2, min_count=1, workers=4)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)

# Save model
model.save("Model/d2v.model")





