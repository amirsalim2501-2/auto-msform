from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import datetime
import time
import smtplib
from email.mime.text import MIMEText
import requests
import os

FORM_URL = "https://forms.office.com/Pages/ResponsePage.aspx?id=HsTJsIjXVEOtfFIw_igOHbLbLDXy-79Ft9IFo9pI4bNUQkNCWktLQ1VWMFdEM0tTWTUyVVFSWjVYVy4u"  # link form kamu

def fill_dropdown(driver, question_number, text):
    # dropdown = driver.find_element(By.XPATH, f"(//button[@role='combobox'])[{question_number}]")
    # dropdown.click()
    # time.sleep(1)
    # driver.find_element(By.XPATH, f"//div[@role='option']//span[text()='{text}']").click()
    
    # klik dropdown Nama
    dropdown = driver.find_element(By.XPATH, "//div[@role='button' and @aria-haspopup='listbox']")
    dropdown.click()
    time.sleep(1)  # tunggu opsi muncul

def select_radio(driver, text):
    driver.find_element(By.XPATH, f"//label[contains(@class,'office-form-question-choice-label')]//span[text()='{text}']").click()

def fill_answers(driver):
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)  # WIB
    weekday = now.weekday()  # 0=Senin, …, 4=Jumat
    hour = now.hour

    # Nama (dropdown) — asumsikan pertanyaan “Nama” adalah dropdown nomor 1
    fill_dropdown(driver, 1, "A")

    # Choose one → In / Out
    if hour == 8:
        choose_one = "In"
    else:
        choose_one = "Out"
    # select_radio(driver, choose_one)

    # Work → WFO / WFH
    if weekday in [0,1,2]:  # Senin–Rabu
        work = "WFO"
    else:  # Kamis–Jumat
        work = "WFH"
    # select_radio(driver, work)

def send_email_notif():
    EMAIL_SENDER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_TARGET = "emailtujuan@gmail.com"  # GANTI
    msg = MIMEText("Form Microsoft telah terisi otomatis.")
    msg["Subject"] = "Notifikasi Automasi Form"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_TARGET

    s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    s.login(EMAIL_SENDER, EMAIL_PASS)
    s.send_message(msg)
    s.quit()

def send_wa_notif():
    FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")
    WA_TARGET = "628xxxxxxxxxx"  # ganti nomor WA
    if not FONNTE_TOKEN:
        return
    headers = {"Authorization": FONNTE_TOKEN}
    data = {"target": WA_TARGET, "message": "Form berhasil diisi otomatis."}
    requests.post("https://api.fonnte.com/send", headers=headers, data=data)

def fill_form():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(FORM_URL)
    time.sleep(3)

    fill_answers(driver)

    # klik tombol Submit / Kirim
    driver.find_element(By.XPATH, "//button[contains(.,'Submit') or contains(.,'Kirim')]").click()
    time.sleep(2)
    driver.quit()

    send_email_notif()
    send_wa_notif()

    print("Form berhasil diisi otomatis pada", datetime.datetime.now())

if __name__ == "__main__":
    fill_form()
