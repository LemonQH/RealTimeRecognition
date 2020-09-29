import uuid
import time
import websocket
import hashlib
import json
import tkinter as tk
from tkinter import filedialog,messagebox,ttk

app_key = '75fbed84cfaXXXXX'
app_secret = '3XXXXXXXXXXXX'



class file():
    def __init__(self,path):
        self.path=path
        root1 = tk.Tk()
        root1.title("netease youdao translation test")
        frm = tk.Frame(root1)
        frm.grid(padx='80', pady='80')

        labelresult = tk.Label(frm, text='翻译结果：')
        labelresult.grid(row=0, column=0)
        text_result = tk.Text(frm, width='40', height='20')
        text_result.grid(row=2, column=1)


def recognise(filepath,language_type):
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



def on_message(ws, message):
    # print('=========message=====:'+message)
    result=json.loads(message)
    # result=json.loads(str(message, encoding="utf-8"))

    # print(resultmessage)
    try:
        resultmessage1 = result['result'][0]
        resultmessage2 = resultmessage1["st"]['sentence']
        print(resultmessage2)
    except Exception as e:
        print('')




def on_error(ws, error):
    print(error)


def on_close(ws):
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