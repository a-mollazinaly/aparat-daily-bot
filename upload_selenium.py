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
CATEGORY_INDEX = 0   # اولین دسته
TAGS = "انگیزشی,جمله روز,موفقیت"
DESCRIPTION = "هر روز یک جمله زیبا برای روحیه شما.\nلطفاً با لایک و حمایت مالی از ما حمایت کنید."

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')
options.add_argument('--lang=fa')
# options.add_argument('--disable-gpu')   # اگر نیاز بود

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 30)

try:
    # ===== ۱. مرحله اول لاگین: وارد کردن نام کاربری =====
    print("۱. باز کردن صفحه لاگین...")
    driver.get("https://www.aparat.com/login")
    
    # صبر می‌کنیم تا فیلد نام کاربری (id="username") ظاهر شود
    username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
    print("فیلد نام کاربری پیدا شد.")
    
    # پاک کردن و وارد کردن نام کاربری
    username_input.clear()
    username_input.send_keys(USERNAME)
    
    # کلیک روی دکمه «ادامه»
    continue_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(),'ادامه')]")
    continue_button.click()
    print("دکمه ادامه کلیک شد.")

    # ===== ۲. مرحله دوم: وارد کردن رمز عبور =====
    # حالا صفحه عوض می‌شود و فیلد رمز عبور ظاهر می‌شود.
    # معمولاً فیلد رمز عبور دارای id="password" یا name="password" است.
    # ابتدا صبر می‌کنیم تا فیلد رمز ظاهر شود.
    try:
        # روش‌های مختلف برای پیدا کردن فیلد رمز
        password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
    except:
        try:
            password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        except:
            # اگر پیدا نشد، با placeholder تلاش می‌کنیم
            password_input = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@type='password' or contains(@placeholder,'رمز') or contains(@placeholder,'پسورد')]")
            ))
    print("فیلد رمز عبور پیدا شد.")
    
    password_input.clear()
    password_input.send_keys(PASSWORD)
    
    # دکمه ورود نهایی (معمولاً "ورود" یا "ادامه" دوباره)
    login_btn = driver.find_element(By.XPATH, "//button[@type='submit' and (contains(text(),'ورود') or contains(text(),'ادامه'))]")
    login_btn.click()
    print("دکمه ورود کلیک شد. منتظر تکمیل لاگین...")
    
    # صبر می‌کنیم تا لاگین کامل شود و به صفحه اصلی یا داشبورد هدایت شویم
    wait.until(EC.url_contains("aparat.com"))
    time.sleep(3)  # اندکی تأخیر برای بارگذاری کامل
    print("لاگین با موفقیت انجام شد.")

    # ===== ۳. رفتن به صفحه آپلود ویدیو =====
    print("۲. رفتن به صفحه آپلود...")
    driver.get("https://www.aparat.com/upload")
    
    # صبر برای ظهور فیلد آپلود فایل
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    print("صفحه آپلود بارگذاری شد.")
    
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(VIDEO_PATH)
    print("فایل ویدیو انتخاب شد. منتظر آپلود فایل...")
    
    # منتظر می‌مانیم تا نوار پیشرفت تمام شود و دکمه ارسال فعال شود
    # از ID دکمه submit استفاده می‌کنیم (باید بررسی کنید که درست باشد)
    # معمولاً دکمه ارسال دارای id='submit_button' یا id='submitBtn' است.
    # اینجا صبر می‌کنیم تا دکمه قابل کلیک شود:
    wait.until(EC.element_to_be_clickable((By.ID, "submit_button")))
    print("آپلود فایل تمام شد. حالا در حال پر کردن اطلاعات...")

    # ===== ۴. پر کردن فرم =====
    # عنوان
    title_field = driver.find_element(By.ID, "title")
    title_field.clear()
    title_field.send_keys(TITLE)

    # دسته‌بندی (select)
    try:
        category_select = driver.find_element(By.ID, "category_select")
        category_select.click()
        time.sleep(1)
        options_list = driver.find_elements(By.CSS_SELECTOR, "#category_select option")
        if len(options_list) > CATEGORY_INDEX:
            options_list[CATEGORY_INDEX].click()
        else:
            options_list[0].click()
        print("دسته‌بندی انتخاب شد.")
    except Exception as e:
        print(f"خطا در انتخاب دسته‌بندی: {e}")

    # تگ‌ها
    try:
        tags_field = driver.find_element(By.ID, "tags")
        tags_field.clear()
        tags_field.send_keys(TAGS)
    except:
        print("فیلد تگ پیدا نشد، ادامه می‌دهیم.")

    # توضیحات
    try:
        desc_field = driver.find_element(By.ID, "descr")
        desc_field.clear()
        desc_field.send_keys(DESCRIPTION)
    except:
        print("فیلد توضیحات پیدا نشد.")

    # ===== ۵. ارسال نهایی =====
    submit_btn = driver.find_element(By.ID, "submit_button")
    submit_btn.click()
    print("دکمه ارسال کلیک شد. منتظر نتیجه...")
    
    # صبر می‌کنیم تا به صفحه ویدیو برویم
    wait.until(EC.url_contains("video"))
    print("ویدیو با موفقیت آپلود شد!")

except Exception as e:
    # در صورت خطا، اسکرین‌شات و سورس صفحه را ذخیره می‌کنیم
    driver.save_screenshot("error_screenshot.png")
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print(f"خطا رخ داد: {str(e)}")
    raise e

finally:
    driver.quit()
