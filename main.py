import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None

while True:
    # Read the current frame from the video stream
    check, frame = video.read()

    # Preprocess the frame by converting it to grayscale and applying Gaussian blurring
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)

    # Show the webcam
    cv2.imshow("Webcam", frame)

    if first_frame is None:
        first_frame = grey_frame_gau

    # Detect if user presses the 'q' key to quit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
