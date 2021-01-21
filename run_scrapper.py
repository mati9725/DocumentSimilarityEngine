# -*- coding: utf-8 -*-

import sys
import os
sys.path.append('./AzureFunctions')
from WikiScrapper import WikiScrapper

while True:
    try:
        WikiScrapper().start_scrapping()
    except:
        pass

