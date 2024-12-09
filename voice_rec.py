#!/bin/python3
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
from torch import embedding

encoder = VoiceEncoder()

# Funkcje przyszłościowe do zapisu i wczytania embeddingu z folderu, póki co bez zastosowania
def saveReferenceEmbedding(username: str,filename: str, embedding):
    np.save("db/admin/"+username+"/"+filename+".npy",embedding)
    return

def loadReferenceEmbedding(username: str,filename: str):
    emb = np.load("db/admin/"+username+"/"+filename+".npy")
    return emb

# Funkcja porównuje póki co pliki dźwięku, docelowo, porównywanie dźwięku test do embeddingu
def compareAudios(reference, test, encoder):
    embedding_ref = encoder.embed_utterance(reference)
    embedding_test = encoder.embed_utterance(test)
    return np.dot(embedding_ref,embedding_test)

# Funkcje operujące już na embeddingach
def compareEmbeddings(emb1, emb2):
    return np.dot(emb1,emb2)


def registerUser(username: str, referenceRecording):
    ref = preprocess_wav(referenceRecording)
    embedding = encoder.embed_utterance(ref)
    saveReferenceEmbedding(username,username+"_embedding",embedding)
    return

def authenticateUser(username: str, testRecording):
    test = preprocess_wav(testRecording)
    testEmbedding = encoder.embed_utterance(test)
    refEmbedding = loadReferenceEmbedding(username,username+"_embedding")
    return compareEmbeddings(refEmbedding, testEmbedding)



ref = str(input("Podaj nazwę pliku referencyjnego bez .wav\n"))
test = str(input("Podaj nazwę pliku testowego bez .wav\n"))
ref = preprocess_wav(ref+".wav")
test = preprocess_wav(test+".wav")
print(f"\nPodobieństwo próbek to: {compareAudios(ref,test,encoder)}")
