import pyaudio
import threading
import wave

from recobynetease import *

language_dict = {'中文': 'zh-CHS', '英语': 'en','日语':'ja','韩语':'ko'}


class Audio_model():

    def __init__(self, audio_path, language_type,is_recording):
        self.audio_path = audio_path,
        self.audio_file_name=''
        self.language_type = language_type,
        # self.language_dict=["zh-CHS","en","ja","ko"]
        self.language=language_dict[language_type]
        print(language_dict[language_type])
        self.is_recording=is_recording
        self.audio_chunk_size=1600
        self.audio_channels=1
        self.audio_format=pyaudio.paInt16
        self.audio_rate=16000

    def record_and_save(self):
        self.is_recording = True
        # self.audio_file_name=self.audio_path+'/recordtmp.wav'
        self.audio_file_name='/recordtmp.wav'

        threading.Thread(target=self.record,args=(self.audio_file_name,)).start()

    def record(self,file_name):
        print(file_name)
        p=pyaudio.PyAudio()
        stream=p.open(
            format=self.audio_format,
            channels=self.audio_channels,
            rate=self.audio_rate,
            input=True,
            frames_per_buffer=self.audio_chunk_size
        )
        wf = wave.open(file_name, 'wb')
        wf.setnchannels(self.audio_channels)
        wf.setsampwidth(p.get_sample_size(self.audio_format))
        wf.setframerate(self.audio_rate)

        # 读取数据写入文件
        while self.is_recording:
            data = stream.read(self.audio_chunk_size)
            wf.writeframes(data)
        wf.close()
        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop_and_recognise(self):
        self.is_recording=False
        recognise(self.audio_file_name,self.language)
        recognise(self.audio_file_name,self.language)
        #处理返回信息

        return '123'

