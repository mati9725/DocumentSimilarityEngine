# -*- coding: utf-8 -*-

from os import listdir, remove
from os.path import isfile, join
import json
from WikiScrapper import WikiScrapper


while(True):
    try:
        wikiscrapper = WikiScrapper()
        mypath = 'urls'
        onlyfiles_gen = (join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and f != '.fakefile')
        file_path = next(onlyfiles_gen)
        
        if file_path is None:
            time.sleep(5)
            
        with open(file_path, 'r') as f:
            urls = json.load(f)  
        
        if urls is not None and len(urls) > 0:
            inserted_cnt = wikiscrapper.save_new_urls(urls, wikiscrapper.scrapper_name, force_all_to_db=True)    
            print(f"Inserted {inserted_cnt} of {len(urls)} from {file_path}")
        else:
            print(f"No urls in file {file_path}")
        
        remove(file_path)
    except:
        pass
            