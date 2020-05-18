import pyperclip
import speech_recognition as sr
import pyautogui
import pyaudio

languages = ["C++", "Python", "Java", "HTML"]


class CallableDict(dict):
    def __getitem__(self, key):
        val = super().__getitem__(key)
        if callable(val):
            return val()
        return val


def readAndPrint(filename):
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        s = [(i+"\n") for i in lines]
        print("executing")
        return "".join(s)
    except FileNotFoundError:
        pass


pydict = CallableDict({"hello world": "print('Hello World!')\n",
                       "for loop": "for i in range(10):\ncontinue\n",
                       "while loop": "i=0\nwhile(i<10):\nbreak\n",
                       "dictionary": "dictionary = dict()\n",
                       "set": "s = set()\n",
                       "empty list": "li = []",
                       "list comp": "lc = [print(i) for i in range(10)]",
                       "boolean list": "bl = [False for i in range [10]]\n",
                       "traverse matrix": "for i in range():\n for j in range():\n",
                       "list": "arr = [i for i in  range(10)]\n",
                       "map": "map ={/'key':'value'}/\n",
                       "class": "class myclass(Object):\ndef __init__(self):\npass \ndef method1():\npass \n\bobj = myclass()\n",
                       "try": "try:\n#some code \n\bexcept:\n#handle exception \n",
                       "switch": "def switch(i):\nswitcher={ 0: \n,1: \n,2: \n \breturn switcher.get(i,'Invalid')\n",
                       "import collections": "import collections",
                       "make heap": readAndPrint("./codesnippets/python/heap.txt")
                       })
cppdict = {
    "initialize": "#include<iostream>\n#include<stdlib.h>\nint main( ){ \n cout<< 'hello world';\n",
    "for": "for(int i=0; i<10; i++){\n break;\n",
    "while": "while(true){\n break; \n}\n",
    "traverse matrix": "for(int i=0;i<10;i++){\n for(int j=0; j<10;j++){\n\n"
}

htmldict = {'html template': '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>Document</title>\n</head>\n<body>\n</body>\n</html>'}


def setMic(microphones):
    global sr
    print("choose your microphone")
    for i, microphone in enumerate(microphones):
        print(i, ". ", microphone)
    while (True):
        mic_index = int(input("Enter Index: "))
        if(mic_index >= 0 and mic_index < len(microphones)):
            break
        print("wring input please enter valid number\n")
    print("Selected mic: ", microphones[mic_index])
    mic = sr.Microphone(device_index=mic_index)
    return mic


def processtext(voice, language):
    if(language == "Python"):
        for cmd in voice:
            if(cmd in pydict):
                pyautogui.typewrite(pydict.get(cmd))
                break

    if(language == "C++"):
        for cmd in voice:
            if(cmd in cppdict):
                pyautogui.typewrite(cppdict.get(cmd))
                break

    if(language == "Java"):
        pass

    if(language == "HTML"):
        for cmd in voice:
            if(cmd in htmldict):
                pyautogui.typewrite(htmldict.get(cmd))
                break


def processvoice(recognizer, mic, language):
    try:
        while True:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source)

            voice = recognizer.recognize_google(audio, show_all=True)
            print("command :", voice)
            if(not voice):
                continue
            results = set()
            for item in voice.get("alternative"):
                results.add(item.get("transcript").lower())
            processtext(results, language)

    except sr.RequestError:
        print("API Unavailable")
    except sr.UnknownValueError:
        print("not recognized")


def setLanguage():
    global languages
    print("select language")
    for i, language in enumerate(languages):
        print(i, ". ", language)
    while(True):
        idx = int(input("Enter Index: "))
        if(idx >= 0 and idx < len(languages)):
            break
        print("please enter valid index")
    return languages[idx]


# recognizer
r = sr.Recognizer()
r.energy_threshold = 400
r.dynamic_energy_threshold = True
# with mic
mic = sr.Microphone()
microphones = sr.Microphone.list_microphone_names()
mic = sr.Microphone(device_index=2)
mic = setMic(microphones)
#language = "Python"
language = setLanguage()

print("listening")
try:
    processvoice(r, mic, language)

except KeyboardInterrupt:
    print("Press Ctrl-C to terminate while statement")
    pass
