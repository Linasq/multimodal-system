from flask import Flask, jsonify, render_template, request, redirect, url_for
import cv2
import sounddevice as sd
import wave
import os
from werkzeug.utils import secure_filename
import face
import voice
import flask_login


app = Flask(__name__)
app.secret_key = 'test' #TODO zmienic pozniej na cos bardziej zaawansowanego

login_manager=flask_login.LoginManager()
login_manager.init_app(app)
SIGN_UP_FOLDER = 'db'
LOG_IN_FOLDER = 'tmp'

#--------------------------------------
#           FLASK LOGIN
#--------------------------------------
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in getUser():
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in getUser():
        return

    user = User()
    user.id = username
    return user


#--------------------------------------
#           FUNCTIONS
#--------------------------------------

# tworzy scieżki do wybranych folderow
def makeDirs(is_login, username):
    if is_login: 
        os.makedirs(LOG_IN_FOLDER+f'/{username}', exist_ok=True)
    else:
        os.makedirs(SIGN_UP_FOLDER+f'/{username}', exist_ok=True)


# zwraca odpowiednia sciezke do folderu
def get_upload_folder(is_login):
    if is_login == 'true':
        return LOG_IN_FOLDER
    return SIGN_UP_FOLDER


# zapisuje zdjecia w odpowiednich folderach
def take_photo(username, is_login):
    if not username:
        return "Brak nazwy użytkownika."

    makeDirs(is_login, username)
    
    folder = get_upload_folder(is_login) + "/" + username  # Ustal folder na podstawie wartości is_login
    filename = secure_filename("img.png")
    filepath = os.path.join(folder, filename)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Nie można uzyskać dostępu do kamery."

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filepath, frame)
        cap.release()
        face.create_embedding(username,is_login)
        os.remove(f'{folder}/img.png')
        return f"Zdjęcie zapisane jako {filename}"
    else:
        cap.release()
        return "Nie udało się zrobić zdjęcia."


# zapisuje audio w odpowiednich folderach
def record_voice(username, is_login):
    if not username:
        return "Brak nazwy użytkownika."

    makeDirs(is_login, username)
    
    folder = get_upload_folder(is_login) + "/" + username  # Ustal folder na podstawie wartości is_login
    filename = secure_filename("reference.wav")
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


# zwraca wszystkich zarejestrowanych uzytkownikow
def getUser():
  return os.listdir('db')


#TODO usuwac sciezke tmp/login bo zalogowaniu sie uzytkownika
# weryfikuje uzytkownika, ktory sie loguje
def verification(username):
    if username in getUser():
        face_check = face.verify_face(username)
        voice_check = voice. 
        if face_check and voice_check:
            user = User()
            user.id = username
            flask_login.login_user(user)
            return True

    return False


#--------------------------------------
#             ROUTES
#--------------------------------------
@app.route('/')
def home():
    return render_template('main.html')


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


@app.route('/protected')
@flask_login.login_required
def protected():
    return jsonify({"message":'Logged in as: ' + flask_login.current_user.id})


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


@app.route('/log_in',methods=['POST'])
def log_in_post():
    username = request.form.get('username')
    message= verification(username)
    if message:
        return redirect(url_for('protected'))
    return jsonify({"message": "bad login"})


@app.route('/sign_up',methods=['POST'])
def sign_up_post():
    username = request.form.get('username')
    user_data=[x for x in os.listdir(f'db/{username}') if os.path.isfile(os.path.join(f'db/{username}',x))]
    if len(user_data)==2:
        return jsonify({"message": "Pomyślnie zarejestrowano użytkownika "+ username})
    return jsonify({"message": "Niedokończono rejestracji"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


