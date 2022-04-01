############################################################################################
# this script will scrape information from of the 400 franchises in www.franchisetimes.com #
############################################################################################

from selenium import webdriver
from helium import  *
from bs4 import BeautifulSoup
import requests
import re
import lxml
import time

payload = {
    'bl': '1111254',
    'o': 0,
    'l': 25,
    'f': 'json',
    'altf': 'widget',
}

url = 'https://www.franchisetimes.com/search/'

url_list = []
for offset in range(0, 400, 25):
    payload['o'] = offset
    response = requests.get(url, params=payload)
    data = response.json()
    for item in data['assets']:
        url_list.append(item['url'])

for i in range(0,len(url_list)):
    sales2 = "nd"
    url = url_list[i]
       
    while True:
        time.sleep(i//2)
        browser = start_firefox(url, headless=True)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        soup2 = soup.get_text("|", strip=True)
        soup2 = str(soup2)
        soup3 = str(soup)
        if soup.title != None:
            break
        else:
            #print("loop recaptcha -> sleep ", str(i//2), " seconds")
            browser.close()
            browser.quit()

    start = end = "hoverinfo"
    try:
        sales = re.search('hoverinfo(.*)hoverinfo', str(soup))
        sales1 = sales.group(1)
        sales2 = str(sales1)
        sales3 = re.findall('(\[.*?\])+', sales2)
        sales4 = sales3[1][1:-1]
        sales5 = re.findall(r'([a-z]{1,4}|\d{1,3}(,\d{3})+)+', sales4)
        #sales2 = re.findall(r'(\d{1,3}(,\d{3})+)+', str(sales.group(1)))
    except:
        pass
    
    last_year_rank = soup2[soup2.find("Last Year Rank")+16:].split('|')[0]
    investment_range = soup2[soup2.find("Investment Range")+18:].split('|')[0]
    initial_investment = soup2[soup2.find("Initial Investment")+20:].split('|')[0]
    category = soup2[soup2.find("Category")+10:].split('|')[0]
    company_description = soup2[soup2.find("Company Description")+20:].split('|')[0]
    global_sales = soup2[soup2.find("Global Sales")+14:].split('|')[0]
    us_units = soup2[soup2.find("US Units")+10:].split('|')[0]
    international_units = soup2[soup2.find("International Units")+21:].split('|')[0]
    sales_growth = soup2[soup2.find("Sales Growth %")+16:].split('|')[0]
    unit_growth = soup2[soup2.find("Unit Growth %")+15:].split('|')[0]

    soupero = str(soup.title.text)
    soupero_lista = soupero.split("|")
    soupero_lista = soupero_lista[0].split(".")

    print("Rank:", soupero_lista[0])
    print("Name:", soupero_lista[1][1:])
    print("Last Year Rank:", last_year_rank)
    print("Investment Range:", investment_range)
    print("Inicial Investment:", initial_investment)
    print("Category:", category)
    print("Company Description:", company_description)
    print("Global Sales:", global_sales)
    print("US Units:", us_units)
    print("International Units:", international_units)
    print("Sales Growth:", sales_growth)
    print("Unit Growth:", unit_growth)
    
    if sales2 == "nd":
        print("Sales 2016: no data")
        print("Sales 2017: no data")
        print("Sales 2018: no data")
        print("Sales 2019: no data")
        print("Sales 2020: no data")
    else:
        print("Sales 2016:", sales5[0][0])
        print("Sales 2017:", sales5[1][0])
        print("Sales 2018:", sales5[2][0])
        print("Sales 2019:", sales5[3][0])
        print("Sales 2020:", sales5[4][0])
    print("")
    browser.close()
    browser.quit()
