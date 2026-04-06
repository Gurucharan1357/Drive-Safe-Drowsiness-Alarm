from scipy.spatial import distance as dist  # Importing distance module from scipy.spatial package to calculate distances
from imutils.video import VideoStream  # Importing VideoStream class from imutils.video package for video streaming
from imutils import face_utils  # Importing face_utils module from imutils package for facial landmarks manipulation
from pygame import mixer  # Importing mixer module from pygame package for audio mixing
from threading import Thread  # Importing Thread class from threading package for creating parallel threads
import numpy as np  # Importing numpy library for numerical computing
import argparse  # Importing argparse module for command-line argument parsing
import imutils  # Importing imutils library for image processing utility functions
import time  # Importing time module for time-related functions
import dlib  # Importing dlib library for machine learning and computer vision algorithms
import cv2  # Importing OpenCV library for computer vision tasks
import os  # Importing os module for operating system functionalities

mixer.init()  # Initialize the mixer module for audio mixing
mixer.music.load(r"C:\Users\Lenovo\Downloads\40811eyack.com.MAIL_xsbsxxypt8dh6!App\aud-20240324-wa0004_lMstCAqD.mp3")  # Load the audio file

def alarm(msg):  # Define a function to trigger an alarm
    global alarm_status  # Declare global variables for alarm status
    global alarm_status2
    global saying

    while alarm_status:  # Loop to continuously check alarm status
        print('call')  # Print statement for debugging
        s = 'espeak "' + msg + '"'  # Create a command for text-to-speech synthesis
        os.system(s)  # Execute the command to generate speech

    if alarm_status2:  # Check if the second alarm status is triggered
        print('call')  # Print statement for debugging
        saying = True  # Set saying flag to true
        s = 'espeak "' + msg + '"'  # Create a command for text-to-speech synthesis
        os.system(s)  # Execute the command to generate speech
        saying = False  # Reset saying flag

def eye_aspect_ratio(eye):  # Define a function to calculate eye aspect ratio
    A = dist.euclidean(eye[1], eye[5])  # Calculate distance between two points of the eye
    B = dist.euclidean(eye[2], eye[4])  # Calculate distance between two points of the eye
    C = dist.euclidean(eye[0], eye[3])  # Calculate distance between two points of the eye
    ear = (A + B) / (2.0 * C)  # Calculate eye aspect ratio
    return ear  # Return the eye aspect ratio

def final_ear(shape):  # Define a function to calculate final eye aspect ratio
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]  # Get the index range for left eye landmarks
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]  # Get the index range for right eye landmarks
    leftEye = shape[lStart:lEnd]  # Extract left eye landmarks
    rightEye = shape[rStart:rEnd]  # Extract right eye landmarks
    leftEAR = eye_aspect_ratio(leftEye)  # Calculate left eye aspect ratio
    rightEAR = eye_aspect_ratio(rightEye)  # Calculate right eye aspect ratio
    ear = (leftEAR + rightEAR) / 2.0  # Calculate average eye aspect ratio
    return (ear, leftEye, rightEye)  # Return the average eye aspect ratio and eye landmarks

def lip_distance(shape):  # Define a function to calculate lip distance
    top_lip = shape[50:53]  # Extract landmarks of the top lip
    top_lip = np.concatenate((top_lip, shape[61:64]))  # Concatenate additional lip landmarks
    low_lip = shape[56:59]  # Extract landmarks of the bottom lip
    low_lip = np.concatenate((low_lip, shape[65:68]))  # Concatenate additional lip landmarks
    top_mean = np.mean(top_lip, axis=0)  # Calculate the mean of top lip landmarks
    low_mean = np.mean(low_lip, axis=0)  # Calculate the mean of bottom lip landmarks
    distance = abs(top_mean[1] - low_mean[1])  # Calculate the vertical distance between lips
    return distance  # Return the lip distance

ap = argparse.ArgumentParser()  # Create an argument parser object
ap.add_argument("-w", "--webcam", type=int, default=0,  # Add an argument for webcam index
                help="index of webcam on system")
args = vars(ap.parse_args())  # Parse command-line arguments and store them as a dictionary

EYE_AR_THRESH = 0.3  # Set the eye aspect ratio threshold
EYE_AR_CONSEC_FRAMES = 30  # Set the consecutive frames for drowsiness detection
YAWN_THRESH = 20  # Set the threshold for yawning detection
alarm_status = False  # Initialize alarm status flag
alarm_status2 = False  # Initialize second alarm status flag
saying = False  # Initialize saying flag
COUNTER = 0  # Initialize counter for consecutive frames

print("-> Loading the predictor and detector...")  # Print loading message
# detector = dlib.get_frontal_face_detector()  # Use dlib's frontal face detector
detector = cv2.CascadeClassifier("C:\\Users\\Lenovo\\PycharmProjects\\Final\\.venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")  # Use OpenCV's Haar cascade classifier for face detection
predictor = dlib.shape_predictor('C:\\Users\\Lenovo\\PycharmProjects\\Final\\.venv\\Lib\\site-packages\\cv2\\data\\shape_predictor_68_face_landmarks.dat')  # Load the facial landmark predictor model

print("-> Starting Video Stream")  # Print message indicating starting of video stream
vs = VideoStream(src=args["webcam"]).start()  # Start the video stream from the webcam
# vs= VideoStream(usePiCamera=True).start()       //For Raspberry Pi
time.sleep(1.0)  # Delay for allowing the camera to warm up

while True:  # Start an infinite loop for processing video frames

    frame = vs.read()  # Read a frame from the video stream
    frame = imutils.resize(frame, width=550)  # Resize the frame for efficient processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale for facial landmark detection

    # rects = detector(gray, 0)  # Detect faces using dlib's frontal face detector
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,  # Detect faces using Haar cascade classifier
                                      minNeighbors=5, minSize=(30, 30),
                                      flags=cv2.CASCADE_SCALE_IMAGE)

    # for rect in rects
    for (x, y, w, h) in rects:  # Loop over the detected faces
        rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))  # Create dlib rectangle for the detected face

        shape = predictor(gray, rect)  # Predict facial landmarks using the dlib shape predictor
        shape = face_utils.shape_to_np(shape)  # Convert the shape object to a NumPy array

        eye = final_ear(shape)  # Calculate final eye aspect ratio
        ear = eye[0]  # Extract the eye aspect ratio
        leftEye = eye[1]  # Extract the landmarks of the left eye
        rightEye = eye[2]  # Extract the landmarks of the right eye

        distance = lip_distance(shape)  # Calculate lip distance

        leftEyeHull = cv2.convexHull(leftEye)  # Find the convex hull of the left eye landmarks
        rightEyeHull = cv2.convexHull(rightEye)  # Find the convex hull of the right eye landmarks
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)  # Draw contours around the left eye
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)  # Draw contours around the right eye

        lip = shape[48:60]  # Extract lip landmarks
        cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)  # Draw contours around the lips

        if ear < EYE_AR_THRESH:  # Check if the eye aspect ratio is below the threshold
            COUNTER += 1  # Increment the frame counter for drowsiness detection

            if COUNTER >= EYE_AR_CONSEC_FRAMES:  # Check if consecutive frames have low eye aspect ratio
                if alarm_status == False:  # Check if the alarm is not already triggered
                    alarm_status = True  # Set the alarm status to True
                    t = Thread(target=alarm, args=('wake up sir',))  # Create a thread for alarm
                    t.deamon = True  # Set the thread as daemon
                    t.start()  # Start the thread for alarm

                cv2.putText(frame, "***DROWSINESS ALERT!***", (10, 30),  # Display drowsiness alert message
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # on the frame
                mixer.music.play()  # Play the alarm sound

        else:  # If eye aspect ratio is above the threshold
            COUNTER = 0  # Reset the frame counter
            alarm_status = False  # Reset the alarm status

        if (distance > YAWN_THRESH):  # Check if lip distance exceeds yawning threshold
            cv2.putText(frame, "Sleepy!.......", (10, 30),  # Display sleepy message on the frame
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            mixer.music.play()  # Play the alarm sound
            if alarm_status2 == False and saying == False:  # Check if the second alarm is not already triggered and not speaking
                alarm_status2 = True  # Set the second alarm status to True
                t = Thread(target=alarm, args=('Wake-up take some fresh air sir',))  # Create a thread for second alarm
                t.deamon = True  # Set the thread as daemon
                t.start()  # Start the thread for second alarm
        else:  # If lip distance is below yawning threshold
            alarm_status2 = False  # Reset the second alarm status

        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),  # Display eye aspect ratio on the frame
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
        cv2.putText(frame, "YAWN: {:.2f}".format(distance), (300, 60),  # Display lip distance on the frame
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)

    cv2.imshow("Frame", frame)  # Display the processed frame
    key = cv2.waitKey(1) & 0xFF  # Wait for a key press

    if key == ord("q"):  # If 'q' is pressed, exit the loop
        break

cv2.destroyAllWindows()  # Close all OpenCV windows
vs.stop()  # Stop the video stream
