import urllib.request
import csv
import os
import time 
from typing import Optional

from .driver import Driver


class SheepScraper:
    """
    Class that interacts dynamically with the sheep whereabouts dataset 
    and stores the data in a csv-file.
    """
    
    SHEEP_DATA_URL = r'https://data.stad.gent/explore/dataset/sheep-tracking-gent/export/'
    CWD = r'C:\Users\maart\Documents\myProjects\sheep'
    FOLDER_PATH = r'csv'
    FILENAME = r'sheep_whereabouts.csv'

    def __init__(self):
        self.driver: Driver = Driver(SheepScraper.SHEEP_DATA_URL)
        self.geodata: Optional[dict] = None

    def scrape_geojson_data(self):
        geojson_webelement = self.driver.get_geojson_webelement()
        href_url = geojson_webelement.get_attribute('href')
        dynamic_file = urllib.request.urlopen(href_url)
        geo_info = eval(dynamic_file.read().decode('utf-8'))
        self.geodata = eval((geo_info['features'][0]['properties']['data']))

    def append_to_the_herd_history(self):
        csv_file_path = SheepScraper._fix_path()
        write_header = not os.path.isfile(csv_file_path)
        with open(csv_file_path, 'a', newline='') as sheep_history:
            writer_object = csv.writer(sheep_history)
            if write_header:
                writer_object.writerow([
                    "scrape time", "time", "latitude", "longitude", 
                    "name", "source", "state", "address"
                ])            
            writer_object.writerow([
                SheepScraper._get_time(), self.geodata['time'], self.geodata['lat'], self.geodata['lng'],
                self.geodata['name'], self.geodata['source'], self.geodata['state'], self.geodata['address']
            ])
            sheep_history.close()
    
    def quit_selenium_driver(self):
        self.driver.quit()
    
    @staticmethod
    def _fix_path():
        """Assures working directory is stable (also when script is run from batch file)"""
        os.chdir(SheepScraper.CWD)
        if not os.path.isdir(SheepScraper.FOLDER_PATH):
            os.mkdir(SheepScraper.FOLDER_PATH)
        return os.path.join(SheepScraper.FOLDER_PATH, SheepScraper.FILENAME)
    
    @staticmethod
    def _get_time() -> str:
        return time.strftime('%Y %b %d, %H:%M:%S', time.localtime())
