# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 21:43:20 2020

@author: mati9
"""


import requests
import bs4 as bs
import urllib.robotparser
import time
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from DbHelper import DbHelper
from sqlalchemy import insert, or_
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

class WikiScrapper:
    # nltk.download('stopwords')
    # nltk.download('punkt')
    
    # porterStemmer = PorterStemmer()
    # stopwords = set(stopwords.words('english'))
    
    def __init__(self):
        self.db_helper = DbHelper()
        self.session = Session(self.db_helper.engine, autocommit=False)
        self.scrapper_name = self.db_helper.db_config['scrapper_name']
        if self.scrapper_name is None or self.scrapper_name == '':
            raise Exception("scrapper_name in db configuration must be defined")
        
        self.appconfig_refresh = None
        self.appconfig = None
        self.refresh_config()
        
        self.print_trace = False #for debugging
    
    def scrap(self, url, robotparser):
        errors = []
        if not robotparser.can_fetch("*", url):
            errors.append("Url disallowed. Content from this URL could not be scrapped.")
        # if url in result_dict:
        #     errors.append(f'Duplicate skipped: {url}')
        #     continue
        if url is None:
            errors.append('Empty url ignored')
        
        if len(errors)>0:
            return None, None, errors
        
        response = requests.get(url)
        if response.status_code != 200:
            errors.append(f'Request error. Status {response.status_code}.  {response.text}')
        
        if len(errors)>0:
            return None, None, errors
    
        soup = bs.BeautifulSoup(response.text, 'html.parser')
        body_children = soup.select('#bodyContent div.mw-parser-output>:not(p.mw-empty-elt)')
        
        text = ''
        for element in body_children:
            if str(element.name) == 'p': # we need first series of paragraphs
                text += element.text + " "
            elif len(text) > 0:
                break
        
        urls = []
        for a in soup.select('#bodyContent div.mw-parser-output a:not(.new)'):
            new_url = a.get('href')
            if new_url is None:
                continue
            if not new_url.startswith('/'):
                continue #skip links to another sites and #cite links
            if not robotparser.can_fetch("*", url):
                continue # skip if link forbidden with robots.txt
            
            full_new_url = 'https://' + robotparser.host + new_url
            if full_new_url in urls:
                continue
            
            urls.append(full_new_url)
        return text, urls, errors
    
    def get_url(self, min_refetch_time, scrapper_name):
        wiki_data = self.db_helper.wiki_data
        
        record = self.session.query(wiki_data) \
            .filter(or_(wiki_data.text == None, wiki_data.text == '')) \
            .filter( wiki_data.errors == None) \
            .filter( wiki_data.picked_date == None) \
            .filter( wiki_data.scrapper_name == scrapper_name) \
            .order_by(wiki_data.Id.desc()).first()
            
        if record is None:
            record = self.session.query(wiki_data) \
                .filter(or_(wiki_data.text == None, wiki_data.text == '') ) \
                .filter( wiki_data.errors == None) \
                .filter( wiki_data.picked_date == None) \
                .order_by(wiki_data.Id.desc()).first()

        if record is None:
            record = self.session.query(wiki_data) \
                .filter(or_(wiki_data.text == None, wiki_data.text == '') ) \
                .filter( wiki_data.errors == None) \
                .filter( 
                    or_(wiki_data.picked_date == None,
                     wiki_data.picked_date < (datetime.now() - timedelta(seconds=min_refetch_time)))) \
                .order_by(wiki_data.Id.desc()).first()
        
        if record is None:
            record = self.session.query(wiki_data) \
                .filter(or_(wiki_data.text == None, wiki_data.text == '') ) \
                .filter( 
                    or_(wiki_data.picked_date == None,
                     wiki_data.picked_date < (datetime.now() - timedelta(seconds=min_refetch_time)))) \
                .order_by(wiki_data.Id.desc()).first()
        
        if(record is not None):
            self.session.query(wiki_data) \
                .filter_by(Id = record.Id) \
                .update({wiki_data.scrapper_name: scrapper_name, wiki_data.picked_date: datetime.now()})
            
            return record.url
        else:
            return None
            
    def save_new_urls(self, new_urls, scrapper_name, force_all_to_db=False):
        if not force_all_to_db and self.appconfig["save_mode"] == 'local':
            filename = f"urls/{datetime.now()}.json".replace('-','_').replace(' ', '_').replace(':','_')
            with open(filename, 'w') as f:
                json.dump(new_urls,f)
            return 0
        
        else:
            self.session.commit()
            new_urls_count = -1 if force_all_to_db \
                else self.appconfig["new_urls_count"]
                
            if new_urls_count == 0:
                return -1 #to mark, that in this site colud be new urls to scrap
            
            existing_urls = [x[0].lower() for x in self.session.query(self.db_helper.wiki_data.url).all()]
            
            if new_urls is None or len(new_urls) == 0:
                return 0
            new_urls = [new_url.lower() for new_url in set(new_urls)]
            new_urls = [new_url for new_url in new_urls if new_url not in existing_urls]
            
            if new_urls is None or len(new_urls) == 0:
                return 0
            new_urls = set(new_urls)
            
            modifier = 1
            if(new_urls_count > 0):
                if new_urls_count < len(new_urls):
                    modifier = -1
                new_urls = list(new_urls)[:new_urls_count]
            
            to_insert = [self.db_helper.wiki_data(url=new_url) for new_url in new_urls]
            
            offset = 0
            batch_size = 1000
            while offset < len(to_insert):
                try:
                    self.session.bulk_save_objects(to_insert[offset:offset+batch_size])
                    offset += batch_size
                    self.session.commit()
                except Exception as ex:
                    self.session.rollback()
                    if(batch_size > 1):
                        batch_size = int(batch_size/2)
                        print(f"Warning! Reducing batch size to {batch_size}")
                    else:
                        print("Error when inserting new URLs", ex)
                        return offset
                
            return len(new_urls)*modifier
            # for new_url in set(new_urls):
            #     if new_url in existing_urls:
            #         continue
                
            #     try:
            #         sql = insert(self.db_helper.wiki_data) \
            #             .values(url=new_url,  scrapper_name = scrapper_name)
                        
            #         self.db_helper.engine.execute(sql)
            #     except Exception as ex:
            #         msg = f"Error when inserting {new_url}. Url skipped."
            #         errors.append(msg)
            #         print(msg, ex)
            # return errors
        
    def save_scrap(self, url, text, errors, urls_saved, scrapper_name):
        wiki_data = self.db_helper.wiki_data
        record = self.session.query(wiki_data) \
            .filter(wiki_data.url == url) \
            .first()
        
        if text is None or text.strip() == '':
            text = None
            errors.append("Empty text could not be inserted")
        
        if record is None:
            print(f"Not found record with url {url} to update text")
            return
        
        if record.text is not None and record.scrapper_name:
            print(f"Conflict with scrapper {record.scrapper_name} for URL {url}. Record will not be updated")
        
        errors_str = str(record.errors) if errors is not None and len(errors) > 0 \
            else None
        
        self.session.query(wiki_data) \
            .filter_by(Id = record.Id) \
            .update({wiki_data.scrapper_name: scrapper_name, 
                     wiki_data.text: text, 
                     wiki_data.errors: errors_str, 
                     wiki_data.urls_saved: urls_saved })

    def refresh_config(self):
        if self.appconfig_refresh is None \
           or self.appconfig_refresh < datetime.now()-timedelta(seconds=30):
            self.appconfig = {x.key:x.value for x in self.session.query(self.db_helper.app_config).all()}
            self.appconfig_refresh = datetime.now()
            
            self.appconfig['min_refetch_time'] = float(self.appconfig['min_refetch_time'])
            self.appconfig['crawl_delay'] = float(self.appconfig['crawl_delay'])
            self.appconfig['new_urls_count'] = int(self.appconfig['new_urls_count'])
            
    def preprocess(self, text):
        text = text.strip().lower()
        text = re.sub(r'  +', ' ', text)
        # text = ''.join([char for char in text if char not in string.punctuation])
        
        words = word_tokenize(text)
        words = [word for word in words if word.isalpha()] #removing punctuation marks
        words = [word for word in set(words) if word not in WikiScrapper.stopwords]
        # words = [porterStemmer.stem(word) for word in words]
        
        text = ' '.join(words)

        return text
        
    def get_robot_parser(self):
        rp = urllib.robotparser.RobotFileParser(self.appconfig['robots.txt_url'])
        rp.read()
        return rp
        
    def start_scrapping(self):
        self.refresh_config()
        rp = self.get_robot_parser()
        
        crawl_delay = rp.crawl_delay("*")
        if crawl_delay is None : 
            crawl_delay = self.appconfig['crawl_delay']
        
        self.session.commit()
        counter = 0
        avg=0
        while True:
            # self.session.begin()
            if self.appconfig["pause"].lower() == str(True).lower():
                print("Running paused with in-db config")
                time.sleep(5)
                self.refresh_config()
                continue
            
            url = self.get_url(self.appconfig['min_refetch_time'], self.scrapper_name)
            if(url is None):
                print(f"URL to scrap not found {datetime.now()}")
                time.sleep(crawl_delay)
                continue
            else:
                print(f'scrapping... avg sleep time: {avg}')

            if self.print_trace: print(f"Got URL {url}")

            text, new_urls, errors = self.scrap(url, rp)
            scrap_datetime = datetime.now()
            if self.print_trace: print(f"Got text {text}")
            
            urls_saved = self.save_new_urls(new_urls, self.scrapper_name)
            if self.print_trace: print(f"Urls saved {new_urls}")
    
            # text = self.preprocess(text)
            # if self.print_trace: print("Preprocessing finished")
            
            self.save_scrap(url, text, errors, urls_saved, self.scrapper_name)
            if self.print_trace: print("Text saved")
            
            self.refresh_config()
            if self.print_trace: print("Config refreshed")
    
            self.session.commit()
            
            next_request_min_datetime = (scrap_datetime + timedelta(seconds=crawl_delay))
            counter += 1
            now = datetime.now()
            sleep_time = (next_request_min_datetime - now).total_seconds()
            avg = (avg*(counter-1)+sleep_time)/counter
            
            if now < next_request_min_datetime:
                if self.print_trace: print(sleep_time)
                time.sleep(sleep_time)


# WikiScrapper().start_scrapping()






