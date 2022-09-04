# importing the required packages
import pyautogui
import cv2
import numpy as np
import pytesseract
from datetime import datetime


# Use text recognition to parse the time from the clock coordinates
def did_time_update(x1, y1, x2, y2, image,):
    # A method that takes in the x and y coordinates of the top left corner of the football timer
    # and the x and y coordinates of the bottom right corner of the football timer
    # And then parses the time from the clock coordinates
    # use pytesseract to parse the time from the image in the specified bouncding box
    def parse_time(x1, y1, x2, y2, image):
        # crop the image to the bounding box
        cropped = image.crop((x1, y1, x2, y2))
        # convert the image to grayscale
        gray = cv2.cvtColor(np.array(cropped), cv2.COLOR_BGR2GRAY)
        # apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1
        text = pytesseract.image_to_string(gray)
        return text

    # parse the time from the image
    time = parse_time(x1, y1, x2, y2, image)
    minutes, seconds = time.split(":")
    return minutes, seconds



def record(height, width, x1, y1, x2, y2, filename):
    # A method that records the screen when the timer is incrementing
    # It takes in the arguments screen resolution hieght, width,
    # the x and y coordinates of the top left corner of the football timer
    # and the x and y coordinates of the bottom right corner of the football timer
    # And then records the screen when the timer is incrementing

    prev_minutes = 0
    prev_seconds = 0
    last_updated = datetime.now()

    # Specify resolution
    resolution = (width, height)

    # Specify video codec
    codec = cv2.VideoWriter_fourcc(*"XVID")

    # Specify frames rate. We can choose any
    # value and experiment with it
    fps = 60.0

    # Creating a VideoWriter object
    out = cv2.VideoWriter(filename, codec, fps, resolution)

    # Create an Empty window
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

    # Resize this window
    cv2.resizeWindow("Live", 480, 270)

    while True:
        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()
        minutes, seconds = did_time_update(x1, y1, x2, y2, img)
        if minutes != prev_minutes or seconds != prev_seconds:
            last_updated = datetime.now()
        if (datetime.now() - last_updated).seconds > 3:
            continue

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Write it to the output file
        out.write(frame)

        # Optional: Display the recording screen
        cv2.imshow('Live', frame)

        # Stop recording when we press 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the Video writer
    out.release()

    # Destroy all windows
    cv2.destroyAllWindows()

def main():
    # A main method that takes in the arguments screen resolution hieght, width,
    # the x and y coordinates of the top left corner of the football timer
    # and the x and y coordinates of the bottom right corner of the football timer
    # And then calls the process to record the screen when the timer is incrementing

    # create command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("height", help="height of the screen resolution", type=int)
    parser.add_argument("width", help="width of the screen resolution", type=int)
    parser.add_argument("x1", help="x coordinate of the top left corner of the football timer", type=int)
    parser.add_argument("y1", help="y coordinate of the top left corner of the football timer", type=int)
    parser.add_argument("x2", help="x coordinate of the bottom right corner of the football timer", type=int)
    parser.add_argument("y2", help="y coordinate of the bottom right corner of the football timer", type=int)
    # add the filename argument
    parser.add_argument("filename", help="name of the output file", type=str)
    record(args.height, args.width, args.x1, args.y1, args.x2, args.y2, args.filename)

#main method
if __name__ == "__main__":
    main()
