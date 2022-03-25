from urllib import request
origin = 'https://www.bungie.net'
url = '/common/destiny2_content/json/ko/DestinySocketCategoryDefinition-aec69088-d246-4c61-b4fc-cd92fd2bd63b.json'
savename = "./jsoon/소켓카테고리정의.json"
request.urlretrieve(origin+url,savename,)
print("저장되었습니다.")
#여기서 json 파일을 다운받아서
#정리한 뒤에 저장해야 됨....
#인벤토리아이템에 퍽에 대한 정보도 들어 있다
