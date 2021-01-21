import logging
import validators
import azure.functions as func
from prediction import predict
from WikiScrapper import WikiScrapper
from urllib.parse import urlparse
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info('Python HTTP trigger function processed a request.')

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

        if not query:
            return func.HttpResponse(
                "query is empty",
                status_code=400,
                headers={"Access-Control-Allow-Origin": "*"}
            )


            errormessage = ''
        try:
            text, errors = query2text(query)
            if errors:
                return func.HttpResponse(
                    "; ".join(errors),
                    status_code=400,
                    headers={"Access-Control-Allow-Origin": "*"}
                )

            response = predict(text)

            return func.HttpResponse(
                json.dumps(response),
                status_code=200,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )

        except Exception as ex:
            logging.info("Exception thrown:")
            errormessage = ex.__str__()
            logging.info(ex)
            
            return func.HttpResponse(
                "Unexpected error " + errormessage,
                status_code=500,
                headers={"Access-Control-Allow-Origin": "*"}
            )
    except Exception as ex:
        logging.info('Entire function exception.')
        logging.info(ex)

            

def query2text(query):
    if validators.url(query.strip()):
        logging.info("Scrapping url query")
        
        url = query
        url_domain = urlparse(url).netloc
        
        scrapper = WikiScrapper()
        rp = scrapper.get_robot_parser()
        allowed_domain = urlparse(rp.url).netloc
        if url_domain != allowed_domain:
            return None, [f"Given URL is not allowed. Only URLs from {allowed_domain} are allowed."]
        
        text, _, errors = scrapper.scrap(url, rp)
    else:
        logging.info("Searching by query as plain search phrase")
        errors = []
        text = query

    return text, errors
