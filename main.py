import cv2
import time
import glob
from datetime import datetime
import send_email

# Start users webcam
video = cv2.VideoCapture(0)
time.sleep(1)

# Set up variables
first_frame = None
status_list = []
count = 1

while True:
    status = 0
    # Read the current frame from the video stream
    check, frame = video.read()
    if not check:
        print("Could not read the frame.")

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

    # Display current date and time on the frame
    now = datetime.now()
    cv2.putText(frame, f"{now.strftime("%d/%m/%Y %H:%M:%S")}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                (0, 0, 255), 2)

    # Find contours in the dilated frame and draw bounding boxes around detected objects
    contours, check = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 2000:
            continue
        # There has been a motion detected
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            middle_image = all_images[index]

    # Send email if object has left the frame, based on the last two frame
    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[0] == 1 and status_list[1] == 0:
        send_email.email(middle_image, "utf-8")

    # Show the final frame with detected objects and bounding boxes
    cv2.imshow("Webcam", frame)

    # Detect if user presses the 'q' key to quit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
