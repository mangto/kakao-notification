from main import *

while True:
    room = str(open('.\\room.txt','r',encoding='utf8').read())
    Notification.auto_alert(room)
    try:
        google_spreadsheet.save_data()
    except: pass
    time.sleep(5)