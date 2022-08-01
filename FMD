import json, time, random, math, os, requests, re
from bs4 import BeautifulSoup

#ㅎㅇㅎㅇㅎㅇ

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
            elif (FMETag == "Caf"): splited_msg[i] = FinalMsgEditor.cafeterria(tags)
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
    def cafeterria(tags):
        if (len(tags)>2):
            month = tags[2]
            day = tags[3]
        else:
            month = None
            day = None
        localtime = time.localtime()
        if month == None: month = localtime.tm_mon
        else:
            if (day.isdigit() == True): month = int(month)
            else: month = localtime.tm_mon
        year = localtime.tm_year
        if day == None: day = localtime.tm_mon
        else:
            if (day.isdigit() == True): day = int(day)
            else: day = localtime.tm_mon
        msg = ''
        if (month < 10): month = f"0{month}"
        else: month = str(month)
        cafeterria_list = os.listdir('.\\cafeterria_data')

        if (f"{year}{month}" in cafeterria_list):
            cafeterria = eval(open(f'.\\cafeterria_data\\{year}{month}', 'r', encoding='utf8').read())
            for food in cafeterria[str(day)]:
                if ('(' in food): food = food[:food.find(')')]
                msg += f"\n{re.sub(r'[^a-zA-Z가-힣]','',food)}"
            return msg

        URL="https://stu.goe.go.kr/sts_sci_md00_001.do"
        params = {'schulCode':"J100002180",'schulCrseScCode':"3",'schulKndScCode':"03",'schYm':f"{year}{month}"}
        response = requests.get(URL, params=params).text
        data = response[response.find("<tbody>"):response.find("</tbody>")]
        regex = re.compile(r'[\n\r\t]')
        data=regex.sub('',data)
        rex = re.compile(r'<div>(.*?)</div>', re.S|re.M)
        data=rex.findall(data)
        file_json={}
        for dat in data:
            date=re.findall(r"[0-3][0-9]",dat[0:2])
            menu=dat[dat.find("[중식]<br />"):]
            if not date:
                date=dat[0:1]
                if date == "" or date == " ":
                    continue
            if type(date) == list:
                date=date[0]
            menu = menu.split("<br />")
            menu.remove(menu[0])
            if not menu:
                menu="None"
            file_json.update({date : menu})
        
        cafeterria = file_json
        for food in cafeterria[str(day)]:
            if ('(' in food): food = food[:food.find(')')]
            food = re.sub(r'[^a-zA-Z가-힣]','',food)
            msg += f"\n{re.sub(r'[^a-zA-Z가-힣]','',food)}"

        open(f".\\cafeterria_data\\{year}{month}",'w',encoding='utf8').write(str(cafeterria))

        return msg
