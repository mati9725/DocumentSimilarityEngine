import logging
from WikiScrapper import WikiScrapper
from preprocessing import preprocess_data
import azure.functions as func
from prediction import predict
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
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
             "url is empty",
             status_code=400,
             headers={"Access-Control-Allow-Origin": "*"}
        )
    
    scrapper = WikiScrapper()
    rp = scrapper.get_robot_parser()
    text, _, errors = scrapper.scrap(query, rp)

    if errors:
        return func.HttpResponse(
             "; ".join(errors),
             status_code=400,
             headers={"Access-Control-Allow-Origin": "*"}
        )
        
    errormessage = ''
    try:
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
        logging.info(errormessage)
        
        return func.HttpResponse(
             "Unexpected error: " + errormessage,
             status_code=500,
             headers={"Access-Control-Allow-Origin": "*"}
        )

