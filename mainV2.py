from PIL import Image, ImageFilter
import telebot
import shutil
import time
import cv2
import os
from mcpi.minecraft import Minecraft

def video(who, bot, message):
    cam = cv2.VideoCapture(os.getcwd().replace("\\", "/") + "/" + str(who) + "/video.mp4")
    try:
        if not os.path.exists(os.getcwd().replace("\\", "/") + '/' + str(who) + '/data'):
            os.makedirs(os.getcwd().replace("\\", "/") + '/' + str(who) + '/data')
    except OSError:
        print('Error: Creating directory of data')
    currentframe = 0
    frames = 0
    while (True):
        ret, frame = cam.read()
        if ret:
            if currentframe % 10 == 0:
                name = "./" + str(who) + '/data/' + str(frames) + ".jpg"
                cv2.imwrite(name, frame)
                i = Image.open(os.getcwd().replace("\\", "/") + "/" + str(who) + "/data/" + str(frames) + ".jpg")
                i = i.filter(ImageFilter.SHARPEN)
                i = i.resize((128, 128))
                i.save(os.getcwd().replace("\\", "/") + "/" + str(who) + "/data/" + str(frames) + ".jpg")
                frames += 1
            currentframe += 1
        else:
            bot.send_message(message.chat.id, "Your video has loaded successfully")
            return frames - 1
            break
    cam.release()
    cv2.destroyAllWindows()


mc = Minecraft.create("26.110.228.166", 4711)
bot = telebot.TeleBot("6971521187:AAGqLfWHD6D2qlLkxtsxoek0fjf4Jyi8Vmw")
@bot.message_handler(content_types=['photo', 'video'])
@bot.message_handler(commands=['start'])
def start_message(message):
    hhh = 0
    data = 0
    if message.text == "/start":
        bot.send_message(message.chat.id, "Hello upload photo or video and i will show it in minecraft, for security it will show your name and some another info!")
    if not os.path.exists(str(message.chat.id)):
        os.makedirs(str(message.chat.id))
    if message.video:
        try:
            if not os.path.exists(os.getcwd().replace("\\", "/") + "/timetable"):
                os.makedirs(os.getcwd().replace("\\", "/") + "/timetable")
            else:
                bot.send_message(message.chat.id, "Sorry, there is currently a video or photo of another player.")
                return 0
            bot.send_message(message.chat.id, "Pls wait, video is uploading...")
            mc.postToChat(f"Don't upload other vidios on telegram, it was uploaded by {message.from_user.username} ({message.from_user.id}, {message.from_user.first_name}, {message.from_user.last_name})!")
            file_name = message.json['video']
            file_info = bot.get_file(message.video.file_id)
            with open("./" + str(message.chat.id) + "/video.mp4", "wb") as f:
                file_content = bot.download_file(file_info.file_path)
                f.write(file_content)
            hhh = 1
            data = video(message.chat.id, bot, message)
        except:
            bot.send_message(message.chat.id, "Sorry, the file is probably too big!")
    elif message.photo:
        try:
            if not os.path.exists(os.getcwd().replace("\\", "/") + "/timetable"):
                os.makedirs(os.getcwd().replace("\\", "/") + "/timetable")
            else:
                bot.send_message(message.chat.id, "Sorry, there is currently a video or photo of another player.")
                return 0
            mc.postToChat(f"Don't upload other photos on telegram, it was uploaded by {message.from_user.username} ({message.from_user.id}, {message.from_user.first_name}, {message.from_user.last_name})!")
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
                i.save(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/" + "image.jpg")
                bot.send_photo(message.chat.id, open(os.getcwd().replace("\\", "/") + "/" + str(message.chat.id) + "/" + "image.jpg", 'rb'))
            picture_x, picture_y = i.size
            state = 0
            i = i.transpose(Image.ROTATE_180)
            for x in range(picture_x):
                for z in range(picture_y):
                    r, g, b = i.getpixel((x, z))
                    if r <= 128:
                        r = 0
                    else:
                        r = 255
                    if g <= 128:
                        g = 0
                    else:
                        g = 255
                    if b <= 128:
                        b = 0
                    else:
                        b = 255
                    if r == 0 and g == 0 and b == 0:
                        state = 15
                    elif r == 0 and g == 0 and b == 255:
                        state = 11
                    elif r == 0 and g == 255 and b == 0:
                        state = 5
                    elif r == 0 and g == 255 and b == 255:
                        state = 3
                    elif r == 255 and g == 0 and b == 0:
                        state = 14
                    elif r == 255 and g == 0 and b == 255:
                        state = 10
                    elif r == 255 and g == 255 and b == 0:
                        state = 4
                    elif r == 255 and g == 255 and b == 255:
                        state = 0
                    mc.setBlock(-65 - x, 96, 63 - z, 251, state)
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
