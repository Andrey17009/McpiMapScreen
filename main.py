from PIL import Image, ImageFilter
import telebot
import shutil
import time
from video import video as vid
import os
from mcpi.minecraft import Minecraft
mc = Minecraft.create("//you server's ip//", 4711)
bot=telebot.TeleBot("//you telegrambot id//")
@bot.message_handler(content_types=['photo', 'video'])
@bot.message_handler(commands=['start'])
def start_message(message):
    hhh = 0
    data = 0
    bot.send_message(message.chat.id, "Hello upload photo or video and i will show it in minecraft!")
    if not os.path.exists(str(message.chat.id)):
        os.makedirs(str(message.chat.id))
    if message.video:
        try:
            if not os.path.exists(os.getcwd().replace("\\", "/") + "/timetable"):
                os.makedirs(os.getcwd().replace("\\", "/") + "/timetable")
            else:
                bot.send_message(message.chat.id, "Sorry, there is currently a video or photo of another player.")
                return 0
            mc.postToChat(f"Don't upload other vidios on telegram, it was upload by {message.from_user.username} ({message.from_user.id}, {message.from_user.first_name}, {message.from_user.last_name})!")
            file_name = message.json['video']
            file_info = bot.get_file(message.video.file_id)
            with open("./" + str(message.chat.id) + "/video.mp4", "wb") as f:
                file_content = bot.download_file(file_info.file_path)
                f.write(file_content)
            hhh = 1
            data = int(vid(message.chat.id, bot, message)) - 1
        except:
            bot.send_message(message.chat.id, "Sorry, the file is probably too big!")
    elif message.photo:
        try:
            if not os.path.exists(os.getcwd().replace("\\", "/") + "/timetable"):
                os.makedirs(os.getcwd().replace("\\", "/") + "/timetable")
            else:
                bot.send_message(message.chat.id, "Sorry, there is currently a video or photo of another player.")
                return 0
            mc.postToChat(f"Don't upload other photos on telegram, it was upload by {message.from_user.username} ({message.from_user.id}, {message.from_user.first_name}, {message.from_user.last_name})!")
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/" + "image.jpg", 'wb') as new_file:
                new_file.write(downloaded_file)
            hhh = 2
            data = 1
        except:
            bot.send_message(message.chat.id, "Sorry, the file is probably too big!")
    if hhh != 0:
        t = -1
        while t != data:
            t += 1
            if hhh == 1:
                i = Image.open(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/data/" + str(t) + ".jpg")
            elif hhh == 2:
                i = Image.open(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/" + "image.jpg")
                i = i.filter(ImageFilter.SHARPEN)
                i = i.resize((128, 128))
                i = i.filter(ImageFilter.SHARPEN)
                picture_x, picture_y = i.size
                for a in range(picture_x):
                    for b in range(picture_y):
                        s, d, f = i.getpixel((a, b))
                        if s <= 128:
                            s = 0
                        else:
                            s = 255
                        if d <= 128:
                            d = 0
                        else:
                            d = 255
                        if f <= 128:
                            f = 0
                        else:
                            f = 255
                        i.putpixel((a,b), (s, d, f))
                i.save(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/" + "image.jpg")
                bot.send_photo(message.chat.id, open(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/" + "image.jpg", 'rb'))
                i = i.transpose(Image.ROTATE_180)
            picture_x, picture_y = i.size
            for a in range(picture_x):
                for b in range(picture_y):
                    s, d, f = i.getpixel((a, b))
                    if s == 0 and d == 0 and f == 0:
                        state = 15
                    elif s == 0 and d == 0 and f == 255:
                        state = 11
                    elif s == 0 and d == 255 and f == 0:
                        state = 5
                    elif s == 0 and d == 255 and f == 255:
                        state = 3
                    elif s == 255 and d == 0 and f == 0:
                        state = 14
                    elif s == 255 and d == 0 and f == 255:
                        state = 10
                    elif s == 255 and d == 255 and f == 0:
                        state = 4
                    elif s == 255 and d == 255 and f == 255:
                        state = 0
                    mc.setBlock(-65 - a, 96, 63 - b, 251, state)
                    #time.sleep(1)
            mc.postToChat(str(t) + "/" + str(data))
            if hhh == 2:
                os.remove(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/image.jpg")
                break
    time.sleep(5)
    if hhh != 0:
        os.rmdir(os.getcwd().replace("\\", "/") + "/timetable")
        mc.postToChat("Now you can!")
    if hhh == 1:
        shutil.rmtree(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/data/")
        os.remove(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/video.mp4")
bot.polling()