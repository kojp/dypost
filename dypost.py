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
index=0

def post(event, resalt):
    
    # テキストボックスの内容を取得
    t = text.get()
    
    #投稿先がInboxでない場合
    if appendToInbox==0:
        dict={'token'  :  token, 'file_id' : file_id,'changes' : [{"action": "insert","parent_id": parent_node_id,"index": index,"content": t}]}
        response = requests.post('https://dynalist.io/api/v1/doc/edit', json.dumps(dict), headers={'Content-Type': 'application/json'})
        
        #file_idやparent_node_idの設定にエラーがある場合の表示
        if file_id=="" or parent_node_id=="":
            mess = tkinter.Label(root, text="設定エラー：file_idやparent_node_idの値が記入されていません。",font=("","9"),bg="#ff0000")
            mess.place(x=30,y=100)
    
    #投稿先がInboxである場合
    elif appendToInbox==1:
        dict = {'token'  : token,'index'  :  index,'content'  : t}
        response = requests.post('https://dynalist.io/api/v1/inbox/add', json.dumps(dict), headers={'Content-Type': 'application/json'})
    
    #appendToInboxの設定にエラーがある場合の表示
    else:
        mess = tkinter.Label(root, text="設定エラー：appendToInboxの値が0または1になっていません。",font=("","9"),bg="#ff0000")
        mess.place(x=30,y=100)
        
    #responseをJSON形式に変換
    r=json.loads(response.text)
    
    #responseを表示するラベル
    #投稿が成功した場合
    if r["_code"]=="Ok":
        res = tkinter.Label(root, text=r["_code"]+": "+t+"          ",font=("","12"),bg="#ffffff")  #「12」はフォントサイズ。bgは背景色。いずれも変更可能。
        res.place(x=30,y=80)
        
        #投稿した成功した場合は入力欄の内容を消す
        text.delete(0, tkinter.END)
        
        resalt=1
        return resalt
        
    #投稿が不成功の場合
    else:
        res = tkinter.Label(root, text="NG ("+r["_code"]+': '+t+")",bg="#ff0000",font=("","12"))
        res.place(x=30,y=80)
    
    #入力欄にフォーカスする
    text.focus_set()

###Enterキーが押されたときのアクション
def enter(event):
    post(event, 0)

###Control + Enterキーが押されたときのアクション
def postclose(event):
    resalt=post(event, 0)
    if resalt==1:
        root.destroy()  #ウィンドウを閉じる

###Escキーが押されたときのアクション
def clear(event):
    text.delete(0, tkinter.END)  #入力欄の内容を消す
    text.focus_set()

###ウィンドウ
root = tkinter.Tk()
if appendToInbox==1:
    root.title("Append to inbox of Dynalist")  #タイトルバーのタイトル
else:
    root.title("Append to Dynalist")  #タイトルバーのタイトル
root.geometry("500x200")  #ウィンドウの大きさ(px)
root.configure(bg='#ffffff')  #ウィンドウの背景色。変更可能

###入力欄
text = tkinter.Entry(root,font=("","12"),bg='#ffffff',fg='black')  #「12は」入力欄のフォントサイズ。bgは背景色、fgは文字色。いずれも変更可能。
text.pack(fill='x',padx=30,pady=30,anchor=tkinter.CENTER)
text.bind('<Key-Return>', enter)  #投稿するためのキー
text.bind('<Control-Return>',postclose)  #投稿し、エラーがなければウィンドウを閉じるためのキー
text.bind('<Key-Escape>', clear)  #入力欄の内容を消すためのキー
text.focus_set()

###キー操作を説明するラベル
h2=tkinter.Label(root, text="<Ctrl + Enter> : Post & Close",font=("","9"),bg="#ffffff")
h2.pack(anchor=tkinter.W,side=tkinter.BOTTOM,padx=30)

h1=tkinter.Label(root, text="<Enter> : Post / <Esc> : Clear",font=("","9"),bg="#ffffff")
h1.pack(anchor=tkinter.W,side=tkinter.BOTTOM,padx=30)

root.mainloop()
