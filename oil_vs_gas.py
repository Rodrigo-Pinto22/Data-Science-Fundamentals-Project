import requests
import nltk
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
#from gas_price_extract import *

def extract(dates, link_url):
    html = ""         
    
    
    #extract dates
    datas = dates['tstamp']
    y = datas[0:4]
    m = datas[4:6]
    d = datas[6:8]
    h = datas[8:10]
    min = datas[10:12]
    s = datas[12:]
    #final_date = int(y+m+d)
    #final_date_list.append(final_date)
    final_date = y+"-"+m+"-"+d
    print(f"{d}/{m}/{y} at {h}:{min}:{s}")
    #extract the link to the text
    original_url = dates['linkToExtractedText']
    #print(original_url)
    #print()
    #page = urlopen(original_url)
    #print(page)
    #html_bytes = page.read()
    #html = html_bytes.decode("utf-8")
    link_url.append(original_url)

    #print(html)
    #print()
    return link_url, final_date

def main():
    topics = ["maisgasolina.com", "compareomercado.pt/precos-combustiveis-gasolina-gasoleo"]
    items = input("How many news to show? ")
    begin =20080218203700
    last =20230217011100
    url_link_to_extract = []
    link_url = []
    title_list = []
    prefinal_date_list = []
    final_date_list = []
    date_rearrange = []
    for topic in topics:
        print(f"Topic: {topic}\n")
                #https://arquivo.pt/url/search?q=maisgasolina.com&l=pt&from=19910806&to=20241106&trackingId=eca23903afbedfe2a2a7_54fd2c45a8ef017253d0&adv_and=maisgasolina.com
        url = f"https://arquivo.pt/textsearch?q={topic}&maxItems={items}&prettyPrint=true&from={begin}&to={last}"
        r = requests.get(url)

        if r.status_code == 200:
            print("Success!")
            data = r.json()
            print(data)
            for dates in data['response_items']:
                title = dates['title']
                if len(title) != 0 and not title.__contains__("301 Moved Permanently") and (title.__contains__('Mais Gasolina') or title.__contains__('Compare o Mercado')):                                                                       
                    print("PASS")
                    url_link_to_extract, dates_4_file = extract(dates, link_url)                    
                    final_date_list.append(dates_4_file)
                    title_list.append(title)
                    
                    
                    #print(new_data)
                else:
                    print("FAIL")
        else:
            print("Something is wrong")


    ziped = list(zip(final_date_list, url_link_to_extract, title_list))
    ziped.sort()
    final_date_list, url_link_to_extract, title_list = zip(*ziped)
    final_date_list = list(final_date_list)
    url_link_to_extract = list(url_link_to_extract)
    title_list = list(title_list)
    dict_search = {'Title':title_list, 'Link To Extracted Text': url_link_to_extract, 'Date': final_date_list}
    #print(dict_search)
    #print(len(title_list), len(url_link_to_extract), len(final_date_list))
    dt_search = pd.DataFrame(data = dict_search)
    dt_search.to_csv('web_search_2', index=False)
    #print(final_date_list)
    #print(dt_search.to_string())

    #Calling another script
    print(len(title_list))
if __name__ == '__main__' :
     main()