# Emotion Recognition from Image

from flask import Flask, request, jsonify

app = Flask(__name__)

from PIL import Image
import numpy as np
from scipy.stats import mode
import cv2

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.layers import MaxPooling2D

cv2.ocl.setUseOpenCL(False)
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

emotion_model = Sequential()
emotion_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
emotion_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Flatten())
emotion_model.add(Dense(1024, activation='relu'))
emotion_model.add(Dropout(0.5))
emotion_model.add(Dense(7, activation='softmax'))
emotion_model.load_weights('models/emotion/trained_model.h5')

bounding_box = cv2.CascadeClassifier('models/haarcascades/haarcascade_frontalface_default.xml')

def predict(img: Image) -> str:
    gray_frame = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
    return emotion_dict[int(mode(np.array([int(np.argmax(emotion_model.predict(np.expand_dims(np.expand_dims(cv2.resize(gray_frame[i[1]:, i[0]:][:i[-1], :i[-2]], (48, 48)), -1), 0)))) for i in bounding_box.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)])))]


@app.route("/api/ai/emotion", methods=["POST"])
def get_emotion():
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream)
    return jsonify(dict(emotion=predict(img)))


if __name__ == "__main__":
    app.run(debug=True)
