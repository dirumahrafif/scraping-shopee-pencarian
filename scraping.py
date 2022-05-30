from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

shopee_link = "https://shopee.co.id/search?keyword=macbook"
driver.set_window_size(1300,800)
driver.get(shopee_link)

rentang = 500
for i in range(1,7):
    akhir = rentang * i 
    perintah = "window.scrollTo(0,"+str(akhir)+")"
    driver.execute_script(perintah)
    print("loading ke-"+str(i))
    time.sleep(1)

time.sleep(5)
driver.save_screenshot("home.png")
content = driver.page_source
driver.quit()

data = BeautifulSoup(content,'html.parser')
# print(data.encode("utf-8"))

i = 1
base_url = "https://shopee.co.id"

list_nama,list_gambar,list_harga,list_link,list_terjual,list_lokasi=[],[],[],[],[],[]

for area in data.find_all('div',class_="col-xs-2-4 shopee-search-item-result__item"):
    print('proses data ke-'+str(i))
    nama = area.find('div',class_="ie3A+n bM+7UW Cve6sh").get_text()
    gambar = area.find('img')['src']
    harga = area.find('span',class_="ZEgDH9").get_text()
    link = base_url + area.find('a')['href']
    terjual = area.find('div',class_="r6HknA uEPGHT")
    if terjual != None:
        terjual = terjual.get_text()
    lokasi = area.find('div',class_="zGGwiV").get_text()
    
    list_nama.append(nama)
    list_gambar.append(gambar)
    list_harga.append(harga)
    list_link.append(link)
    list_terjual.append(terjual)
    i+=1
    print("------")

df = pd.DataFrame({'Nama':list_nama,'Gambar':list_gambar,'Harga':list_harga,'Link':list_link,'Terjual':list_terjual})
writer = pd.ExcelWriter('macbook.xlsx')
df.to_excel(writer,'Sheet1',index=False)
writer.save()