import random
import json
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy import *

# ۱. خواندن فایل جملات و انتخاب یکی تصادفی
with open("quotes.json", encoding="utf-8") as f:
    quotes = json.load(f)
quote = random.choice(quotes)

# ۲. ساختن یک عکس از جمله (پس‌زمینه مشکی و متن سفید)
img = Image.new('RGB', (1920, 1080), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("Vazir.ttf", 70)

# شکستن جمله به خط‌های کوتاه
import textwrap
lines = textwrap.wrap(quote, width=30)

# نوشتن خطوط وسط صفحه
y = 300
for line in lines:
    line_width = font.getlength(line)
    x = (1920 - line_width) / 2
    draw.text((x, y), line, font=font, fill=(255, 255, 255))
    y += 100

img.save("quote_image.png")

# ۳. ساختن فایل صوتی از جمله (با صدای کامپیوتری فارسی)
tts = gTTS(text=quote, lang='fa', slow=False)
tts.save("speech.mp3")

# ۴. ساختن ویدیو: ترکیب ویدیوی پس‌زمینه، عکس و صدا
video_bg = VideoFileClip("background.mp4").without_audio()
audio_speech = AudioFileClip("speech.mp3")
music = AudioFileClip("music.mp3").volumex(0.3)  # کم کردن صدای موسیقی

# تنظیم مدت زمان ویدیو
duration = audio_speech.duration + 0.5
video_bg = video_bg.subclip(0, duration)
music = music.subclip(0, duration)

# مخلوط کردن دو صدا
final_audio = CompositeAudioClip([audio_speech, music])

# لایه تصویر جمله
img_clip = ImageClip("quote_image.png").set_duration(duration).set_position('center')

# ترکیب نهایی
final_video = CompositeVideoClip([video_bg, img_clip]).set_audio(final_audio)
final_video.write_videofile("output.mp4", fps=24, codec='libx264', audio_codec='aac')
