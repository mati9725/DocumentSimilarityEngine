import re
from gensim.parsing.preprocessing import strip_punctuation, strip_multiple_whitespaces, remove_stopwords, strip_non_alphanum
from gensim.utils import tokenize
from nltk.stem import WordNetLemmatizer 

def preprocess_data(text):
    #delete [x]
    text = re.sub('\[\d{1,3}\]', '', text)
    #strip non alphanumeric
    text = strip_non_alphanum(text)
    #lowercase
    text = text.lower()
    #delete punctuation
    text = strip_punctuation(text)
    #strip multiple whitespaces
    text = strip_multiple_whitespaces(text)
    #remove stopwords
    text = remove_stopwords(text)
    #tokenization
    text = text.split(' ')
    return text

def accuracy(model, document, topn):
    correct = 0
    for tag in document:
        inferred_vector = model.infer_vector(tag[0])
        n = model.docvecs.most_similar([inferred_vector], topn=topn)
        x = []
        for n_ in n:
            x.append(n_[0])
        if tag[1][0] in x:
            correct += 1
    return 100*correct/len(document)