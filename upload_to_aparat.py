import os
import requests

def get_access_token():
    data = {
        "grant_type": "password",
        "client_id": os.environ['CLIENT_ID'],
        "client_secret": os.environ['CLIENT_SECRET'],
        "username": os.environ['APARAT_USERNAME'],
        "password": os.environ['APARAT_PASSWORD']
    }
    resp = requests.post("https://api.aparat.com/oauth/token", data=data)
    return resp.json().get('access_token')

def upload_video(file_path, title, description, tags, category):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # قدم اول: درخواست آماده‌سازی
    prepare = requests.post("https://api.aparat.com/rest/v1/video/prepare", headers=headers, json={
        "title": title,
        "category": category,
        "description": description,
        "tags": tags
    })
    info = prepare.json()
    upload_url = info['url']
    file_id = info['file_id']
    
    # آپلود فایل
    with open(file_path, 'rb') as f:
        requests.put(upload_url, data=f)
    
    # نهایی‌سازی
    commit = requests.post("https://api.aparat.com/rest/v1/video/commit", headers=headers, json={
        "file_id": file_id
    })
    return commit.json()

if __name__ == "__main__":
    # این مقادیر را می‌توانید تغییر دهید
    title = "جمله انگیزشی روز"
    description = "هر روز یک جمله زیبا برای روحیه شما.\nحمایت مالی: (لینک شما)"
    tags = ["انگیزشی", "جمله روز", "موفقیت"]
    category = 1  # دسته‌بندی (مثلاً ۱ برای سرگرمی)
    
    result = upload_video("output.mp4", title, description, tags, category)
    print(result)