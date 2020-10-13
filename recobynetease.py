import uuid
import time
import websocket
import hashlib
import json
import tkinter as tk
from tkinter import filedialog,messagebox,ttk



app_key = '75fbed84cfac08b4'
app_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
result_arr=[]
class file():
    def __init__(self,path):
        self.path=path

def recognise(filepath,language_type):
    print('l:'+language_type)
    global file_path
    file_path=filepath
    nonce = str(uuid.uuid1())
    curtime = str(int(time.time()))
    signStr = app_key + nonce + curtime + app_secret
    print(signStr)
    sign = encrypt(signStr)

    uri = "wss://openapi.youdao.com/stream_asropenapi?appKey=" + app_key + "&salt=" + nonce + "&curtime=" + curtime + \
          "&sign=" + sign + "&version=v1&channel=1&format=wav&signType=v4&rate=16000&langType=" + language_type
    print(uri)
    start(uri, 1600)


def encrypt(signStr):
    hash = hashlib.sha256()
    hash.update(signStr.encode('utf-8'))
    return hash.hexdigest()


def print_resule(arr):
    text_result.delete('1.0',tk.END)
    for n in arr:
        text_result.insert("insert", n + '\n')
#接收socket消息并处理
def on_message(ws, message):
    result=json.loads(message)
    resultmessage= result['result']
    if resultmessage:
        resultmessage1 = result['result'][0]
        resultmessage2 = resultmessage1["st"]['sentence']
        print(resultmessage2)
        #text_result.insert(tk.END, resultmessage2+'\n')
        result_arr.append(resultmessage2)


def on_error(ws, error):
    print(error)

#结束socket会话后，打印结果
def on_close(ws):
    print_resule(result_arr)
    print("### closed ###")


def on_open(ws):
    count = 0
    file_object = open(file_path, 'rb')
    while True:
        chunk_data = file_object.read(1600)
        ws.send(chunk_data, websocket.ABNF.OPCODE_BINARY)
        time.sleep(0.05)
        count = count + 1
        if not chunk_data:
            break
    print(count)
    ws.send('{\"end\": \"true\"}', websocket.ABNF.OPCODE_BINARY)



def start(uri,step):

    websocket.enableTrace(True)

    ws = websocket.WebSocketApp(uri,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()
    root.mainloop()


#输出结果的对话框
root = tk.Tk()
root.title("result")
frm = tk.Frame(root)
frm.grid(padx='80', pady='80')
text_result = tk.Text(frm, width='40', height='20')
text_result.grid(row=0, column=1)