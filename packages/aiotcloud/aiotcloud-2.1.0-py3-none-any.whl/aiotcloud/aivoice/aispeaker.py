# -*- coding: UTF-8 -*-
from aip import AipSpeech
from aiotcloud.aivoice.playsound import playsound
import threading
from queue import Queue

class AiSpeaker(threading.Thread):
    def __init__(self,queue=Queue(),app_id,app_key,secret_key,person=3,voice=5):
        """
        appid:你所申请的百度appid
        appkey:对应的key
        secret:key所对应的secret
        person:发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
        voice:音量，取值0-15，默认为5中音量
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.client = AipSpeech(app_id, app_key, secret_key)
        self.launguage = 'zh'
        self.speed = 2
        self.vol = 5
        self.person = 3

    def speech(self,text):
        """
        异步播放文字语音
        """
        self.queue.put(text)

    def speech_sync(self,text):
        """
        同步语音合成
        """
        result = self.client.synthesis(text, 'zh', 2, {
            'vol': 5,'per':3
        })
        if not isinstance(result, dict):
            with open('auido.mp3', 'wb') as f:
                f.write(result)
        playsound('auido.mp3')

    def run(self):
        while True:
            text = self.queue.get()
            result = self.client.synthesis(text, 'zh', 2, {
                'vol': 5,'per':3
            })
            if not isinstance(result, dict):
                with open('auido.mp3', 'wb') as f:
                    f.write(result)
            playsound('auido.mp3')

