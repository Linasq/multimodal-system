from flask import Flask, jsonify, render_template
import cv2
import sounddevice as sd
import wave

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('stronka.html')  # Domyślnie będzie szukać w folderze 'templates'

# Strona logowania - załaduj "log_in.html"
@app.route('/log_in')
def log_in():
    return render_template('log_in.html')  # Wskaż dokładnie nazwę pliku HTML

# Strona rejestracji - załaduj "sign_up.html"
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')  # Wskaż dokładnie nazwę pliku HTML


# Funkcja do robienia zdjęcia
def take_photo(output_filename="photo.jpg"):
    cap = cv2.VideoCapture(0)  # Użycie domyślnej kamery
    if not cap.isOpened():
        return "Nie można uzyskać dostępu do kamery."

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_filename, frame)
        cap.release()
        return f"Zdjęcie zapisane jako {output_filename}"
    else:
        cap.release()
        return "Nie udało się zrobić zdjęcia."

# Funkcja do nagrywania głosu
def record_voice(output_filename="audio.wav", duration=7):
    sample_rate = 16000  # Częstotliwość próbkowania
    try:
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
        sd.wait()  # Czekaj na zakończenie nagrywania
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)  # 16-bitowe próbki
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
        return f"Dźwięk zapisany jako {output_filename}"
    except Exception as e:
        return f"Błąd podczas nagrywania: {str(e)}"

@app.route('/take_photo', methods=['POST'])
def take_photo_route():
    message = take_photo()
    return jsonify({"message": message})

@app.route('/record_voice', methods=['POST'])
def record_voice_route():
    message = record_voice()
    return jsonify({"message": message})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
