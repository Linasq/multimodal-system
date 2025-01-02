from flask import Flask, jsonify, render_template, request
import cv2
import sounddevice as sd
import wave
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
SIGN_UP_FOLDER = 'sign_up_samples'
LOG_IN_FOLDER = 'log_in_samples'

@app.route('/')
def home():
    return render_template('main.html')

os.makedirs(SIGN_UP_FOLDER, exist_ok=True)
os.makedirs(LOG_IN_FOLDER, exist_ok=True)

def get_upload_folder(is_login):
    if is_login == 'true':  # Jeżeli is_login jest równe "true"
        return LOG_IN_FOLDER
    return SIGN_UP_FOLDER

def take_photo(username, is_login):
    if not username:
        return "Brak nazwy użytkownika."
    
    folder = get_upload_folder(is_login)  # Ustal folder na podstawie wartości is_login
    filename = secure_filename(username + ".jpg")
    filepath = os.path.join(folder, filename)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Nie można uzyskać dostępu do kamery."

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filepath, frame)
        cap.release()
        return f"Zdjęcie zapisane jako {filename}"
    else:
        cap.release()
        return "Nie udało się zrobić zdjęcia."

def record_voice(username, is_login):
    if not username:
        return "Brak nazwy użytkownika."
    
    folder = get_upload_folder(is_login)  # Ustal folder na podstawie wartości is_login
    filename = secure_filename(username + ".wav")
    filepath = os.path.join(folder, filename)
    
    sample_rate = 16000
    try:
        audio_data = sd.rec(int(7 * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
        return f"Dźwięk zapisany jako {filename}"
    except Exception as e:
        return f"Błąd podczas nagrywania: {str(e)}"
    
@app.route('/log_in')
def log_in():
    return render_template('log_in.html')  # Strona logowania

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')  # Strona rejestracji

@app.route('/take_photo', methods=['POST'])
def take_photo_route():
    username = request.form.get('username')
    is_login = request.form.get('is_login')  # Odbieramy is_login
    message = take_photo(username, is_login)
    return jsonify({"message": message})

@app.route('/record_voice', methods=['POST'])
def record_voice_route():
    username = request.form.get('username')
    is_login = request.form.get('is_login')  # Odbieramy is_login
    message = record_voice(username, is_login)
    return jsonify({"message": message})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
