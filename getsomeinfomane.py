import tkinter as tk
from tkinter import scrolledtext, END, font as tkFont
from tkinter import messagebox
import threading
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options


def update_text_widget(text_widget, content, clear_first=False):
    try:
        text_widget.config(state=tk.NORMAL)
        if clear_first:
            text_widget.delete('1.0', END)
        text_widget.insert('end', content)
        text_widget.config(state=tk.DISABLED)
        text_widget.see(END)
    except tk.TclError:
        pass


def fetch_wikipedia_data(name, text_widget):
    driver = None
    try:
        update_text_widget(text_widget, f"'{name}' bilgileri yükleniyor...\nLütfen bekleyin...",
                           clear_first=True)

        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        driver.get("https://tr.wikipedia.org/wiki/")

        elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "cdx-text-input__input")))
        elem.send_keys(name)
        elem.send_keys(Keys.RETURN)

        try:
            h1_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.TAG_NAME, "h1"))
            )

            if "Arama sonuçları" in h1_element.text:
                update_text_widget(text_widget, "\nBeklediğiniz için teşekkür ederiz...\n")

                first_result_xpath = "//ul[contains(@class, 'mw-search-results')]//li[1]//a"
                first_link = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, first_result_xpath))
                )

                clicked_title = first_link.text
                update_text_widget(text_widget, f"'{clicked_title}' yazılıyor...\n\n")
                first_link.click()

            else:
                update_text_widget(text_widget, "\nBuyrunuz.\n\n")

        except TimeoutException:
            print("Sayfa başlığı hızlı bulunamadı, doğrudan içerik aranıyor.")
            pass

        paragraphs_xpath = "//*[@id='mw-content-text']//p"
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, paragraphs_xpath))
        )

        paragraflar = driver.find_elements(By.XPATH, paragraphs_xpath)

        full_text = ""
        for p in paragraflar:
            paragraf_metni = p.text.strip()
            if paragraf_metni:
                full_text += paragraf_metni + "\n\n"

        update_text_widget(text_widget, full_text, clear_first=True)

    except TimeoutException:
        update_text_widget(text_widget,
                           f"HATA: Sayfa yüklendi ancak '{name}' için paragraf metni bulunamadı (Timeout). Aradığınız kelimeden emin olun.",
                           clear_first=True)
    except StaleElementReferenceException:
        update_text_widget(text_widget, "HATA: Sayfa çok hızlı değişti (Stale Element). Lütfen tekrar deneyin.",
                           clear_first=True)
    except Exception as e:
        if "invalid command name" not in str(e):
            update_text_widget(text_widget, f"Ana metin veya paragraflar bulunurken hata oluştu: {e}", clear_first=True)
    finally:
        if driver:
            driver.quit()
            print("Selenium sürücüsü kapatıldı.")


def on_search_click():
    name = entry.get()
    if not name.strip():
        update_text_widget(text_widget, "Lütfen bir arama terimi girin.", clear_first=True)
        return

    thread = threading.Thread(target=fetch_wikipedia_data, args=(name, text_widget))
    thread.daemon = True
    thread.start()


root = tk.Tk()
root.title("İnformatik")

window_width = 800
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Arial", size=10)
root.option_add("*Font", default_font)

top_frame = tk.Frame(root, pady=10, bg="#f0f0f0")
top_frame.pack(fill='x')

tk.Label(top_frame, text="Aranacak Konu:", bg="#f0f0f0").pack(side=tk.LEFT, padx=(10, 5))
entry = tk.Entry(top_frame, width=50, font=("Arial", 11))
entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5, ipady=4)

search_button = tk.Button(top_frame, text="Bilgileri Getir", command=on_search_click, font=("Arial", 10, "bold"),
                          bg="#007bff", fg="white", relief=tk.FLAT, padx=10, pady=2)
search_button.pack(side=tk.LEFT, padx=10)

entry.bind("<Return>", lambda event: on_search_click())

bottom_frame = tk.Frame(root)
bottom_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))

scrollbar = tk.Scrollbar(bottom_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget = tk.Text(bottom_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Arial", 11), state=tk.DISABLED,
                      relief=tk.SOLID, borderwidth=1, padx=5, pady=5)
text_widget.pack(side=tk.LEFT, fill='both', expand=True)

scrollbar.config(command=text_widget.yview)

info_title = "İnformatik'e hoşgeldiniz!"
info_message = (
    "Bu program, girdiğiniz konu hakkında kapsamlı bilgiler verir.\n\n"
    "Nasıl Çalışır:\n"
    "1. Arama kutusuna bir konu yazın (örn: 'Ali Koç' veya 'Rasputin').\n"
    "2. 'Bilgileri Getir' butonuna veya 'Enter' tuşuna basın.\n"
    "3. Program, makaleyi arka planda halledecek.\n\n"
)
messagebox.showinfo(info_title, info_message)

root.mainloop()

