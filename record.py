#!/bin/python3

# Plik jest tylko w celu nagrania próbek do porównania.

from numpy import test
import sounddevice as sd
import time
import scipy.io.wavfile as wav


def recordReferenceAudio(file, duration=7, samplerate=16000):
    print("Przeczytaj dwa zdania które zostaną nagrane i zapisane jako referencyjna próbka")
    print("1. Nazywam się Cezary Baryka i posiadam szklany dom")
    print("2. To będzie moja próbka głosu do tego systemu")
    print("nagrywanie zacznie się za 3 sekundy")
    time.sleep(3)
    print("nagrywam...")
    try:
        recording = sd.rec(int(duration*samplerate),samplerate,channels=1,dtype='int16')
        sd.wait()
        wav.write(str(file)+".wav",samplerate,recording)
        print("Nagrane!")
        return
    except:
        print("Błąd nagrywania dźwięku")
        return

def recordTestAudio(file, duration=2, samplerate=16000):
    print("Przeczytaj to krótkie zdanie aby potwierdzić swoją tożsamość:")
    print("Jebać żydów")
    print("nagrywanie zacznie się za 3 sekundy")
    time.sleep(3)
    print("nagrywam...")
    try:
        recording = sd.rec(int(duration*samplerate),samplerate,channels=1,dtype='int16')
        sd.wait()
        wav.write(str(file)+".wav",samplerate,recording)
        print("Nagrane!")
        return
    except:
        print("Błąd nagrywania próbki testowej")
        return 


print("Podaj nazwe pod ktora zapisać plik referencyjny")
ref = str(input())
print("Podaj nazwe pod ktora zapisać plik test")
test = str(input())
recordReferenceAudio(file=ref)
recordTestAudio(file=test)
