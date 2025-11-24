import os
import time
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# --- NOTIF WA FONNTE ---
def send_wa(message):
    token = os.getenv("FONNTE_TOKEN")
    if not token:
        print("FONNTE_TOKEN tidak ditemukan, WA tidak dikirim.")
        return

    url = "https://api.fonnte.com/send"

    payload = {
        "target": os.getenv("WA_TARGET", "08xxxxxxxxxx"),  
        "message": message,
    }

    headers = {
        "Authorization": token
    }

    try:
        requests.post(url, data=payload, headers=headers)
        print("Notifikasi WA terkirim.")
    except Exception as e:
        print("Gagal kirim WA:", e)


# --- SETUP SELENIUM ---
def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)


# --- FILL DROPDOWN ---
def select_dropdown(driver, placeholder_text, select_value):
    dropdown = driver.find_element(
        By.XPATH, f"//span[@aria-label='{placeholder_text}']/ancestor::div[@role='button']"
    )
    dropdown.click()
    time.sleep(1)

    option = driver.find_element(
        By.XPATH, f"//div[@role='option']//span[text()='{select_value}']"
    )
    option.click()
    time.sleep(1)


# --- FILL RADIO BUTTON ---
def select_radio(driver, label_text):
    element = driver.find_element(By.XPATH, f"//span[text()='{label_text}']")
    element.click()
    time.sleep(1)


# --- MAIN FILL ---
def fill_form():
    FORM_URL = "https://forms.office.com/Pages/ResponsePage.aspx?id=HsTJsIjXVEOtfFIw_igOHbLbLDXy-79Ft9IFo9pI4bNUQkNCWktLQ1VWMFdEM0tTWTUyVVFSWjVYVy4u"

    driver = start_driver()
    driver.get(FORM_URL)
    time.sleep(3)

    hari = datetime.datetime.now().weekday()  # 0=Senin ... 4=Jumat
    jam = datetime.datetime.now().hour

    # --- LOGIKA JAWABAN ---
    nama = "A"

    if hari <= 2:  
        work = "WFO"
    else:
        work = "WFH"

    choose = "in" if jam < 12 else "out"

    # --- ISI NAMA (dropdown) ---
    # Placeholder awal biasanya huruf default misal "B"
    select_dropdown(driver, placeholder_text="B", select_value=nama)

    # --- CHOOSE (radio) ---
    select_radio(driver, choose)

    # --- WORK (radio) ---
    select_radio(driver, work)

    # --- SUBMIT ---
    submit = driver.find_element(By.XPATH, "//button[@type='submit' or @aria-label='Submit']")
    submit.click()
    time.sleep(3)

    driver.quit()

    send_wa(f"Form Microsoft otomatis berhasil diisi.\nNama: {nama}\nChoose: {choose}\nWork: {work}")


# --- RUN ---
if __name__ == "__main__":
    fill_form()
