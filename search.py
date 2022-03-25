import requests
import json
from urllib import request
from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
import pickle
import os
import itertools

global imagephoto,imagephoto2
global txt_detalie, client_secret, HEADERS, origin, data_location, image_location
global stathash

stathash = []

data_location = './data/'
image_location = './image/'

client_secret = "428d72e8d59140d89a4d9e4ee234e10f"
HEADERS = {"X-API-Key": client_secret}
origin = 'https://www.bungie.net'

#폴더랑 기본파일 확인용, ddd.json 확인....

root = Tk()
root.title("데스티니 2")
root.geometry("500x500+100+100")
#프레임/윈도우/창 크기 조절 허용 여부
root.resizable(False, True)
root.iconbitmap(data_location+"destiny-2.ico")

def btndef():
    global names
    print(entr1.get())
    names = findhash()

    #txt_detalie.insert(END,find_hash)
    #name.clear()
    return

def findhash():
    gettxt = entr1.get()
    list1.delete(0,END)
    ss = '/Platform/Destiny2/Armory/Search/DestinyInventoryItemDefinition/'+gettxt+'?lc=ko'
    r = requests.get(origin + ss, headers=HEADERS);
    print(r.json())
    touch = r.json()

    with open('./data/touch.pickle','wb') as fw:
        pickle.dump(touch, fw)

    totalResult = touch.get("Response").get("results").get("totalResults")
    name = [0] * totalResult
    for i in range(totalResult):
        name[i] = touch.get("Response").get("results").get("results")[i].get("displayProperties").get("name")
    print(name)

    #리스트 목록에 검색된 것들
    for ii in range(totalResult):
        list1.insert(ii,name[ii])
    return name

def findinformation():
    global anchor_str, item_response, getyou_num

    #선택된 리스트의 이름을 가져온다...인데 이름말고 순서를 들고 와야함
    anchor_str = list1.get(ANCHOR)
    #튜플 형태로 선택된 위치를 준다. [0]사용으로 번호 뽑기
    in_to = list1.curselection()

    print(anchor_str)
    with open('./data/touch.pickle','rb') as f:
        data = pickle.load(f)

    getyou_num = data.get("Response").get("results").get("results")[in_to[0]].get("hash")
    print(getyou_num)
    item_response = Checking_file_DestinyInventoryItemDefinition(getyou_num)
    print(item_response)
    image_upload = item_response.get("Response").get("displayProperties").get("icon")
    phtoimage_down(image_upload)
    phtoimage_setup()
    More_information()
    item_display_tierTypeName = item_response.get("Response").get("inventory").get("tierTypeName")
    socketEntries_Legendary()

def default_weapon():
    "충격 : \n사거리 : \n안정성 : \n조작성 : \n재장전 속도 : \n분당 발사 수 : \n탄창 : "
    "조준 지원 : \n소지품 크기 : \n확대/축소 : \n반동 방향 : "

def More_information():
    global item_display_name
    item_display_name = item_response.get("Response").get("displayProperties").get("name")
    item_display_tierTypeName = item_response.get("Response").get("inventory").get("tierTypeName")
    item_display_typename = item_response.get("Response").get("itemTypeDisplayName")
    tiertyprhash = item_response.get("Response").get("inventory").get("tierTypeHash")
    stathash = list(item_response.get("Response").get("stats").get("stats").keys())
    weapon_stat_data = Checkinig_file_DestinyStatDefinition(stathash)
    print(weapon_stat_data)
    paste = item_display_name + '\n'+ item_display_tierTypeName + '\n' + item_display_typename
    label2.config(text=paste)
    label2.text = paste

def phtoimage_down(urldown):
    #os.system("curl " + origin +urldown + " > "+data_location+"icons2.jpg")
    if not os.path.isfile("./image/"+anchor_str+'.jpg'):
        request.urlretrieve(origin+urldown,image_location+anchor_str+'.jpg')
        print("다운 완료")
    return

def jsondata_down(touch,name):
    with open('./data/'+ str(name) +'.pickle', 'wb') as Handle:
        pickle.dump(touch,Handle, protocol=pickle.HIGHEST_PROTOCOL)

def jsondata_open(name):
    with open('./data/'+ str(name) +'.pickle','rb') as Handle:
        data = pickle.load(Handle)
    return data

def phtoimage_setup():
    image_change = ImageTk.PhotoImage(Image.open(image_location+anchor_str+".jpg"))
    label1.config(image=image_change)
    label1.image = image_change

def scaled(event):
    print()
    #label1.configure(image=imagephoto2)

def Checking_file_DestinyPlugSetDefinition(rprint):
    #랜덤 소켓의 정보를 가져오는 함수, 해당 파일의 체크와 불러오기 담당
    if not os.path.isfile("./data/" + str(rprint) + ".pickle"):
        ss = "/Platform/Destiny2/Manifest/DestinyPlugSetDefinition/"+str(rprint)+"/"
        r = requests.get(origin + ss, headers=HEADERS);
        reusablePlugItems = r.json()
        jsondata_down(reusablePlugItems,rprint)
    else :
        reusablePlugItems  = jsondata_open(rprint)
    return reusablePlugItems

def Checking_file_DestinyInventoryItemDefinition(getyou_hash):
    #퍽의 자세한 정보를 들고오는 함수...
    if not os.path.isfile("./data/" + str(getyou_hash) + ".pickle"):
        ss = '/Platform/Destiny2/Manifest/DestinyInventoryItemDefinition/' + str(getyou_hash) + '?lc=ko'
        r = requests.get(origin + ss, headers=HEADERS);
        displayProperties = r.json()
        jsondata_down(displayProperties, getyou_hash)
    else:
        displayProperties = jsondata_open(getyou_hash)
    return displayProperties

def Checkinig_file_DestinyStatDefinition(stathash):
    for i in range(len(stathash)):
        rprint = item_response.get("Response").get("stats").get("stats").get(stathash[i]).get("value")
        print(stathash[i])
        if not os.path.isfile("./data/" + str(stathash[i]) + ".pickle"):
            ss = "/Platform/Destiny2/Manifest/DestinyStatDefinition/" + str(stathash[i]) + "?lc=ko"
            r = requests.get(origin + ss, headers=HEADERS);
            weapon_stat_data = r.json()
            jsondata_down(weapon_stat_data,stathash[i])
        else:
            weapon_stat_data = jsondata_open(stathash[i])
    return weapon_stat_data

def scope_socket():
    global reusablePlugItems1
    fprint = []
    list_donw1.delete(0, END)
    rprint = item_response.get("Response").get("sockets").get("socketEntries")[1].get("randomizedPlugSetHash")

    reusablePlugItems1 = Checking_file_DestinyPlugSetDefinition(rprint)

    list_len = reusablePlugItems1.get("Response").get("reusablePlugItems")

    for i in range(len(list_len)):
        fprint.append(reusablePlugItems1.get("Response").get("reusablePlugItems")[i].get("plugItemHash"))
    for i in range(len(list_len)):
        getyou_hash = fprint[i]
        displayProperties = Checking_file_DestinyInventoryItemDefinition(getyou_hash)
        item_name = displayProperties.get("Response").get("displayProperties").get("name")
        list_donw1.insert(i, item_name)

def magazine_socket():
    global reusablePlugItems2
    fprint = []
    list_donw2.delete(0, END)
    rprint2 = item_response.get("Response").get("sockets").get("socketEntries")[2].get("randomizedPlugSetHash")

    reusablePlugItems2 = Checking_file_DestinyPlugSetDefinition(rprint2)

    list_len = reusablePlugItems2.get("Response").get("reusablePlugItems")

    for i in range(len(list_len)):
        fprint.append(reusablePlugItems2.get("Response").get("reusablePlugItems")[i].get("plugItemHash"))

    for i in range(len(list_len)):
        getyou_hash = fprint[i]
        displayProperties = Checking_file_DestinyInventoryItemDefinition(getyou_hash)
        item_name = displayProperties.get("Response").get("displayProperties").get("name")
        list_donw2.insert(i, item_name)

def trait1_socket():
    global reusablePlugItems3
    fprint = []
    list_donw3.delete(0, END)
    rprint3 = item_response.get("Response").get("sockets").get("socketEntries")[3].get("randomizedPlugSetHash")

    reusablePlugItems3 = Checking_file_DestinyPlugSetDefinition(rprint3)

    list_len = reusablePlugItems3.get("Response").get("reusablePlugItems")

    for i in range(len(list_len)):
        fprint.append(reusablePlugItems3.get("Response").get("reusablePlugItems")[i].get("plugItemHash"))

    for i in range(len(list_len)):
        getyou_hash = fprint[i]
        displayProperties = Checking_file_DestinyInventoryItemDefinition(getyou_hash)
        if displayProperties.get("Response").get('itemTypeDisplayName') == '강화된 속성':
            item_name = '*' + displayProperties.get("Response").get("displayProperties").get("name")
        else:
            item_name = displayProperties.get("Response").get("displayProperties").get("name")
        list_donw3.insert(i, item_name)

def trait2_socket():
    global reusablePlugItems4
    fprint = []
    list_donw4.delete(0, END)
    rprint4 = item_response.get("Response").get("sockets").get("socketEntries")[4].get("randomizedPlugSetHash")

    reusablePlugItems4 = Checking_file_DestinyPlugSetDefinition(rprint4)

    list_len = reusablePlugItems4.get("Response").get("reusablePlugItems")

    for i in range(len(list_len)):
        fprint.append(reusablePlugItems4.get("Response").get("reusablePlugItems")[i].get("plugItemHash"))

    for i in range(len(list_len)):
        getyou_hash = fprint[i]
        displayProperties = Checking_file_DestinyInventoryItemDefinition(getyou_hash)
        if displayProperties.get("Response").get('itemTypeDisplayName') == '강화된 속성':
            item_name = '*' + displayProperties.get("Response").get("displayProperties").get("name")
        else:
            item_name = displayProperties.get("Response").get("displayProperties").get("name")
        list_donw4.insert(i, item_name)

def socketEntries_Legendary():
    scope_socket()
    magazine_socket()
    trait1_socket()
    trait2_socket()
    #label2.config(text=name_sum)

#등록 버튼을 누르면 작동하는 함수, 누르게 되면 전역변수에 선택한 소켓 리스트를 저장, 이걸 변환해야 한다..허허
def socket_selection1():
    global socket_selection1_get, selection1
    selection1 = []
    list_socket1 = []
    listtext = '--------'
    labels1.config(text=listtext)
    labels1.text = listtext
    socket_selection1_get = list_donw1.curselection()
    socket_selection1_name_get = [list_donw1.get(i) for i in list_donw1.curselection()]
    for f in range(len(socket_selection1_name_get)):
        textsum = socket_selection1_name_get[f]
        listtext = listtext+ '\n' + textsum
    listtext = listtext + "\n--------"
    labels1.config(text=listtext)
    labels1.text = listtext
    list_socket1 = reusablePlugItems1.get("Response").get("reusablePlugItems")
    for i in socket_selection1_get:
        selection1.append(list_socket1[i].get("plugItemHash"))

def socket_selection2():
    global socket_selection2_get, selection2
    selection2 = []
    selection2.clear()
    list_socket2 = []
    listtext = '--------'
    labels2.config(text=listtext)
    labels2.text = listtext
    socket_selection2_get = list_donw2.curselection()
    socket_selection2_name_get = [list_donw2.get(i) for i in list_donw2.curselection()]
    for f in range(len(socket_selection2_name_get)):
        textsum = socket_selection2_name_get[f]
        listtext = listtext+ '\n' + textsum
    listtext = listtext + "\n--------"
    labels2.config(text=listtext)
    labels2.text = listtext
    list_socket2 = reusablePlugItems2.get("Response").get("reusablePlugItems")
    for i in socket_selection2_get:
        selection2.append(list_socket2[i].get("plugItemHash"))
    print(selection2)

def socket_selection3():
    global socket_selection3_get, selection3
    selection3 = []
    list_socket3 = []
    listtext = '--------'
    labels3.config(text=listtext)
    labels3.text = listtext
    socket_selection3_get = list_donw3.curselection()
    socket_selection3_name_get = [list_donw3.get(i) for i in list_donw3.curselection()]
    for f in range(len(socket_selection3_name_get)):
        textsum = socket_selection3_name_get[f]
        listtext = listtext+ '\n' + textsum
    listtext = listtext + "\n--------"
    labels3.config(text=listtext)
    labels3.text = listtext
    list_socket3 = reusablePlugItems3.get("Response").get("reusablePlugItems")
    for i in socket_selection3_get:
        selection3.append(list_socket3[i].get("plugItemHash"))

def socket_selection4():
    global socket_selection4_get, selection4
    selection4 = []
    list_socket4 = []
    listtext = '--------'
    labels4.config(text=listtext)
    labels4.text = listtext
    socket_selection4_get = list_donw4.curselection()
    socket_selection4_name_get = [list_donw4.get(i) for i in list_donw4.curselection()]
    for f in range(len(socket_selection4_name_get)):
        textsum = socket_selection4_name_get[f]
        listtext = listtext+ '\n' + textsum
    listtext = listtext + "\n--------"
    labels4.config(text=listtext)
    labels4.text = listtext
    list_socket4 = reusablePlugItems4.get("Response").get("reusablePlugItems")
    for i in socket_selection4_get:
        selection4.append(list_socket4[i].get("plugItemHash"))

def make_dim_wishlist():
    dimwishlist = 'dimwishlist:item='
    dimwishperks = '&perks='
    paste = '//' + item_display_name + '\n//notes:\n'

    a = []
    if not selection1:
        print("None 1")
    else:
        a.append(selection1)
    if not selection2:
        print("None 2")
    else:
        a.append(selection2)
    if not selection3:
        print("None 3")
    else:
        a.append(selection3)
    if not selection4:
        print("None 4")
    else:
        a.append(selection4)

    caselist = list(itertools.product(*a))

    for i in caselist:
        i = str(i)
        i = i.replace("(","")
        i = i.replace(")", "")
        i = i.replace(", ", ",")
        sumsum = dimwishlist + str(getyou_num) + dimwishperks + str(i) + '\n'
        text1.insert(1.0, sumsum)
    text1.insert(1.0, paste)

def specificity():
    global frame_down1,frame_down2,frame_down3,frame_down4, main_frame2
    global list_donw1,list_donw2,list_donw3,list_donw4
    global btns1, btns2, btns3, btns4
    global labels1, labels2, labels3, labels4
    main_frame2 = Frame(root, bg='#FFF38A', bd=20)
    frame_down1 = Frame(main_frame2)
    frame_down2 = Frame(main_frame2, bg='#BDFFE3')
    frame_down3 = Frame(main_frame2)
    #frame_down4 = Frame(main_frame2)
    list_donw1 = Listbox(frame_down2,width=15,height=0,selectmode='multiple')
    list_donw2 = Listbox(frame_down2,width=15,height=0,selectmode='multiple')
    list_donw3 = Listbox(frame_down2,width=15,height=0,selectmode='multiple')
    list_donw4 = Listbox(frame_down2,width=15,height=0,selectmode='multiple')

    btns1 = Button(frame_down1, text="등록1", command=socket_selection1,width=14,height=0)
    btns2 = Button(frame_down1, text="등록2", command=socket_selection2,width=14,height=0)
    btns3 = Button(frame_down1, text="등록3", command=socket_selection3,width=14,height=0)
    btns4 = Button(frame_down1, text="등록4", command=socket_selection4,width=14,height=0)

    labels1 = Label(frame_down3,text="--------",width=14,height=0)
    labels2 = Label(frame_down3,text="--------",width=14,height=0)
    labels3 = Label(frame_down3,text="--------",width=14,height=0)
    labels4 = Label(frame_down3,text="--------",width=14,height=0)

    main_frame2.pack()
    frame_down1.pack(side=TOP,anchor=N)
    frame_down2.pack(side=TOP,anchor=S)
    frame_down3.pack(side=BOTTOM,anchor=N)
    #frame_down3.pack(side=LEFT,anchor=N)
    #frame_down4.pack(side=LEFT,anchor=N)

    btns1.pack(side=LEFT,anchor=N)
    btns2.pack(side=LEFT, anchor=N)
    btns3.pack(side=LEFT, anchor=N)
    btns4.pack(side=LEFT, anchor=N)

    list_donw1.pack(side=LEFT, anchor=N)
    list_donw2.pack(side=LEFT, anchor=N)
    list_donw3.pack(side=LEFT, anchor=N)
    list_donw4.pack(side=LEFT, anchor=N)

    labels1.pack(side=LEFT, anchor=N)
    labels2.pack(side=LEFT, anchor=N)
    labels3.pack(side=LEFT, anchor=N)
    labels4.pack(side=LEFT, anchor=N)

def seting():
    global imagephoto,label1, btn1, list1, combo1, btn2, scroll1, frame1, frame2, main_frame, frame3
    global frame1_left,frame1_right, scroll1, label2, entr1
    main_frame = Frame(root, bg='light blue', bd=10 )
    frame1 = Frame(main_frame,bd=6,bg='white')
    frame2 = Frame(main_frame, bg='red')
    frame3 = Frame(main_frame,bg='light green',relief="solid")
    frame1_left = Frame(frame1)
    frame1_right = Frame(frame1)

    imagephoto = ImageTk.PhotoImage(Image.open(data_location+"main.jpg"))
    label1 = Label(frame2, image=imagephoto)
    entr1 = Entry(frame1_left, width=20)
    entr1.insert(END, "내일")
    btn1 = Button(frame1_left, text="상세 검색", command=findinformation)

    scroll1 = Scrollbar(frame1_right,orient="vertical")
    list1 = Listbox(frame1_right, selectmode='extended',height=0, yscrollcommand=scroll1.set)
    combo1 = ttk.Combobox(frame1, width=20,textvariable=str)
    btn2 = Button(frame1_left, text="아이템 검색", command=btndef)
    label2 = Label(frame3,width=20, bd=5)

def seting_ui():
    main_frame.pack()
    frame1.pack(side=TOP)
    frame1_left.pack(side=LEFT)
    frame1_right.pack(side=RIGHT)
    frame2.pack(side=LEFT)
    frame3.pack(side=RIGHT)
    entr1.pack(side=TOP)
    btn1.pack(side=BOTTOM, fill=X)
    btn2.pack(side=BOTTOM, fill=X, anchor=S)
    #txt_detalie.pack()
    list1.pack(side=LEFT)
    scroll1.pack(side=RIGHT,fill=Y)
    #combo1.grid(row=1,column=0)
    label1.pack()
    label2.pack()
    specificity()

def text_gui():
    global main_frame3,text1

    main_frame3 = Frame(root, bg='#C3E873', bd=10)
    text1 = Text(main_frame3,width=30,height=5)
    btni1 = Button(main_frame3,width=10,height=0,command=make_dim_wishlist)

    main_frame3.pack()
    btni1.pack(side=LEFT, anchor=N)
    text1.pack(side=RIGHT, anchor=N)


if __name__ == "__main__":
    seting()
    seting_ui()
    text_gui()
    root.mainloop()