import smtplib
import random
import subprocess
import os
import shutil
from pytube import YouTube
import playsound


def email_bot(send_addr, password, recv_addr, body, server, port, sub='No Subject'):
    with smtplib.SMTP(server, port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(send_addr, password)

        sub_msg = 'Subject: {}'.format(sub)
        body_msg = '\n\n {}'.format(body)

        final_msg = sub_msg + body_msg

        smtp.sendmail(send_addr, recv_addr, final_msg)
        return True


def email_address_slicer(full_addr):
    splitList = full_addr.split('@')
    username = splitList[0]
    domain = splitList[1]
    return username, domain


def yt_downloader(video_url, output_path=str(os.getcwd()), filename='video'):
    yt = YouTube(video_url)
    if yt.streams.first().download():
        return True
    else:
        return False


def roll_dice(dice_1=True):
    if dice_1 == True:
        rolls = [1, 2, 3, 4, 5, 6]
        return random.choice(rolls)
    else:
        rolls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        return random.choice(rolls)


def timer(seconds, audio_file):
    time = seconds
    for i in range(0, seconds):
        if time <= 0:
            playsound.playsound(audio_file)
        time = time - 1

def start_app(drive, exe_path):
    command = drive + ': && ' + exe_path
    if subprocess.run(command, shell=True):
        return True