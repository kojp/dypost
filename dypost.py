import tkinter
import json
import requests
import webbrowser

###Secret token
token='SECRET_TOKEN'

###投稿先をInboxにするかどうか
#Inboxにする=1 / Inboxにしない=0
appendToInbox=1

###ドキュメントのid＝書き込む対象のドキュメントのidの指定
#appendToInbox=0にしている場合は必須
file_id='YOUR_FILE_ID'

###親ノードのid＝書き込みたい内容の1階層上位に相当するアイテム（行）のidの指定
#appendToInbox=0にしている場合は必須
parent_node_id='YOUR_PARENT_NODE_ID'

###記入位置を先頭にするか、末尾にするか
#先頭にする = 0
#末尾にする = -1
index= 0

def post(event, resalt):
    
    # テキストボックスの内容を取得
    t = text.get()
    
    #チェックボタンの状態に従ってappendToIndexの値を再指定
    if bln.get():
        appendToInbox=1
    else:
        appendToInbox=0
        
    #ラジオボタンの状態を取得
    rb=var.get()
    
    #ラジオボタンの状態に従ってindexの値を再指定
    if rb==0:
        index=0
    else:
        index=-1
    
    #投稿先がInboxでない場合
    if appendToInbox==0:
        dict={'token'  :  token, 'file_id' : file_id,'changes' : [{"action": "insert","parent_id": parent_node_id,"index": index,"content": t}]}
        response = requests.post('https://dynalist.io/api/v1/doc/edit', json.dumps(dict), headers={'Content-Type': 'application/json'})
    
    #投稿先がInboxである場合
    elif appendToInbox==1:
        dict = {'token'  : token,'index'  :  index,'content'  : t}
        response = requests.post('https://dynalist.io/api/v1/inbox/add', json.dumps(dict), headers={'Content-Type': 'application/json'})
    
    #appendToInboxの設定に間違いがある場合の表示
    else:
        mess = tkinter.Label(root, text="設定エラー：appendToInboxの値が0または1になっていません。",font=("","9"),bg="#ff0000")
        mess.place(x=30,y=120)
        
    #responseをJSON形式に変換
    r=json.loads(response.text)
    
    #responseを表示するラベル
    #投稿が成功した場合
    if r["_code"]=="Ok":
        res = tkinter.Label(root, text=r["_code"]+": "+t+"          ",font=("","12"),bg="#ffffff")  #「12」はフォントサイズ。bgは背景色。いずれも変更可能。
        res.place(x=30,y=120)
        
        #投稿が成功した場合は入力欄の内容を消す
        text.delete(0, tkinter.END)
        
        resalt=1
        return resalt
        
    #投稿が不成功の場合にエラーを表示
    else:
        res = tkinter.Label(root, text="NG ("+r["_code"]+': '+t+")",bg="#ff0000",font=("","12"))
        res.place(x=30,y=120)
        
        #secret tokenの値が間違っている場合のエラー
        if r["_code"]=="InvalidToken":
            mess = tkinter.Label(root, text="設定エラー：Secret tokenの値が間違っています。",font=("","9"),bg="#ff0000")
            mess.place(x=30,y=140)
            mess2 = tkinter.Label(root, text="対処法：tokenの値を修正してください。",font=("","9"),bg="#ff0000")
            mess2.place(x=30,y=160)
        
        #Inboxに関するエラー
        if appendToInbox==1:
            if r["_code"]=="NoInbox":
                mess = tkinter.Label(root, text="設定エラー：DynalistでInboxの位置が設定されていないか、またはInbox削除されています。",font=("","9"),bg="#ff0000")
                mess.place(x=30,y=140)
                mess2 = tkinter.Label(root, text="対処法：DynalistでInboxの位置をもう一度決めてください。",font=("","9"),bg="#ff0000")
                mess2.place(x=30,y=160)
        
        if appendToInbox==0:
            #file_idの値に間違いがある場合の表示
            if r["_code"]=="NotFound":
                mess = tkinter.Label(root, text="設定エラー：書き込み対象のドキュメントがDynalistに存在しません。",font=("","9"),bg="#ff0000")
                mess.place(x=30,y=140)
                mess2 = tkinter.Label(root, text="対処法：file_idの値を修正してください。",font=("","9"),bg="#ff0000")
                mess2.place(x=30,y=160)
        
            #parent_node_id_idの値に間違いがある場合の表示
            if r["_code"]=="NodeNotFound":
                    mess = tkinter.Label(root, text="設定エラー：書き込み対象の親ノードがDynalistに存在しません。",font=("","9"),bg="#ff0000")
                    mess.place(x=30,y=140)
                    mess2 = tkinter.Label(root, text="対処法：parent_node_idの値を修正してください（空白は不可）。",font=("","9"),bg="#ff0000")
                    mess2.place(x=30,y=160)
    
    #入力欄にフォーカスする
    text.focus_set()
    
###Enterキーが押されたときのアクション
def enter(event):
    post(event, 0)
    text.focus_set()

###Control + Enterキーが押されたときのアクション
def postclose(event):
    resalt=post(event, 0)
    if resalt==1:
        root.destroy()  #ウィンドウを閉じる

###Escキーが押されたときのアクション(1)
def clear(event):
    text.delete(0, tkinter.END)  #入力欄の内容を消す
    text.focus_set()
    
def focus(event):
    text.focus_set()
    
def github(event):
    webbrowser.open("https://github.com/kojp/dypost")
        
###ウィンドウ
root = tkinter.Tk()
root.title("Append to Dynalist")
root.geometry("500x240") #230
root.configure(bg='#ffffff')  #ウィンドウの背景色。変更可能
root.bind('<Key-Return>', enter)  #投稿するためのキー
root.bind('<Control-Return>', postclose)  #投稿し、エラーがなければウィンドウを閉じるためのキー
root.bind('<Key-Escape>', clear)  #入力欄の内容を消すためのキー
root.bind('<Control-f>', focus)

###本文用入力欄
text = tkinter.Entry(root,font=("","12"),bg='#ffffff',fg='black')  #「12は」入力欄のフォントサイズ。bgは背景色、fgは文字色。いずれも変更可能。
text.pack(fill='x',padx=30,pady=30,anchor=tkinter.CENTER)
text.focus_set()

###投稿ボタン
button1=tkinter.Button(root, text="投稿",width="5",height=2,font=("","10"))
button1.place(x=30,y=70)
button1.bind('<Button-1>', enter)

###投稿・終了ボタン
button3=tkinter.Button(root, text="投稿 & 終了",width="7",height=2,font=("","10"))
button3.place(x=110,y=70)
button3.bind('<Button-1>', postclose)
button3.bind('<Key-Return>', postclose)

'''
###消去ボタン
button2=tkinter.Button(root, text="消去",width="3",height=2,font=("","10"))
button2.place(x=190,y=70)
button2.bind('<Button-1>', clear)
button2.bind('<Key-Return>', clear)
'''

#チェックボタン用変数
bln = tkinter.BooleanVar()
if appendToInbox==1:
    bln.set(True)
else:
    bln.set(False)

###チェックボタン
chb = tkinter.Checkbutton(root, variable=bln, text='Inbox',bg="#ffffff")
chb.place(x=205, y=70)

#ラジオボタン用変数
var = tkinter.IntVar()

#indexの値と同じvalueのラジオボタンにチェックを入れる
var.set(index)

### ラジオボタン
rdo1 = tkinter.Radiobutton(root, value=0, variable=var, text='先頭',bg="#ffffff",font=("","9"))
rdo1.place(x=265, y=70)

rdo2 = tkinter.Radiobutton(root, value=-1, variable=var, text='末尾',bg="#ffffff",font=("","9"))
rdo2.place(x=323, y=70)

h4=tkinter.Label(root, text="<Shift>またはマウスで選択",font=("","9"),bg="#ffffff")
h4.place(x=205, y=90)

###キー操作を説明するラベル
h2=tkinter.Label(root, text="<Ctrl + Enter> : 投稿し閉じる",font=("","9"),bg="#ffffff")
h2.pack(anchor=tkinter.W,side=tkinter.BOTTOM,padx=30)

h3=tkinter.Label(root, text="<Control + F> : 入力欄にフォーカス",font=("","9"),bg="#ffffff")
h3.pack(anchor=tkinter.W,side=tkinter.BOTTOM,padx=30)

h1=tkinter.Label(root, text="<Enter> : 投稿 / <Esc> : 消去",font=("","9"),bg="#ffffff")
h1.pack(anchor=tkinter.W,side=tkinter.BOTTOM,padx=30)

###リンク
link = tkinter.Label(root, text="Github", fg="blue", cursor="hand2",bg="#ffffff")
link.place(x=430,y=220)
link.bind("<Button-1>", github)

root.mainloop()
