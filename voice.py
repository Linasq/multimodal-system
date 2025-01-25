#!/bin/python3
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
from torch import threshold

encoder = VoiceEncoder()
threshold = 0.65


# Funkcja porównuje póki co pliki dźwięku, docelowo, porównywanie dźwięku test do embeddingu
def compareAudios(reference, test, encoder):
    embedding_ref = encoder.embed_utterance(reference)
    embedding_test = encoder.embed_utterance(test)
    return np.dot(embedding_ref,embedding_test)

def voiceCheck(username: str):
    reference = preprocess_wav("db/"+username+"/reference.wav")
    test = preprocess_wav("tmp/"+username+"/reference.wav")
    similarity = compareAudios(reference, test,encoder)
    return similarity>threshold

