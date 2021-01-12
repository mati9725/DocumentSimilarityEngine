import logging

import azure.functions as func
from os import listdir


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    logging.info(name)
    logging.info(req)
    logging.info(req.params)
    

    if name:
        files = [f for f in listdir(name)]
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully." + files)
    else:
        files = [f for f in listdir(".")]
        return func.HttpResponse(
             f"{files} This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response00:29.",
             status_code=200
        )
