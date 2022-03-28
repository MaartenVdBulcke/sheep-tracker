from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request
import csv
import os
import time 


class SheepScraper:
    
    URL_EXPORT = r'https://data.stad.gent/explore/dataset/sheep-tracking-gent/export/'
    CWD = r'C:\Users\maart\Documents\myProjects\sheep'
    FOLDER_PATH = r'csv'
    FILENAME = r'sheep_whereabouts.csv'

    def __init__(self):
        pass

    def scrape_geojson(self):
        driver = webdriver.Chrome()
        driver.get(SheepScraper.URL_EXPORT)
        geojson_button = driver.find_element(By.XPATH, '//div[@format-extension="geojson"]/a')
        href = geojson_button.get_attribute('href')
        file = urllib.request.urlopen(href)
        geo = eval(file.read().decode('utf-8'))
        driver.quit()
        self.geojson: dict = eval((geo['features'][0]['properties']['data']))

    def append_to_the_herd_history(self):
        csv_file_path = SheepScraper.__fix_path()
        write_header = not os.path.isfile(csv_file_path)

        with open(csv_file_path, 'a', newline='') as sheep_history:
            writer_object = csv.writer(sheep_history)
            if write_header:
                writer_object.writerow(
                    [
                        "scrape time", "time", "latitude", "longitude", 
                        "name", "source", "state", "address"
                    ]
                )
            
            SheepScraper.__freeze_now_time(self)

            writer_object.writerow(
                [
                    self.nowtime, self.geojson['time'], self.geojson['lat'], self.geojson['lng'],
                    self.geojson['name'], self.geojson['source'], self.geojson['state'], self.geojson['address']
                ]
            )
            
            sheep_history.close()
    
    @staticmethod
    def __fix_path():
        os.chdir(SheepScraper.CWD)
        if not os.path.isdir(SheepScraper.FOLDER_PATH):
            os.mkdir(SheepScraper.FOLDER_PATH)
        return os.path.join(SheepScraper.FOLDER_PATH, SheepScraper.FILENAME)

    def __freeze_now_time(self):
        t = time.localtime()
        self.nowtime: str = time.strftime('%Y %b %d, %H:%M:%S', t)
    