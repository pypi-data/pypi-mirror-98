import glob as g
import pyttsx3 as pt
from win32com.client import Dispatch as dis
from gtts import gTTS as gt
from playsound import playsound as ps

def skp1(txt):
    engine = pt.init()
    engine.say(txt)
    engine.runAndWait()

def spk2(tr):
    a = dis("SAPI.SpVoice").Speak
    a(str(tr))


def spk_mp3(Text, name):
    val = gt(text=Text, lang='en')
    val.save(name)
    ps(name)


def playSound(flnme):
    ps(flnme)
    
def advance_speak(TEXT, lang, file_name, slowness, play):
    sod = gt(text=TEXT, lang=lang, slow=slowness)
    sod.save(file_name)

    if play:
          ps(file_name)

def check_mp3():
    lisT = []
    for i in g.glob("*.mp3"):
          lisT.append(i)
    return lisT


def check_file(typE):
    lop = []
    for i in g.glob(typE):
          lop.append(i)

    return lop

