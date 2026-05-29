import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = os.environ['APARAT_USERNAME']
PASSWORD = os.environ['APARAT_PASSWORD']
VIDEO_PATH = os.path.abspath("output.mp4")

today = datetime.now().strftime("%Y/%m/%d")
TITLE = f"جمله انگیزشی روز - {today}"
CATEGORY_INDEX = 0   # صفر برای اولین دسته، در صورت نیاز عوض شود
TAGS = "انگیزشی,جمله روز,موفقیت"
DESCRIPTION = "هر روز یک جمله زیبا برای روحیه شما.\nلطفاً با لایک و حمایت مالی از ما حمایت کنید."

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--lang=fa')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

try:
    # ۱. لاگین
    print("۱. ورود به صفحه لاگین...")
    driver.get("https://www.aparat.com/login")
    
    # تلاش برای پیدا کردن فیلد نام کاربری با چندین شناسه محتمل
    username_input = None
    for selector in [By.NAME, By.ID]:
        for name in ["username", "email", "mobile", "luser"]:
            try:
                username_input = wait.until(EC.presence_of_element_located((selector, name)))
                print(f"پیدا شد: {selector} = {name}")
                break
            except:
                continue
        if username_input:
            break

    if not username_input:
        # اگر هنوز پیدا نشد، از placeholder کمک بگیریم
        username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder,'ایمیل') or contains(@placeholder,'موبایل') or contains(@placeholder,'کاربری')]")))
        print("با placeholder پیدا شد.")

    # حالا فیلد رمز عبور
    password_input = driver.find_element(By.NAME, "password")  # معمولاً name='password' ثابت است
    # اگر name='password' کار نکرد، روش‌های دیگر:
    if not password_input:
        password_input = driver.find_element(By.XPATH, "//input[@type='password']")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    
    # کلیک روی دکمه ورود
    login_button = driver.find_element(By.XPATH, "//button[@type='submit'] | //input[@type='submit'] | //button[contains(text(),'ورود')]")
    login_button.click()

    # منتظر بمانیم تا لاگین انجام شود
    wait.until(EC.url_contains("aparat.com"))
    time.sleep(3)
    print("لاگین انجام شد.")

    # ۲. آپلود (ادامه مانند قبل)
    driver.get("https://www.aparat.com/upload")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(VIDEO_PATH)
    print("فایل انتخاب شد. منتظر آپلود...")
    wait.until(EC.element_to_be_clickable((By.ID, "submit_button")))
    print("آپلود فایل کامل شد.")

    # پر کردن فرم
    title_field = driver.find_element(By.ID, "title")
    title_field.clear()
    title_field.send_keys(TITLE)

    # دسته‌بندی (فرض بر وجود select)
    try:
        category_select = driver.find_element(By.ID, "category_select")
        category_select.click()
        time.sleep(1)
        options_list = driver.find_elements(By.CSS_SELECTOR, "#category_select option")
        if len(options_list) > CATEGORY_INDEX:
            options_list[CATEGORY_INDEX].click()
        else:
            options_list[0].click()
    except:
        print("هشدار: فیلد دسته‌بندی پیدا نشد، ادامه می‌دهیم.")

    tags_field = driver.find_element(By.ID, "tags")
    tags_field.send_keys(TAGS)

    desc_field = driver.find_element(By.ID, "descr")
    desc_field.send_keys(DESCRIPTION)

    submit_btn = driver.find_element(By.ID, "submit_button")
    submit_btn.click()
    wait.until(EC.url_contains("video"))
    print("ویدیو با موفقیت آپلود شد.")

except Exception as e:
    driver.save_screenshot("error_screenshot.png")
    # چاپ source صفحه برای دیباگ (اختیاری)
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"خطا: {str(e)}")
    raise e

finally:
    driver.quit()
