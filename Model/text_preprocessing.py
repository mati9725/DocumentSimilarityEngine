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
    #delate punctuation
    text = strip_punctuation(text)
    #strip multiple whitespaces
    text = strip_multiple_whitespaces(text)
    #remove stopwords
    text = remove_stopwords(text)
    # # Lemmatization
    # lemmatizer = WordNetLemmatizer()
    # text = lemmatizer.lemmatize(text) 
    #tokenization
    text = text.split(' ')
    return text