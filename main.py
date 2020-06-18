import vk_api
from variables import variable




vk_session = vk_api.VkApi(variable['login'],variable['password'])
vk_session.auth()

vk = vk_session.get_api()
print(vk)
print(vk.wall.post(message='Hello world!'))
