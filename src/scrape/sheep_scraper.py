import os
from pathlib import Path
import time 
import urllib.request
import csv
from .driver import Driver


class SheepScraper:
    """Class that interacts dynamically with the sheep whereabouts dataset 
    and stores the data in a csv-file."""
    
    SHEEP_DATA_URL = r'https://data.stad.gent/explore/dataset/sheep-tracking-gent/export/'

    def __init__(self):
        self.csv_path = self._get_csv_path()
        self.driver: Driver = Driver(SheepScraper.SHEEP_DATA_URL)
        self.geodata: dict = {}

    def _get_csv_path(self, folder_path: str = 'csv', filename: str = 'sheep_whereabouts.csv'):
        """Assures csv_path is stable (also when script is run from batch file)"""
        scrape_path = Path(os.path.abspath(os.path.dirname(__file__)))
        root = os.path.abspath(scrape_path.parent.parent)
        os.chdir(root)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        return os.path.join(folder_path, filename)

    def scrape_geojson_data(self):
        geojson_webelement = self.driver.get_geojson_webelement()
        href_url = geojson_webelement.get_attribute('href')
        dynamic_file = urllib.request.urlopen(href_url)
        geo_info = eval(dynamic_file.read().decode('utf-8'))
        self.geodata = eval((geo_info['features'][0]['properties']['data']))

    def append_to_the_herd_history(self):
        write_header = not os.path.isfile(self.csv_path)
        with open(self.csv_path, 'a', newline='') as sheep_history:
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
    def _get_time() -> str:
        return time.strftime('%Y %b %d, %H:%M:%S', time.localtime())
