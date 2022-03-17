from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib.request

url_export = 'https://data.stad.gent/explore/dataset/sheep-tracking-gent/export/'

# automate one launch a day

# scrape geojson file
driver = webdriver.Chrome()
driver.get(url_export)
geojson_button = driver.find_element(By.XPATH, '//div[@format-extension="geojson"]/a')
href = geojson_button.get_attribute('href')
file = urllib.request.urlopen(href)
geo = eval(file.read().decode('utf-8'))
print(f'geo {geo}')
driver.quit()

# extract values from geojson
print(type(geo))
print(geo['features'])
print(geo['features'][0]['geometry']['coordinates'])
data = eval((geo['features'][0]['properties']['data']))
print(data['name'])
print(data['time'])
print(data['source'])
print(data['state'])
print(data['address'])
print(geo['features'][0]['properties']['lat'])
print(geo['features'][0]['properties']['lng'])


# collect values in csv file 