import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    with open("index.html", "r") as f:
        html = f.read()

    return func.HttpResponse(
            html,
            status_code=200,
            mimetype="text/html"
    )
