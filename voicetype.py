import pyperclip
import speech_recognition as sr
import pyautogui
import pyaudio
import sys
import threading

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QWidget, QComboBox, QVBoxLayout, QTextEdit, QSystemTrayIcon,QMenu,QAction
from PyQt5.QtGui import QIcon

pypath = "./codesnippets/python/"
pydict = {"hello world": "print('Hello World!')\n",
          "for loop": "for i in range(10):\ncontinue\n",
          "while loop": "i=0\nwhile(i<10): \nbreak\n",
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
                # print("listening")

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
                msg.setText(cmd)
                if(cmd in pydict):
                    result = pydict.get(cmd)
                    if(result.endswith(".txt")):
                        result = self.readAndPrint(pypath+result)
                    pyautogui.write(result)
                    break

        if(self.language == "C++"):
            for cmd in voice:
                msg.setText(cmd)
                if(cmd in cppdict):
                    result = cppdict.get(cmd)
                    if(result.endswith(".txt")):
                        result = self.readAndPrint(cpppath+result)
                    pyautogui.typewrite(result)
                    break

        if(self.language == "Java"):
            pass

        if(self.language == "HTML"):
            for cmd in voice:
                msg.setText(cmd)
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
            # print("executing")
            return "".join(s)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    vc = VoiceCode()

    def startvoicetype():
        startbtn.setEnabled(False)
        micoption.setEnabled(False)
        langoption.setEnabled(False)
        action1.setEnabled(False)
        # print("starting")
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
        thread.setDaemon(True)
        thread.setName("voiceanalyzer thread")
        thread.start()

    def stopvoicetype():
        startbtn.setEnabled(True)
        micoption.setEnabled(True)
        langoption.setEnabled(True)
        action1.setEnabled(True)
        msg.setText("")
        print("stopping")
        print(threading.enumerate())
        vc.play = False
    
    def trayclicked():
        if(window.isVisible()):
            window.hide()
        else:
            window.show()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = QWidget()
    window.setWindowTitle('VoiceCode')
    
    layout = QHBoxLayout()
    
    micoption = QComboBox()
    micoption.addItems(vc.microphones)
    micoption.setFixedWidth(200)

    langoption = QComboBox()
    langoption.addItems(["Python", "Java", "C++", "HTML"])
    langoption.setFixedWidth(100)
    
    startbtn = QPushButton('play')
    startbtn.clicked.connect(startvoicetype)  # Connect clicked to greeting()
    startbtn.setFixedWidth(80)

    stopbtn = QPushButton('stop')
    stopbtn.clicked.connect(stopvoicetype)
    stopbtn.setFixedWidth(80)

    msg = QLabel('')
    msg.setStyleSheet("border-style:outset;border-width: 2px;border-radius: 200px;border-color: black;")



    layout.addWidget(langoption)
    layout.addWidget(micoption)
    layout.addWidget(startbtn)
    layout.addWidget(stopbtn)
    layout.addWidget(msg)
    
    window.setLayout(layout)
    window.setFixedSize(800,50)
    window.setWindowIcon(QIcon("appicon.png"))
    window.show()

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(QIcon("appicon.png"))
    tray.setVisible(True)



    # Create the menu
    menu = QMenu()
    action1 = QAction("start")
    action1.triggered.connect(startvoicetype)
    menu.addAction(action1)

    action2 = QAction("stop")
    action2.triggered.connect(stopvoicetype)
    menu.addAction(action2)


    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)
    tray.activated.connect(trayclicked)

    sys.exit(app.exec_())
