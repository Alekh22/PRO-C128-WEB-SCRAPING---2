import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("/Users/Mohit/Desktop/chromedriver")
browser.get(START_URL)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink"]
planet_data = []
def scrape():
    
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    
scrape()
new_data_planet=[]
def get_more_data(hyperlink):
    page=requests.get(hyperlink)
    soup=BeautifulSoup(page.content,"html.parser")
    for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
        td=tr_tag.find_all("td")
        temp_list=[]
        for td_tag in td:
            try:
                temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
    new_data_planet.append(temp_list)
final_planet_data=[]
for index,data in enumerate(planet_data):
    final_planet_data.append(data+new_data_planet[index])
for data in planet_data:
    get_more_data(data[5])
with open("final.csv","w")as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)

