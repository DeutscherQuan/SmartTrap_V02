import cv2
import datetime
import os
import sys

def gstreamer_pipeline(sensor_id=0, capture_width=1920, capture_height=1080, display_width=960, display_height=540, framerate=30, flip_method=0):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def capture_image(output_directory):
    today = datetime.datetime.now()
    print(gstreamer_pipeline(flip_method=0))
    video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if video_capture.isOpened():
        try:
            ret_val, frame = video_capture.read()

            date_time = datetime.datetime.now().strftime("%y%m%d%H%M")
            img_name = "{}.jpg".format(date_time)
            full_name = os.path.join(output_directory, img_name)
            cv2.imwrite(full_name, frame)
            print("{} written!".format(img_name))
            #print(full_name)

        finally:
            video_capture.release()

    else:
        print("Error: Unable to open camera")

if __name__ == "__main__":
    output_directory = './Realtime_Data'  # Thay đổi đường dẫn tại đây
    capture_image(output_directory)

