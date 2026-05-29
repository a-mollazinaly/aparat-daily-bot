import random, json, asyncio, textwrap
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import edge_tts

QUOTES_FILE = "quotes.json"
BACKGROUND_VIDEO = "background.mp4"
MUSIC_FILE = "music.mp3"
FONT_PATH = "Vazir.ttf"
OUTPUT_VIDEO = "output.mp4"

# انتخاب جمله
with open(QUOTES_FILE, encoding="utf-8") as f:
    quotes = json.load(f)
quote = random.choice(quotes)

# ساخت تصویر
img = Image.new('RGB', (1920, 1080), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype(FONT_PATH, 70)

lines = textwrap.wrap(quote, width=30)
y = 300
for line in lines:
    line_width = font.getsize(line)[0]   # اصلاح‌شده
    x = (1920 - line_width) / 2
    draw.text((x, y), line, font=font, fill=(255, 255, 255))
    y += 100

img.save("quote_image.png")

# تولید صوت با edge-tts
async def generate_audio():
    tts = edge_tts.Communicate(quote, voice="fa-IR-FaridNeural")
    await tts.save("speech.mp3")

asyncio.run(generate_audio())

# ساخت ویدیو
video_bg = VideoFileClip(BACKGROUND_VIDEO).without_audio()
speech_audio = AudioFileClip("speech.mp3")
music = AudioFileClip(MUSIC_FILE).volumex(0.3)   # این تابع با moviepy 1.0.3 کار می‌کند

duration = speech_audio.duration + 0.5
video_bg = video_bg.subclip(0, duration)
music = music.subclip(0, duration)

final_audio = CompositeAudioClip([speech_audio, music])
img_clip = ImageClip("quote_image.png").set_duration(duration).set_position('center')

final_video = CompositeVideoClip([video_bg, img_clip]).set_audio(final_audio)
final_video.write_videofile(OUTPUT_VIDEO, fps=24, codec='libx264', audio_codec='aac')
