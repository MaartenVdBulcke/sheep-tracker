from selenium import webdriver
from selenium.webdriver.common.by import By


class Driver:
    """
    Class that instatiates a driver session. Upon initialization, 
    the sheep data webpage is automatically loaded. 

    Params
    ------
    sheep_data_url: str
        Weblink to the sheep database webpage 
    """
    def __init__(self, sheep_data_url: str):
        self.driver = webdriver.Chrome()
        self.driver.get(sheep_data_url)
    
    def get_geojson_webelement(self):
        return self.driver.find_element(By.XPATH, '//div[@format-extension="geojson"]/a')

    def quit(self):
        self.driver.quit()
