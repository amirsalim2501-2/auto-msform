# ==========================================================
# AUTOMASI PENGISIAN MICROSOFT FORM (SESUAIKAN DENGAN FORM KAMU)
# ==========================================================

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


# ==========================================================
# === GANTI DENGAN LINK FORM KAMU ==========================
# ==========================================================
FORM_URL = "https://forms.office.com/Pages/ResponsePage.aspx?id=HsTJsIjXVEOtfFIw_igOHbLbLDXy-79Ft9IFo9pI4bNUQkNCWktLQ1VWMFdEM0tTWTUyVVFSWjVYVy4u"  # <-- WAJIB GANTI


# ==========================================================
# === FUNGSI PENGISIAN FORM ================================
# ==========================================================

def fill_dropdown(driver, question_number, text):
    """Select dropdown by visible text."""
    dropdown = driver.find_element(By.XPATH, f"(//div[contains(@class,'office-form-question-choice-container')]//i[contains(@class,'ms-Icon--ChevronDown')])[{question_number}]")
    dropdown.click()
    time.sleep(1)
    driver.find_element(By.XPATH, f"//span[text()='{text}']").click()


def select_radio(driver, text):
    """Click radio button by label text."""
    driver.find_element(By.XPATH, f"//div[@role='radio']//span[text()='{text}']").click()


# ==========================================================
# === LOGIKA JAWABAN SESUAI HARI DAN JAM ===================
# ==========================================================

def fill_answers(driver):
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)  # WIB
    weekday = now.weekday()  # 0=Mon, 4=Fri
    hour = now.hour          # 8 pagi atau 17 sore

    # =================
    # FIELD 1: Nama
    # =================
    fill_dropdown(driver, 1, "A")

    # =================
    # FIELD 2: Choose one (In/Out)
    # =================
    if hour == 8:
        choose_one = "In"
    else:
        choose_one = "Out"

    select_radio(driver, choose_one)

    # =================
    # FIELD 3: Work (WFO/WFH)
    # =================
    if weekday in [0,1,2]:  # Senin–Rabu
        work = "WFO"
    else:
        work = "WFH"

    select_radio(driver, work)



# ==========================================================
# === NOTIF EMAIL ==========================================
# ==========================================================
EMAIL_SENDER = os.getenv("i_amir@agate.id")
EMAIL_PASS = os.getenv("Suplexcity123")
EMAIL_TARGET = "amirsalim2501@gmail.com"   # <-- GANTI EMAIL TUJUAN

def send_email_notif():
    msg = MIMEText("Microsoft Form berhasil diisi otomatis.")
    msg["Subject"] = "Automasi Berhasil"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_TARGET

    smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp.login(EMAIL_SENDER, EMAIL_PASS)
    smtp.send_message(msg)
    smtp.quit()



# ==========================================================
# === NOTIF WHATSAPP =======================================
# ==========================================================
FONNTE_TOKEN = os.getenv("FONNTE_TOKEN")
WA_TARGET = "6281388340805"    # <-- GANTI NOMOR WA

def send_wa_notif():
    if not FONNTE_TOKEN:
        return
    headers = {"Authorization": FONNTE_TOKEN}
    data = {
        "target": WA_TARGET,
        "message": "Microsoft Form berhasil diisi otomatis.",
    }
    requests.post("https://api.fonnte.com/send", headers=headers, data=data)



# ==========================================================
# === MAIN PROCESS =========================================
# ==========================================================
def fill_form():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=chrome_options)

    driver.get(FORM_URL)
    time.sleep(3)

    fill_answers(driver)

    # Klik submit
    driver.find_element(By.XPATH, "//button[contains(.,'Submit') or contains(.,'Kirim')]").click()
    time.sleep(2)

    driver.quit()

    # Notifikasi
    send_email_notif()
    send_wa_notif()



if __name__ == "__main__":
    fill_form()
