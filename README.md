# Multimodal Biometric System

## Backend

Our entire backend is written in Python, and we use the Flask framework for communication with websites. Additionally, to enable login functionality and retain logged-in users, we utilize `flask_login`.

---

### Path Management Functions

The `makeDirs` and `get_upload_folder` functions are used to create and manage folders where user data is stored. These folders include:  
- **db**: Contains data of registered users.  
- **tmp**: Contains data of users who are currently logging in.  

---

### Embedding Saving Functions

The functions `take_photo` and `record_voice` take the username and, depending on the function, either a photo or a voice sample.

- **`take_photo`**:  
   1. The file is decoded from Base64 and saved as `img.png` in the appropriate folder.  
   2. An embedding of the photo is created using the `create_embedding` function.  
   3. If the embedding is created successfully, the photo is deleted as it is no longer needed.  
   4. If embedding creation fails (e.g., no face is detected), an appropriate message is returned.  

- **`record_voice`**:  
   - Unlike `take_photo`, this function does not immediately create an embedding. Instead, the decoded file is saved as `reference.wav` in the appropriate folder.

---

### User Authentication Functions

Using the functions `getUser` and `verification`, we verify whether a user is registered in the database (i.e., has a folder in `db/`). Next, we call functions that check the similarity of samples submitted by the user.  

If both functions return a positive result, the user is considered logged in, and their samples are deleted from the `tmp/` folder.  

---

### Paths

Our backend also handles redirecting users to appropriate pages using the `@app.route()` decorators. The following routes are available:  
- **/**: Main page, generates the `main.html` file.  
- **/sign_up**: A page where users can register or check if they are already registered.  
- **/log_in**: A page where users can log in.  
- **/protected**: A page that only logged-in users can access.  
- **/logout**: Logs out the user upon accessing this page.  

Additionally, several routes using the POST method are described below:  
- **/take_photo**: Users send their photo to the server.  
- **/record_voice**: Users send their voice sample to the server.  
- **/log_in**: Users attempt to log in to the website.  
- **/sign_up**: Users attempt to register on the website.

---

## Face

The file `face.py` contains two functions responsible for communicating with the model:  

- **`create_embedding`**: Creates an embedding based on an input photo and saves the matrix in the `emb.txt` file in the appropriate folder.  
- **`verify_face`**: Takes two user embeddings and calculates the cosine distance between them, similar to the DeepFace framework. It then checks whether the calculated distance is within the specified threshold and returns the corresponding result.

---

## Voice

The file `voice.py` contains two functions responsible for voice verification:  

- **`voiceCheck`**:  
   - Takes the username to be verified as a parameter.  
   - Retrieves the appropriate voice samples and sends them to a function that calculates similarity.  
   - Checks whether the similarity is higher than the specified threshold and returns either `True` or `False`.  

- **`compareAudios`**:  
   - Accepts two audio files and a sound encoder as input.  
   - Calculates embeddings from the files and returns the cosine similarity between them.  

