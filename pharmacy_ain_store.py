from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

chrome_options = Options()
chrome_options.add_argument("--headless")  # Menjalankan tanpa tampilan browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

base_url = "https://store.ainj.co.jp/all/"

def scrape_page(url):
    driver.get(url)

    time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    cards = soup.find_all('li', class_='break-words border-t border-horizontal-line text-sm leading-5.5 first-of-type:border-0 md:py-3 px-0')

    print(f"Jumlah cards di halaman {url}: {len(cards)}")
    
    extracted_data = []
    for card in cards:
        shop_info = {
            "name": card.find('h2', class_='text-lg font-semibold leading-6 md:text-xl md:leading-7').text.strip(),
            "address": card.find('p', class_='justify-center break-words text-text').text.strip(),
            "phone_number": card.find('a', href=True, text="電話する").text.strip(),
            "business_status": card.find('p', class_='mr-4').text.strip(),
        }

        shop_url = "https://store.ainj.co.jp" + card.find('a', class_='absolute left-0 top-0 h-full w-full')['href']
    

        shop_info["shop_url"] = shop_url

        extracted_data.append(shop_info)

    return extracted_data

page_number = 1
all_shop_data = []

while True:
    page_url = f"{base_url}?page={page_number}"
    print(f"Memproses halaman: {page_url}")
    
    page_data = scrape_page(page_url)
    
    if not page_data:
        print("Tidak ada data lebih lanjut, berhenti scraping.")
        break
    
    all_shop_data.extend(page_data)
    page_number += 1 

csv_filename = 'pharmacy_ain_store.csv'
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ["name", "address", "phone_number", "business_status", "shop_url"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_shop_data)

print(f"Data berhasil disimpan ke dalam file {csv_filename}")

print(f"Total data yang berhasil dikumpulkan: {len(all_shop_data)}")

driver.quit()
