import requests
import json
import codecs
from urllib.parse import urlencode



file_path = "./ddd.json"
client_id = "35855"
client_secret = "428d72e8d59140d89a4d9e4ee234e10f; charset=utf-8"
HEADERS = {"X-API-Key":client_secret}
origin = 'https://www.bungie.net'
name = '데스티니스탯정의'
ss = "/Platform/Destiny2/Actions/Items/EquipItem/"
print(origin+ss)

r = requests.get(origin + ss, headers=HEADERS);

print(r)
#아 쉬바 ㅋㅋㅋ메인 버려진거냐구 ㅋㅋㅋㅋ