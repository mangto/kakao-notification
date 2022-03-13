from main import *

while True:
    room = str(open('.\\room.txt','r',encoding='utf8').read())
    Notification.auto_alert('3-12 수다방')
    time.sleep(5)