import cv2
import time

# Start users webcam
video = cv2.VideoCapture(0)
time.sleep(1)

# Set first frame to None to store the first frame in the video stream
first_frame = None

while True:
    # Read the current frame from the video stream
    check, frame = video.read()

    # Preprocess the frame by converting it to grayscale and applying Gaussian blurring
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)

    # Set first frame on first run of the loop
    if first_frame is None:
        first_frame = grey_frame_gau

    # Compare the difference between the current frame and the first frame
    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)

    # Set threshold for detecting motion
    threshold_frame = cv2.threshold(delta_frame, 105, 255, cv2.THRESH_BINARY)[1]

    # Set kernel for dilation
    dilate_frame = cv2.dilate(threshold_frame, None, 2)
    #cv2.imshow("Webcam", dilate_frame)

    # Find contours in the dilated frame and draw bounding boxes around detected objects
    contours, check = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 2000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Show the final frame with detected objects and bounding boxes
    cv2.imshow("Webcam", frame)

    # Detect if user presses the 'q' key to quit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
