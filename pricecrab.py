from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import pandas as pd

print("WebDriver başlatılıyor...")
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--headless") # arka planda halletmek için
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.maximize_window()

main_page_url = "https://coinmarketcap.com/all/views/all"
limit = 200 # çünkü 200 var bir sayfada

print(f"'{main_page_url}' açılıyor...")
driver.get(main_page_url)

try:
    print("Sayfa verisi bekleniyor...")
    next_data_script = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
    )
    print("Veri bulundu, çekiliyor...")

    json_data_string = next_data_script.get_attribute('textContent')
    data = json.loads(json_data_string)

    print("Gömülü 'initialState' verisi ayrıştırılıyor...")
    initial_state_string = data['props']['initialState']
    initial_state_data = json.loads(initial_state_string)

    print("JSON verisi başarıyla ayrıştırıldı.")

except Exception as e:
    print(f"HATA: Sayfa yüklenirken veya __NEXT_DATA__ bulunurken sorun oluştu: {e}")
    driver.quit()
    exit()

crypto_data_list = []
try:
    listing_data = initial_state_data['cryptocurrency']['listingLatest']['data']

    keys = listing_data[0]['keysArr']
    name_index = keys.index('name')
    symbol_index = keys.index('symbol')
    price_index = keys.index('quote.USD.price')

    crypto_rows = listing_data[1:]

    print(f"JSON içinde {len(crypto_rows)} kripto bulundu. İlk {limit} tanesi işleniyor...")

    for i, crypto_list in enumerate(crypto_rows):
        if i >= limit:
            break

        try:
            name = crypto_list[name_index]
            symbol = crypto_list[symbol_index]
            price = crypto_list[price_index]

            formatted_price = f"${price:,.2f}" if price is not None else "N/A"

            crypto_data_list.append({"Coin Adı": f"{name} ({symbol})", "Fiyat": formatted_price})

        except Exception as inner_e:
            print(f"Uyarı: {i + 1}. kripto verisi işlenirken hata: {inner_e}")
            continue

except KeyError as e:
    print(f"HATA: JSON yapısı değişmiş olabilir. Beklenen anahtar bulunamadı: {e}")
except Exception as e:
    print(f"HATA: Kripto verileri JSON'dan çekilirken beklenmedik hata: {e}")
finally:
    driver.quit()


print("--------------------------------------------------")
print(f"\nToplam {len(crypto_data_list)} adet kripto paranın verisi başarıyla çekildi.")

if crypto_data_list:
    df = pd.DataFrame(crypto_data_list)
    print("\n--- ÇEKİLEN FİYATLAR (Pandas DataFrame) ---")
    print(df.to_string(index=False))
else:
    print("\nHiç veri çekilemedi.")

print("\nİşlem tamamlandı.")