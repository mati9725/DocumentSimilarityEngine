import logging
import pickle
import azure.functions as func
import re
from gensim.parsing.preprocessing import strip_punctuation, strip_multiple_whitespaces, remove_stopwords, strip_non_alphanum
from gensim.utils import tokenize
from gensim.models.doc2vec import Doc2Vec
from gensim.test.utils import common_texts
from nltk.stem import WordNetLemmatizer 
import json

def main(req: func.HttpRequest, pickledmodel: func.InputStream) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            if not isinstance(req_body, str):
                text = req_body.get('text')
            else:
                rext = req_body


    logging.info(f"text loaded: {text}")
    if not text:
        return func.HttpResponse(
             "text argument is empty or not found",
             status_code=400,
             headers={"Access-Control-Allow-Origin": "*"}
        )

    errormessage = ''
    try:
        logging.info(type(pickledmodel))
        model = pickle.load(pickledmodel)
        logging.info("model loaded")

        data = preprocess_data(text)
        logging.info(f"text preprocessed: {data}")
        
        # Inferr vector
        inferred_vector = model.infer_vector(data)
        logging.info(f"inferred_vector")

        n = model.docvecs.most_similar([inferred_vector], topn = 15)
        logging.info(n)

        return func.HttpResponse(
            json.dumps(n),
            status_code=200,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )

    except Exception as ex:
        logging.info("Exception thrown MW:")
        logging.info(ex.__str__())
        errormessage = ex.__str__()
        
        return func.HttpResponse(
             "Unexpected error " + errormessage,
             status_code=500,
             headers={"Access-Control-Allow-Origin": "*"}
        )

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
