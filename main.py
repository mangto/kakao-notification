import win32api, win32con, win32gui, time, ctypes
import pygetwindow, json, time, random, math, os, requests, re
from bs4 import BeautifulSoup
from ctypes import wintypes

PBYTE256 = ctypes.c_ubyte * 256
_user32 = ctypes.WinDLL("user32")
GetKeyboardState = _user32.GetKeyboardState
SetKeyboardState = _user32.SetKeyboardState
PostMessage = win32api.PostMessage
SendMessage = win32gui.SendMessage
FindWindow = win32gui.FindWindow
IsWindow = win32gui.IsWindow
GetCurrentThreadId = win32api.GetCurrentThreadId
GetWindowThreadProcessId = _user32.GetWindowThreadProcessId
AttachThreadInput = _user32.AttachThreadInput
MapVirtualKeyA = _user32.MapVirtualKeyA
MapVirtualKeyW = _user32.MapVirtualKeyW
MakeLong = win32api.MAKELONG
w = win32con
wintypes.ULONG_PTR = wintypes.WPARAM
hllDll = ctypes.WinDLL ("User32.dll", use_last_error=True)

def open_chatroom(chatroom_name, RE=False):
    if (chatroom_name not in pygetwindow.getAllTitles() or RE==True):
        hwndkakao = win32gui.FindWindow(None, "카카오톡")
        hwndkakao_edit1 = win32gui.FindWindowEx( hwndkakao, None, "EVA_ChildWindow", None)
        hwndkakao_edit2_1 = win32gui.FindWindowEx( hwndkakao_edit1, None, "EVA_Window", None)
        hwndkakao_edit2_2 = win32gui.FindWindowEx( hwndkakao_edit1, hwndkakao_edit2_1, "EVA_Window", None)    # ㄴ시작핸들을 첫번째 자식 핸들(친구목록) 을 줌(hwndkakao_edit2_1)
        hwndkakao_edit3 = win32gui.FindWindowEx( hwndkakao_edit2_2, None, "Edit", None)
        win32api.SendMessage(hwndkakao_edit3, win32con.WM_SETTEXT, 0, chatroom_name)
        time.sleep(0.1)
        SendReturn(hwndkakao_edit3)
        time.sleep(0.1)
    if(RE==False):open_chatroom('',True)
def send_text(chatroom_name, text):
    hwndMain = win32gui.FindWindow( None, chatroom_name)
    hwndEdit = win32gui.FindWindowEx( hwndMain, None, "RICHEDIT50W", None)

    win32api.SendMessage(hwndEdit, win32con.WM_SETTEXT, 0, text)
    SendReturn(hwndEdit)
def PostKeyEx(hwnd, key, shift, specialkey):
    if IsWindow(hwnd):

        ThreadId = GetWindowThreadProcessId(hwnd, None)

        lparam = MakeLong(0, MapVirtualKeyA(key, 0))
        msg_down = w.WM_KEYDOWN
        msg_up = w.WM_KEYUP

        if specialkey:
            lparam = lparam | 0x1000000

        if len(shift) > 0:
            pKeyBuffers = PBYTE256()
            pKeyBuffers_old = PBYTE256()

            SendMessage(hwnd, w.WM_ACTIVATE, w.WA_ACTIVE, 0)
            AttachThreadInput(GetCurrentThreadId(), ThreadId, True)
            GetKeyboardState(ctypes.byref(pKeyBuffers_old))

            for modkey in shift:
                if modkey == w.VK_MENU:
                    lparam = lparam | 0x20000000
                    msg_down = w.WM_SYSKEYDOWN
                    msg_up = w.WM_SYSKEYUP
                pKeyBuffers[modkey] |= 128

            SetKeyboardState(ctypes.byref(pKeyBuffers))
            time.sleep(0.01)
            PostMessage(hwnd, msg_down, key, lparam)
            time.sleep(0.01)
            PostMessage(hwnd, msg_up, key, lparam | 0xC0000000)
            time.sleep(0.01)
            SetKeyboardState(ctypes.byref(pKeyBuffers_old))
            time.sleep(0.01)
            AttachThreadInput(GetCurrentThreadId(), ThreadId, False)

        else:
            SendMessage(hwnd, msg_down, key, lparam)
            SendMessage(hwnd, msg_up, key, lparam | 0xC0000000)
def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.008)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
def encrypt(string: str,seed:int=5,length=20):
    if(type(string) != str):
        print(str(string) + " <- string have to be <class 'str'> not ",str(type(string)))
    string = str(string)

    ols = "" #Ord List String
    si = 0
    result = ""
    result_1 = ""
    for c in string: ols += str(ord(c))
    for i in range(len(ols)-1):
        if (int(ols[i]) <= 3): si = int(ols[i])
        else: si = 3
        if (si == 0): si = 1
        n = int(math.log2((len(ols)-i)*i**int(ols[i:i+2])+41))
        result_1 += str(n**2-2*n+1)
    ols = ""
    olsl = []
    for c in result_1: ols += str(ord(c))
    for c in result_1: olsl.append(int(c))
    olsl = [olsl[i * seed:(i + 1) * seed] for i in range((len(olsl) + seed- 1) //seed )]
    if ([] in olsl):
        olsl.remove([])
    random.Random(int(ols)).shuffle(olsl)
    result_2 = result_1
    result_1 = ""
    for l in olsl:
        for ll in l: result_1 += str(ll+41)
    result_1 = str(int(result_1)*int(result_2))
    for i in range(int(len(result_1))):
        if not(int(result_1[i:i+2]) < 40): result += chr(int(result_1[i:i+2]))
        else: result += chr(int(result_1[i:i+2])+45)
    result_1 = str(result).splitlines()
    result = ""
    for r in result_1: result += r
    if (int(len(result)/5+length) < len(result)): end = int(len(result)/5)+length
    else: end = len(result)
    return re.sub(r"[^a-zA-Z0-9]", '', str(result)[int(len(result)/5):end])

class FinalMsgEditor:
    def split_msg(msg:str):
        return [c for c in msg.split('///') if (c != '')]
    def fullEdit(msg:str):
        splited_msg = FinalMsgEditor.split_msg(msg)
        for i in range(len(splited_msg)): #each message
            emsg = splited_msg[i]
            if (emsg.startswith('FME:') == False): continue # FME Type Only

            tags = emsg.split(':')
            FMETag = tags[1]
            
            if (FMETag == 'Ran'): splited_msg[i] = FinalMsgEditor.random(tags)
            elif (FMETag == 'Crw'): splited_msg[i] = FinalMsgEditor.crawl(tags)
            elif (FMETag == "Sup"): splited_msg[i] = FinalMsgEditor.supplies(tags)
        msg = ''
        for c in splited_msg: msg += c

        return msg
    def random(tags):
        # ///FME:Ran:"random tag"///
        msg = ''
        random_tag = tags[2]
        random_dict = json.load(open('.\\FME_random.json','r',encoding='utf8'))

        if (random_tag not in random_dict): return msg

        random_list = random_dict[random_tag]
        return random.sample(random_list, 1)[0]
    def crawl(tags):
        # ///FME:Crw:"crawl tag"///
        msg = ''
        crawl_tag = tags[2]
        crawl_dict = json.load(open('.\\FME_crawl.json','r',encoding='utf8'))
        
        if (crawl_tag not in crawl_dict): return msg

        list_crawled_data = os.listdir('.\\crawl_data')
        selector = crawl_dict[crawl_tag]['selector']
        url = crawl_dict[crawl_tag]['url']
        crawl_id = encrypt(url,10)
        region = crawl_dict[crawl_tag]['text_region'].split(':')
        localtime = time.localtime()
        year = localtime.tm_year
        month = localtime.tm_mon
        day = localtime.tm_mday
        hour = localtime.tm_hour

        if (crawl_id+f'.{year}{month}{day}.{hour}' in list_crawled_data):
            req = str(open(f'.\\crawl_data\\{crawl_id}.{year}{month}{day}.{hour}','r',encoding='utf8').read())
            soup = BeautifulSoup(req,'html.parser')
        else:
            req = requests.get(url).text
            soup = BeautifulSoup(req,'html.parser')
            open(f'.\\crawl_data\\{crawl_id}.{year}{month}{day}.{hour}','w',encoding='utf8').write(str(req))

        if (region != ['']):
            msg = soup.select_one(str(selector)).text[int(region[0]):int(region[1])]
        else: msg = soup.select_one(str(selector)).text
        
        return msg
    def supplies(tags):
        msg = ''
        localtime = time.localtime()
        wday = localtime.tm_wday
        month = localtime.tm_mon
        day = localtime.tm_mday
        DayKey = f"{month}/{day}"

        if (wday >= 5): return ''

        ClassList = json.load(open('.\\FME_supplies_classes.json','r',encoding='utf8'))
        Supplies = json.load(open('.\\FME_supplies.json','r',encoding='utf8'))
        n = 1
        for class_ in ClassList[str(wday)]:
            msg += f"\n[{n}] {class_}: {Supplies['default'][class_]}"
            if (class_ in Supplies['wday'][str(wday)]): msg += f", {Supplies['wday'][str(wday)][class_]}" #wday
            if (DayKey in Supplies['specific']): #specific day
                if (class_ in Supplies['specific'][DayKey]):
                    msg += f", {Supplies['specific'][DayKey][class_]}"
            
            n+=1

        #else supplies like survey
        if (DayKey in Supplies['else']):
            for sup in Supplies['else'][DayKey]:
                msg += f"\n[*] {sup}"

        return msg
class Notification:
    chatroom = "임영재" #change to 3-12 after testing #chatroom name

    def get_data():
        ###  [DATA TYPE]
        ###   - default: regular alert
        ###   - extra: alert on specific day
        return json.load(open('.\\notification_data.json','r',encoding='utf8'))
    def get_log():
        return json.load(open('.\\notification_log.json','r',encoding='utf8'))
    def add_log(NOTIFICATION_TAG):
        localtime = time.localtime()
        log = Notification.get_log()
        timetag = f'{localtime.tm_year}-{localtime.tm_mon}-{localtime.tm_mday}'

        if(timetag not in log): log[timetag] = [] #make if there's no anytags today

        log[timetag].append(NOTIFICATION_TAG)
        json.dump(log, open('.\\notification_log.json','w',encoding='utf8'),indent="\t")
    def auto_alert():
        data_set = Notification.get_data()
        localtime = time.localtime()
        wday = localtime.tm_wday
        nhour = localtime.tm_hour
        nminute = localtime.tm_min
        month = localtime.tm_mon
        day = localtime.tm_mday
        timetag = f'{localtime.tm_year}-{localtime.tm_mon}-{localtime.tm_mday}'
        logs = Notification.get_log()

        for notific in data_set['default']:
            notific = data_set['default'][notific]
            alert_time = notific['time'].split(":") #seperate into hour and minute
            if (timetag not in logs or notific['tag'] not in logs[timetag]): #is already alerted this notification?
                if (wday in notific['cycle'] and int(alert_time[0]) == nhour and int(alert_time[1]) == nminute):
                    open_chatroom(Notification.chatroom)
                    send_text(Notification.chatroom, FinalMsgEditor.fullEdit(notific['msg']))
                    Notification.add_log(notific['tag'])
        for notific in data_set['extra']:
            notific = data_set['extra'][notific]
            alert_time = notific['time'].split(":") #seperate into hour and minute
            alert_day = notific['day'].split('/')
            if (timetag not in logs or notific['tag'] not in logs[timetag]): #is already alerted this notification?
                if (int(alert_day[0]) == month and int(alert_day[1]) == day and int(alert_time[0]) == nhour and int(alert_time[1]) == nminute):
                    open_chatroom(Notification.chatroom)
                    send_text(Notification.chatroom, FinalMsgEditor.fullEdit(notific['msg']))
                    Notification.add_log(notific['tag'])


while True:
    Notification.auto_alert()
    time.sleep(5)