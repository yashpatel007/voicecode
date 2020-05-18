import pyperclip
import speech_recognition as sr
import pyautogui
import pyaudio
import sys
import threading

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QComboBox

pypath = "./codesnippets/python/"
pydict = {"hello world": "print('Hello World!')\n",
          "for loop": "for i in range(10):\ncontinue\n",
          "while loop": "i=0\nwhile(i<10):\nbreak\n",
          "dictionary": "dictionary = dict()\n",
          "set": "s = set()\n",
          "empty list": "li = []",
          "list comp": "lc = [print(i) for i in range(10)]",
          "boolean list": "bl = [False for i in range [10]]\n",
          "traverse matrix": "for i in range():\n for j in range():\n",
          "list": "arr = [i for i in  range(10)]\n",
          "map": "map ={'key':'value'}\n",
          "class": "class myclass(Object):\ndef __init__(self):\npass \ndef method1():\npass \n\bobj = myclass()\n",
          "try": "try:\n#some code \n\bexcept:\n#handle exception \n",
          "switch": "def switch(i):\nswitcher={ 0: \n,1: \n,2: \n \breturn switcher.get(i,'Invalid')\n",
          "import collections": "import collections",
          "make heap": "heap.txt",
          "quicksort": "quicksort.txt",
          "bubble sort": "bubblesort.txt"
          }

cpppath = "./codesnippets/cpp/"
cppdict = {
    "initialize": "#include<iostream>\n#include<stdlib.h>\nint main( ){ \n cout<< 'hello world';\n",
    "for": "for(int i=0; i<10; i++){\n break;\n",
    "while": "while(true){\n break; \n}\n",
    "traverse matrix": "for(int i=0;i<10;i++){\n for(int j=0; j<10;j++){\n\n",
    "bubble sort": "bubblesort.txt"
}

htmlpath = "./codesnippets/html/"
htmldict = {'html template': 'plaintemplate.txt'}


class VoiceCode():
    def __init__(self):
        # recognizer
        self.play = True
        self.r = sr.Recognizer()
        self.initRecognizer()
        self.mic = sr.Microphone()
        self.language = "Python"
        self.microphones = sr.Microphone.list_microphone_names()

    def initRecognizer(self):
        self.r.energy_threshold = 400
        self.r.dynamic_energy_threshold = True
        pass

    def initMic(self, idx):
        #microphones = sr.Microphone.list_microphone_names()
        self.mic = sr.Microphone(device_index=idx)
        #self.mic = self.setMic(microphones)
        pass

    def setMic(self, microphones):
        global sr
        print("choose your microphone")
        for i, microphone in enumerate(microphones):
            print(i, ". ", microphone)
        while (True):
            mic_index = int(input("Enter Index: "))
            if(mic_index >= 0 and mic_index < len(microphones)):
                break
            print("Wrong input please enter valid number\n")
        print("Selected mic: ", microphones[mic_index])
        mic = sr.Microphone(device_index=mic_index)
        return mic

    def setLanguage(self, lang):
        # print("select language")
        # for i, language in enumerate(self.languages):
        #     print(i, ". ", language)
        # while(True):
        #     idx = int(input("Enter Index: "))
        #     if(idx >= 0 and idx < len(self.languages)):
        #         break
        #     print("please enter valid index")
        # return self.languages[idx]
        self.language = lang

    def processvoice(self):
        try:
            while self.play:
                print("listening")
                with self.mic as source:
                    self.r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.r.listen(source)

                voice = self.r.recognize_google(audio, show_all=True)
                print("command :", voice)
                if(not voice):
                    continue
                results = set()
                for item in voice.get("alternative"):
                    results.add(item.get("transcript").lower())
                self.processtext(results)

        except sr.RequestError:
            print("API Unavailable")
        except sr.UnknownValueError:
            print("not recognized")
        except KeyboardInterrupt:
            print("Press Ctrl-C to terminate while statement")
        pass

    def processtext(self, voice):
        if(self.language == "Python"):
            for cmd in voice:
                if(cmd in pydict):
                    result = pydict.get(cmd)
                    if(result.endswith(".txt")):
                        result = self.readAndPrint(pypath+result)
                    pyautogui.write(result)
                    break

        if(self.language == "C++"):
            for cmd in voice:
                if(cmd in cppdict):
                    result = cppdict.get(cmd)
                    if(result.endswith(".txt")):
                        result = self.readAndPrint(cpppath+result)
                    pyautogui.write(result)
                    break

        if(self.language == "Java"):
            pass

        if(self.language == "HTML"):
            for cmd in voice:
                if(cmd in htmldict):
                    result = htmldict.get(cmd)
                    if(result.endswith(".txt")):
                        result = self.readAndPrint(htmlpath+result)
                    pyautogui.write(result)
                    break
        pass

    def readAndPrint(self, filename):
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            s = [(i) for i in lines]
            print("executing")
            return "".join(s)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    vc = VoiceCode()

    def startvoicetype():
        startbtn.setEnabled(False)
        print("starting")
        vc.play = True
        vc.initMic(int(micoption.currentIndex()))
        vc.setLanguage(str(langoption.currentText()))

        def run():
            try:
                vc.processvoice()
            except KeyboardInterrupt:
                print("Press Ctrl-C to terminate while statement")
                pass

        thread = threading.Thread(target=run)
        thread.start()

    def stopvoicetype():
        startbtn.setEnabled(True)
        stopbtn.hasFocus()
        print("stopping")
        print(threading.enumerate())
        vc.play = False

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('VoiceCode')
    layout = QHBoxLayout()

    micoption = QComboBox()
    micoption.addItems(vc.microphones)

    langoption = QComboBox()
    langoption.addItems(["Python", "Java", "C++", "HTML"])

    startbtn = QPushButton('play')
    startbtn.clicked.connect(startvoicetype)  # Connect clicked to greeting()
    stopbtn = QPushButton('stop')
    stopbtn.clicked.connect(stopvoicetype)

    layout.addWidget(langoption)
    layout.addWidget(micoption)
    layout.addWidget(startbtn)
    layout.addWidget(stopbtn)
    msg = QLabel('')
    layout.addWidget(msg)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())
