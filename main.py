
import vk_api
from variables import variable
import vk as VKONTAKTE
import time 
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict
import csv
import os
import re

words = [
    'веб','web','сайт','сайт под ключ','дизайн','Tilda','tilda','php','python','django','wordpress','wp','веб-дизайн'
]

class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()




def get_token():
    vk_session = vk_api.VkApi(variable['login'],variable['password'])
    vk_session.auth()
    vk = vk_session.get_api()
    return vk._vk.token['access_token']

def parse_wall(groupid):
    # first = vk_api.groups.getMembers(group_id=groupid, v=5.92)  # Первое выполнение метода
    first = vk_api.wall.get(owner_id='-40527789',v=5.92)
    data = first["items"]  # Присваиваем переменной первую тысячу id'шников
    count = first['count'] // 1000  # Присваиваем переменной количество тысяч участников
    # С каждым проходом цикла смещение offset увеличивается на тысячу
    # и еще тысяча id'шников добавляется к нашему списку.
    for i in range(1, count+1):
        time.sleep(0.3) 
        data = data + vk_api.wall.get(owner_id='-40527789',v=5.92,offset=i*1000)["items"]
    return data




def get_text_and_date(data,words):
    res = []
    count= 0
    date= datetime
    yesterday = date.today() - timedelta(days=1)
    for d in data:
        count+=1
        date_d = datetime.fromtimestamp(d['date'])
        if date_d < yesterday:
            continue
        for word in words:
            if re.match(r'{}'.format(word), d['text']):
                res.append({'id':(count),'text': d['text'],'date':datetime.fromtimestamp(d['date']).strftime('%Y-%m-%d %H:%M:%S')})
                
            else: 
                continue

    return sorted(res, key = lambda i: i['date'],reverse=True)

def write_to_csv(info_for_write):
#notice use OrderedDict for save order
    fields = ['id','text','date']
    file = 'out.csv'
    with open(file,'a+',encoding='utf-8-sig',newline='') as f:
        csv_dict = [row for row in csv.DictReader(f)]
        w = csv.DictWriter(f,fieldnames=fields)
        if os.stat(file).st_size == 0:
            w.writeheader()
        for r in info_for_write:    
            w.writerow(r)



def find_sites_in_data(data):
    cleaned_data = get_text_and_date(data,words)
    write_to_csv(cleaned_data)


token = get_token()
session = VKONTAKTE.Session(access_token=token)
vk_api = VKONTAKTE.API(session)
data = parse_wall("distantsiya")
work = find_sites_in_data(data)
