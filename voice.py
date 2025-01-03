#!/bin/python3
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
from torch import threshold

encoder = VoiceEncoder()
threshold = 0.6

# Funkcje przyszłościowe do zapisu i wczytania embeddingu z folderu, póki co bez zastosowania
def saveReferenceEmbedding(username: str,filename: str, embedding):
    try:
        np.save("db/"+username+"/"+filename+".npy",embedding)
        return
    except:
        print("Nie można zapisać pliku")
        return

def loadReferenceEmbedding(username: str,filename: str):
    try:
        emb = np.load("db/"+username+"/"+filename+".npy")
        return emb
    except:
        print("Nie można pobrać referencyjnego embeddingu!")
        return None

# Funkcja porównuje póki co pliki dźwięku, docelowo, porównywanie dźwięku test do embeddingu
def compareAudios(reference, test, encoder):
    embedding_ref = encoder.embed_utterance(reference)
    embedding_test = encoder.embed_utterance(test)
    return np.dot(embedding_ref,embedding_test)

# Funkcje operujące już na embeddingach
def compareEmbeddings(emb1, emb2):
    return np.dot(emb1,emb2)


def registerUser(username: str, referenceRecording):
    try:
        ref = preprocess_wav(referenceRecording)
        embedding = encoder.embed_utterance(ref)
        saveReferenceEmbedding(username,"voice_embedding",embedding)
    except:
        print("Problem z audio referencyjnym!")
    return


def authenticateUser(username: str, testRecording):
    test = preprocess_wav(testRecording)
    try:
        testEmbedding = encoder.embed_utterance(test)
    except:
        print("Problem z testowym audio")
        return -1

    refEmbedding = loadReferenceEmbedding(username,"voice_embedding")
    if refEmbedding is None:
        print("Błąd wczytywania embeddingu referencyjnego!")
        return -1
    return compareEmbeddings(refEmbedding, testEmbedding)

def voiceCheck(username: str):
    reference = preprocess_wav("db/"+username+".wav")
    test = preprocess_wav("tmp/"+username+".wav")
    similarity = compareAudios(reference, test,encoder)
    return similarity>threshold

# Odkomentować to do prezentacji na przygotowanych plikach

# ref = str(input("Podaj nazwę pliku referencyjnego bez .wav\n"))
# test = str(input("Podaj nazwę pliku testowego bez .wav\n"))
# ref = preprocess_wav(ref+".wav")
# test = preprocess_wav(test+".wav")
# print(f"\nPodobieństwo próbek to: {compareAudios(ref,test,encoder)}")


# To do testów rejestracji

#username = 'testUser'
#registerUser(username,'ref.wav')

