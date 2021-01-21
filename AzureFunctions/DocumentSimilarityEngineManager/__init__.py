import logging
import os
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read() \
            .replace("$$ENGINE_URL$$", os.environ['ENGINE_URL'])
    logging.info(html)

    return func.HttpResponse(
            html,
            status_code=200,
            mimetype="text/html"
    )
