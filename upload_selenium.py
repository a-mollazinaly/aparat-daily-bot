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

# --- خواندن اطلاعات از متغیرهای محیطی ---
USERNAME = os.environ['APARAT_USERNAME']
PASSWORD = os.environ['APARAT_PASSWORD']
VIDEO_PATH = os.path.abspath("output.mp4")

# --- تنظیمات ویدیو ---
# تاریخ امروز را به عنوان بخشی از عنوان می‌گذاریم تا هر روز منحصربه‌فرد باشد
today = datetime.now().strftime("%Y/%m/%d")
TITLE = f"جمله انگیزشی روز - {today}"
CATEGORY_INDEX = 1    # 0-based, e.g., 0 for first category (maybe "سرگرمی"), check the dropdown
TAGS = "انگیزشی,جمله روز,موفقیت"
DESCRIPTION = "هر روز یک جمله زیبا برای روحیه شما.\nلطفاً با لایک و حمایت مالی از ما حمایت کنید."

# --- راه‌اندازی Chrome headless ---
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--lang=fa')  # برای اینکه سایت به فارسی نمایش داده شود

# نکته: از webdriver-manager برای دریافت خودکار chromedriver مناسب استفاده می‌کنیم
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

try:
    # ۱. لاگین در آپارات
    print("۱. ورود به صفحه لاگین...")
    driver.get("https://www.aparat.com/login")
    
    # صبر می‌کنیم تا فیلد نام کاربری ظاهر شود
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_input = driver.find_element(By.NAME, "password")
    
    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    
    # کلیک روی دکمه ورود یا زدن Enter
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    # منتظر می‌مانیم تا لاگین موفق انجام شود (مثلاً URL به صفحه اصلی تغییر کند)
    wait.until(EC.url_contains("aparat.com"))
    time.sleep(3)
    print("لاگین انجام شد.")

    # ۲. رفتن به صفحه آپلود
    print("۲. رفتن به صفحه آپلود...")
    driver.get("https://www.aparat.com/upload")
    
    # صبر تا صفحه کاملاً بارگذاری شود
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    
    # ۳. انتخاب فایل ویدیو
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(VIDEO_PATH)
    print("فایل انتخاب شد. منتظر آپلود فایل...")
    
    # آپارات معمولاً پس از انتخاب فایل، نوار پیشرفت نشان می‌دهد.
    # باید صبر کنیم تا آپلود فایل کامل شود.
    # می‌توانیم حضور دکمه‌ای که بعد از اتمام آپلود ظاهر می‌شود را بررسی کنیم.
    # در بسیاری از نسخه‌ها، پس از آپلود فایل، دکمه "ارسال" فعال می‌شود.
    # ما تا ۱۲۰ ثانیه صبر می‌کنیم.
    wait.until(EC.element_to_be_clickable((By.ID, "submit_button")))
    print("آپلود فایل کامل شد.")

    # ۴. پر کردن عنوان
    title_field = wait.until(EC.presence_of_element_located((By.ID, "title")))
    title_field.clear()
    title_field.send_keys(TITLE)
    
    # ۵. انتخاب دسته‌بندی (category)
    # در صفحه آپلود یک dropdown برای دسته‌بندی وجود دارد.
    # فرض می‌کنیم یک select با id="category_select" وجود دارد.
    # می‌توانیم با اندیس انتخاب کنیم.
    category_select = driver.find_element(By.ID, "category_select")
    category_select.click()
    # کمی صبر می‌کنیم تا گزینه‌ها باز شوند
    time.sleep(1)
    # گزینه‌ها معمولاً li هستند. اندیس CATEGORY_INDEX را انتخاب می‌کنیم (0 برای اولی)
    options_list = driver.find_elements(By.CSS_SELECTOR, "#category_select option")
    if len(options_list) > CATEGORY_INDEX:
        options_list[CATEGORY_INDEX].click()
    else:
        # اگر گزینه پیدا نشد، اولین گزینه
        if options_list:
            options_list[0].click()
    
    # ۶. تگ‌ها
    tags_field = driver.find_element(By.ID, "tags")
    tags_field.send_keys(TAGS)
    
    # ۷. توضیحات
    desc_field = driver.find_element(By.ID, "descr")
    desc_field.send_keys(DESCRIPTION)
    
    # ۸. ارسال نهایی
    submit_btn = driver.find_element(By.ID, "submit_button")
    submit_btn.click()
    print("ویدیو با موفقیت ارسال شد.")

    # منتظر می‌مانیم تا پیام موفقیت یا تغییر صفحه را ببینیم
    wait.until(EC.url_contains("video"))
    print("آپلود کامل شد.")

except Exception as e:
    # اگر خطایی رخ داد، عکس صفحه را بگیریم تا بعداً بررسی کنیم
    driver.save_screenshot("error_screenshot.png")
    print(f"خطا رخ داد: {str(e)}")
    raise e

finally:
    driver.quit()
