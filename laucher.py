from main import *

while True:
    room = str(open('.\\room.txt','r',encoding='utf8').read())
    Notification.auto_alert(room)
    time.sleep(5)
