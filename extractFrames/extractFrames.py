# Program To Read video
# and Extract Frames

import cv2
import os
import sys

# Function to extract frames


def FrameCapture(path):

    # Path to video file
    vidObj = cv2.VideoCapture(path)

    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1
    videoName = sys.argv[1]
    if (videoName.endswith('.mp4')):
        folderPath = "./{}_frames".format(videoName.split('/')[-1])
        os.mkdir(folderPath)
        while success:

            # vidObj object calls read
            # function extract frames
            success, image = vidObj.read()

            # Saves the frames with frame-count filled with 0
            fileName = "frame_" + f'{count :0>8}.jpg'
            if success:
                frameFile = os.path.join(folderPath, fileName)
                cv2.imwrite(frameFile, image)

            count += 1
    else:
        print("File type wrong")


# Driver Code
if __name__ == '__main__':

    # Calling the function
    FrameCapture(sys.argv[1])
