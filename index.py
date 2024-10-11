import telebot
import cv2 as cv
import os
from rembg import remove
from fpdf import FPDF
from pytube import YouTube
from MukeshAPI import api
import random

API_TOKEN = "7502187198:AAFqt-hOzuVH4mIxdc5_DDeLRPf6wrHA7X0"
bot = telebot.TeleBot(API_TOKEN)
pdf = FPDF()
# Start Sections

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "hello im robot for seintiant ai how can help you ")

# End Section
# Start Help Sections
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "\n start - \nhelp - \ncontact_us -\nreduce_noise - \nremove_bg -\ntext2pdf - pdf\nimage2text - \ndownload_youtube - \ndirect_auto_insta -\ndownload_insta_post - \nimage_generator -\nvirtual_glass_and_clouth \nsms_bomber - \nface_swap ")

# Start Contact-us Section
@bot.message_handler(commands=['contact_us'])
def contact_us_handler(message):
    bot.reply_to(message, "Support ID: @sadeghi_code")

# Start Reduce Noise
@bot.message_handler(commands=['reduce_noise'])
def redce_noise(message):
    bot.reply_to(message, "please enter the photo")
    bot.register_next_step_handler(message=message, callback=reduce)

def enhance(image_path):
    image = cv.imread(image_path)

    reduce_noise = cv.bilateralFilter(image, 9, 75, 75)

    output_path = "dnoise.jpg"
    cv.imwrite(output_path, reduce_noise)

    return output_path
def reduce(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("after_denoise.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, "picture is reducting...")
    processed_image_path = enhance("after_denoise.jpg")
    
    file_size = os.path.getsize(processed_image_path)
    file_size_kb = file_size / 1024

    bot.send_message(message.chat.id, "picture with successfully reducing")
    with open(processed_image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, f"size: {file_size_kb} KB")
    bot.send_message(message.chat.id, "picture without noise uploaded")

# Start Removebg section
@bot.message_handler(commands=['remove_bg'])
def removes(message):
    bot.reply_to(message, "please enter photo")
    bot.register_next_step_handler(message=message, callback=removebg)

def removebg(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("remove_background.png", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, "picture is removing background")
    # Remove background
    with open("remove_background.png", "rb") as input_file:
        output = remove(input_file.read())
    
    processed_image_path = "removedbg.png"
    with open(processed_image_path, "wb") as output_file:
        output_file.write(output)
    
    file_size = os.path.getsize(processed_image_path)
    file_size_kb = file_size / 1024

    bot.send_message(message.chat.id, "picture is uploading to telegram")
    with open(processed_image_path, 'rb') as photo:
        bot.send_document(message.chat.id, photo, f"size: {file_size_kb} KB")
    bot.send_message(message.chat.id, "image without uploaded succesfully")

# Start text2pdf section
@bot.message_handler(commands=['text2pdf'])
def pdfs1(message):
    bot.reply_to(message, "please enter a text")
    bot.register_next_step_handler(message=message, callback=text2pdf)

def text2pdf(message):
    text = message.text
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    bot.send_message(message.chat.id, "text is converted.. ")
    
    pdf.multi_cell(0, 10, text)
    file_names = "out.pdf"
    pdf.output(file_names)

    bot.send_message(message.chat.id,"text changed to pdf successfully")
    with open(file_names, 'rb') as pdfs:
        bot.send_document(message.chat.id, pdfs)
    bot.send_message(message.chat.id, "pdf file uploaded successfully")


# Start text2pdf section
@bot.message_handler(commands=['download_youtube'])
def yt_download(message):
    bot.reply_to(message, "for download the video send a link video")
    bot.register_next_step_handler(message=message, callback=youtube)

def get_video(video_path, chatID):
    try:
        yt = YouTube(video_path)
        bot.send_message(chatID, f"Title: {yt.title}")

        stream = yt.streams.get_highest_resolution()
        
        bot.send_message(chatID, "youtube video placed in queue download")

    
        stream.download(output_path=".", filename="yt_video.mp4")

        with open("yt_video.mp4", 'wb') as vid:
            vid.write("yt_writed.mp4")

        bot.send_message(chatID, "video downloaded successfully")
        return "yt_video.mp4"
    except Exception as e:
        bot.send_message(chatID, f"'failed error in download' {str(e)}")
        return None
    
def youtube(message):
    video_path = message.text

    vid_yt = get_video(video_path, message.chat.id)

    with open(vid_yt, 'rb') as vid:
        bot.send_document(message.chat.id, vid)
    bot.send_message(message.chat.id, "video send successfully")

    os.remove("yt_video.mp4")



# Start image-generator section
@bot.message_handler(commands=['image_generator'])
def img_generator(message):
    bot.reply_to(message, "please enter a picture prompt: ")
    bot.register_next_step_handler(message=message, callback=generatorai)


def generatorai(message):
    text = message.text
    response = api.ai_image(text)

    bot.send_message(message.chat.id, "picture is creating...")
    
    bot.send_message(message.chat.id, "picture created successfully")
    with open(f"image-{random.randint(1000,10000)}", 'wb') as f:
        f.write(response)
        bot.send_document(message.chat.id, f)
    bot.send_message(message.chat.id, "picture uploaded to telegram")


bot.polling()