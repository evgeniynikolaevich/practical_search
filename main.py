
import vk_api
from variables import variable
import vk as VKONTAKTE
import time 
from datetime import datetime
from collections import OrderedDict



word_for_search = [
    'сайт','сайт под ключ','дизайн'
]


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
        time.sleep(0.2) 
        data = data + vk_api.wall.get(owner_id='-40527789',v=5.92,offset=i*1000)["items"]
    return data




def get_text_and_date(data):
    res = []
    count= 0
    for d in data:
        res.append({'id':count+1,'text': d['text'],'date':datetime.fromtimestamp(d['date']).strftime("%d, %Y %I:%M:%S")})
    return res



def find_sites_in_data(data):
    cleaned_data = get_text_and_date(data)
    print(cleaned_data)


token = get_token()
session = VKONTAKTE.Session(access_token=token)
vk_api = VKONTAKTE.API(session)
data = parse_wall("distantsiya")
work = find_sites_in_data(data)
