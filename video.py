import cv2
import os
from PIL import Image, ImageFilter
def video(who, bot, message):
    cam = cv2.VideoCapture(os.getcwd().replace("\\", "/") +  "/" + str(who) + "/video.mp4")
    try:
        if not os.path.exists(os.getcwd().replace("\\", "/") + '/' + str(who) + '/data'):
            os.makedirs(os.getcwd().replace("\\", "/") + '/' + str(who) + '/data')
    except OSError:
        print('Error: Creating directory of data')
    # frame
    currentframe = 0
    frames = 0
    while (True):
        ret, frame = cam.read()
        if ret:
            if currentframe % 1 == 0:
                name = "./" + str(who) + '/data/' + str(frames) + ".jpg"
                cv2.imwrite(name, frame)
                i = Image.open(os.getcwd().replace("\\", "/") + "/" + str(who) + "/data/" + str(frames) + ".jpg")
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
                        i.putpixel((a, b), (s, d, f))
                i = i.transpose(Image.ROTATE_180)
                i.save(os.getcwd().replace("\\", "/") + "/" + str(who) + "/data/" + str(frames) + ".jpg")
                frames += 1
            currentframe += 1
        else:
            bot.send_message(message.chat.id, "Your video has loaded successfully")
            return frames
            break
    cam.release()
    cv2.destroyAllWindows()