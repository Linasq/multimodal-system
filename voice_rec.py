#!/bin/python3
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

encoder = VoiceEncoder()

# Funkcje przyszłościowe, póki co bez zastosowania
def saveReferenceEmbedding(username: str,filename: str, embedding):
    np.save("db/admin/"+username+"/"+filename+".npy",embedding)
    return

def loadReferenceEmbedding(username: str,filename: str):
    emb = np.load("db/admin/"+username+"/"+filename+".npy")
    return emb

def compareAudios(reference, test, encoder):
    embedding_ref = encoder.embed_utterance(reference)
    embedding_test = encoder.embed_utterance(test)
    return np.dot(embedding_ref,embedding_test)

ref = str(input("Podaj nazwę pliku referencyjnego bez .wav\n"))
test = str(input("Podaj nazwę pliku testowego bez .wav\n"))
ref = preprocess_wav(ref+".wav")
test = preprocess_wav(test+".wav")
print(f"\nPodobieństwo próbek to: {compareAudios(ref,test,encoder)}")
