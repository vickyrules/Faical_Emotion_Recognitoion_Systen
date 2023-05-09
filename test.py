import random

import numpy as np
import cv2
import tensorflow as tf
import easygui

# Load the face detection cascade classifier
face_detection = cv2.CascadeClassifier('haar_cascade_face_detection.xml')

# Prompt the user to choose between using the camera or uploading a video file
msg = "Choose an option"
title = "Facial Expression Recognition"
choices = ["Camera", "Video File"]
choice = easygui.buttonbox(msg, title, choices)

# Initialize the camera or read the video file
if choice == "Camera":
    camera = cv2.VideoCapture(0)
elif choice == "Video File":
    path = easygui.fileopenbox()
    camera = cv2.VideoCapture(path)

# Set the camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

# Set the face detection settings
settings = {
    'scaleFactor': 1.3,
    'minNeighbors': 5,
    'minSize': (50, 50)
}

# Define the facial expression labels
labels = ['Surprise', 'Normal', 'Angry', 'Happy', 'Sad']

# Load the pre-trained Keras model
model = tf.keras.models.load_model('network-5Labels.h5')

##customize window size
# cv2.namedWindow('Facial Expression', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Facial Expression', 800, 600)

## start

total_frames = 0
correct_predictions = 0

fps = camera.get(cv2.CAP_PROP_FPS) # get frame rate of video
current_time = 0


while True:
    ret, img = camera.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected = face_detection.detectMultiScale(gray, **settings)






    for x, y, w, h in detected:
        cv2.rectangle(img, (x, y), (x+w, y+h), (245, 135, 66), 2)
        cv2.rectangle(img, (x, y), (x+w//3, y+20), (245, 135, 66), -1)
        face = gray[y+5:y+h-5, x+20:x+w-20]
        face = cv2.resize(face, (48,48))
        face = face/255.0

        predictions = model.predict(np.array([face.reshape((48,48,1))])).argmax()

        state = labels[predictions]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,state,(x+10,y+15), font, 0.5, (255, 255, 255), 2, cv2.LINE_8)

        # Calculate accuracy for each frame
        total_frames += 1
        if state == 'Normal':
            correct_predictions += 1
        accuracy = round(correct_predictions / total_frames, 2) * 100
        # Display accuracy in the video window
        
        cv2.putText(img, f'Accuracy: {accuracy:.04f}%', (20, 90), cv2.FONT_HERSHEY_COMPLEX, 1, (10, 120, 255), 2, cv2.LINE_AA)

        if choice == "Video File":
        #timeline

            timeline_position = (img.shape[1] - 100, 30)
            # Get the current position of the video in seconds
            current_pos = int(camera.get(cv2.CAP_PROP_POS_MSEC)) // 1000
            # Get the total duration of the video in seconds
            total_duration = int(camera.get(cv2.CAP_PROP_FRAME_COUNT)) // int(camera.get(cv2.CAP_PROP_FPS))
            # Calculate the current position as a percentage of the total duration
            current_percent = int(current_pos / total_duration * 100)
            # Draw a yellow bar to indicate the current position on the timeline
            cv2.rectangle(img, (0, 0), (int(current_percent * 5.12), 10), (50, 220, 255), -1)
            cv2.putText(img, f' {total_duration//60:02d}:{total_duration%60:02d}', timeline_position, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (10, 120, 255), 2,cv2.LINE_AA)
            # # Display the frame along with the timeline
            # cv2.imshow('Facial Expression', img)
        #time
            current_time = round(total_frames / fps, 2)
            minutes = int(current_time // 60)
            seconds = int(current_time % 60)
            cv2.putText(img, f'{minutes:02d}:{seconds:02d}', (20, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (10, 120, 255), 2,
                        cv2.LINE_AA)



    cv2.imshow('Facial Expression', img)

    if cv2.waitKey(5) != -1:
        break

    # Add a button to exit
    if cv2.getWindowProperty('Facial Expression', cv2.WND_PROP_VISIBLE) < 1:
        break

camera.release()
cv2.destroyAllWindows()
