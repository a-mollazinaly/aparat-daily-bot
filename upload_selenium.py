import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

USERNAME = os.environ['APARAT_USERNAME']
PASSWORD = os.environ['APARAT_PASSWORD']
VIDEO_PATH = "output.mp4"
TITLE = "جمله انگیزشی روز"
CATEGORY = "۱"  # دسته‌بندی (مثلاً سرگرمی)
TAGS = "انگیزشی-موفقیت"
DESCRIPTION = "هر روز یک جمله زیبا برای شما."

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # بدون رابط گرافیکی
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

# ۱. لاگین در آپارات
driver.get("https://www.aparat.com/login")
time.sleep(2)
username_field = driver.find_element(By.NAME, "username")
password_field = driver.find_element(By.NAME, "password")
username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)
password_field.send_keys(Keys.RETURN)
time.sleep(5)

# ۲. رفتن به صفحه آپلود
driver.get("https://www.aparat.com/upload")
time.sleep(2)

# آپلود فایل
file_input = driver.find_element(By.NAME, "video_file")
file_input.send_keys(os.path.abspath(VIDEO_PATH))
time.sleep(5)  # صبر برای آپلود

# عنوان
title_input = driver.find_element(By.ID, "title")
title_input.send_keys(TITLE)

# دسته‌بندی: انتخاب از dropdown (باید ID واقعی پیدا شود)
# فعلاً یک sleep و سپس ارسال دستی
# (در عمل باید المان‌ها بررسی شوند)

# ارسال نهایی
submit_btn = driver.find_element(By.ID, "submit_button")
submit_btn.click()
time.sleep(10)

driver.quit()
