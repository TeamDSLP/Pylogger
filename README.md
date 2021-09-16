# Pylogger
A keylogger written in Python for CS6348 Data & Applications Security

## Features
- [ ] Stores keystrokes a user makes to a file
  - [x] Keystrokes
  - [ ] Clipboard text
  - [ ] Length of keypress
- [ ] Logs the application keystrokes are being made in
- [x] Accounts for different keyboard layouts (i.e., Dvorak)/onscreen keyboards
  - Accounts for Windows default on-screen keyboard. Unable to test other physical layouts.
- [x] Periodically takes a screenshot of whole screen
- [x] Periodically sends the files or files’ contents over email

Logger.pyw: Uses library pynput to store the keystrokes of the victim's keyboard. After 50 characters it sends an email with the keystroke information and also sends a screenshot of the main monitor of the victim

Launch.bat: File that launches logger and IE if the properties of IE have been altered
Launch.bat.txt: Text file of launch.bat so that it can be read by TA

Windows will try to delete the launch.bat scripts because they are malicious, you need to approve the scripts in your antivirus program.
