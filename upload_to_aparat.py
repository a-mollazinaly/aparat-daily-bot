import os, hashlib, requests

USERNAME = os.environ['APARAT_USERNAME']
PASSWORD = os.environ['APARAT_PASSWORD']

def login():
    pass_md5 = hashlib.md5(PASSWORD.encode()).hexdigest()
    pass_sha1 = hashlib.sha1(pass_md5.encode()).hexdigest()
    url = "https://www.aparat.com/etc/api/login"
    params = {"luser": USERNAME, "lpass": pass_sha1}
    resp = requests.get(url, params=params)
    data = resp.json()
    ltoken = data.get('login', {}).get('ltoken')
    if not ltoken:
        raise Exception(f"Login failed: {data}")
    return ltoken

def get_upload_form(ltoken):
    url = "https://www.aparat.com/etc/api/uploadform"
    params = {"luser": USERNAME, "ltoken": ltoken}
    resp = requests.get(url, params=params)
    data = resp.json()
    form_action = data['uploadform']['formAction']
    frm_id = data['uploadform']['frm-id']
    return form_action, frm_id

def upload_video(file_path, title, category, tags, description, comment="yes"):
    ltoken = login()
    form_action, frm_id = get_upload_form(ltoken)
    with open(file_path, 'rb') as f:
        files = {'video': f}
        data = {
            'frm-id': frm_id,
            'data[title]': title,
            'data[category]': category,
            'data[tags]': tags,
            'data[descr]': description,
            'data[comment]': comment,
        }
        resp = requests.post(form_action, files=files, data=data)
        result = resp.json()
        print(result)
        return result

if __name__ == "__main__":
    title = "جمله انگیزشی روز"
    description = "هر روز یک جمله زیبا برای روحیه شما.\nحمایت مالی: (لینک شما)"
    tags = "انگیزشی-جمله روز-موفقیت"
    category = 1
    upload_video("output.mp4", title, category, tags, description)
