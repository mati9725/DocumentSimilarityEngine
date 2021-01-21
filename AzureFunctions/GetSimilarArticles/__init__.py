import logging
import pickle
import azure.functions as func
import re
from gensim.parsing.preprocessing import strip_punctuation, strip_multiple_whitespaces, remove_stopwords, strip_non_alphanum
from gensim.utils import tokenize
from gensim.models.doc2vec import Doc2Vec
from gensim.test.utils import common_texts
from nltk.stem import WordNetLemmatizer 
from prediction import predict
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    if not query:
        try: 
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            if not isinstance(req_body, str):
                query = req_body.get('query')
            else:
                query = req_body

# logging.info(f"text loaded: {query}")


    if not query:
        return func.HttpResponse(
             "text is empty",
             status_code=400,
             headers={"Access-Control-Allow-Origin": "*"}
        )

    errormessage = ''
    try:
        response = predict(query)

        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )

    except Exception as ex:
        logging.info("Exception thrown:")
        errormessage = ex.__str__()
        logging.info(errormessage)
        
        return func.HttpResponse(
             "Unexpected error " + errormessage,
             status_code=500,
             headers={"Access-Control-Allow-Origin": "*"}
        )
