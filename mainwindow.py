import tkinter as tk
from tkinter import filedialog,messagebox,ttk
from audioandprocess import Audio_model

au_model=Audio_model("","",False)
lang_type_dict=("中文","英语","日语","韩语")

def get_lang_type(*args):
    select=combox.get()
    au_model.language_type=lang_type_dict.index(select)
    print(au_model.language_type)

def set_result_path():
    result_path=filedialog.askdirectory()
    au_model.audio_path=result_path
    text1.insert(tk.END,result_path)

def start_rec():
    lb_Status['text']='正在录音...'
    au_model.record_and_save()

def get_result():
    lb_Status['text']='Ready'
    sr_result=au_model.stop_and_recognise()



root=tk.Tk()
root.title("netease youdao translation test")
frm = tk.Frame(root)
frm.grid(padx='80', pady='80')
# label1=tk.Label(frm,text="选择待翻译文件：")
# label1.grid(row=0,column=0)
label=tk.Label(frm,text='选择语言类型：')
label.grid(row=0,column=0)
combox=ttk.Combobox(frm,textvariable=tk.StringVar(),width=38)
combox["value"]=lang_type_dict
combox.current(0)
combox.bind("<<ComboboxSelected>>",get_lang_type)
combox.grid(row=0,column=1)

# btn_get_rec_path=tk.Button(frm,text='选择录音存储路径',command=set_result_path)
# btn_get_rec_path.grid(row=1,column=0)
# text1=tk.Text(frm,width='40', height='2')
# text1.grid(row=1,column=1)

btn_start_rec = tk.Button(frm, text='开始录音', command=start_rec)
btn_start_rec.grid(row=2, column=0)

lb_Status = tk.Label(frm, text='准备录音', anchor='w', fg='green')
lb_Status.grid(row=2,column=1)

btn_sure=tk.Button(frm,text="结束并识别",command=get_result)
btn_sure.grid(row=3,column=0)
#
# labelresult=tk.Label(frm,text='翻译结果：')
# labelresult.grid(row=4,column=0)
# combox1=ttk.Combobox(frm,textvariable=tk.StringVar(),width=38)
# combox1.grid(row=4,column=1)

root.mainloop()
