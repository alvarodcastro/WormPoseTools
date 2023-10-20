# xml-to-yolov8
Python script to convert labeleled data in XML file to Yolov8 required dataset format.
The dataset label format used for training YOLO pose models is as follows:

1. One text file per image: Each image in the dataset has a corresponding text file with the same name as the image file and the ".txt" extension.
2. One row per object: Each row in the text file corresponds to one object instance in the image.
3. Object information per row: Each row contains the following information about the object instance:
    * Object class index: An integer representing the class of the object (e.g., 0 for person, 1 for car, etc.).
    * Object center coordinates: The x and y coordinates of the center of the object, normalized to be between 0 and 1.
    * Object width and height: The width and height of the object, normalized to be between 0 and 1.
    * Object keypoint coordinates: The keypoints of the object, normalized to be between 0 and 1.


Here is an example of the label format for pose estimation task:

* Format with Dim = 2

`<class-index> <x> <y> <width> <height> <px1> <py1> <px2> <py2> ... <pxn> <pyn>` 

Format with Dim = 3

`<class-index> <x> <y> <width> <height> <px1> <py1> <p1-visibility> <px2> <py2> <p2-visibility> <pxn> <pyn> <p2-visibility>`

In this format, `<class-index>` is the index of the class for the object,`<x> <y> <width> <height>` are coordinates of bounding box, and `<px1> <py1> <px2> <py2> ... <pxn> <pyn>` are the pixel coordinates of the keypoints. The coordinates are separated by spaces.

**The current implementation of the script supports only for Dim = 2 format annotation**
It supports converting XML annotation to Yolov8 required format, sync annotations with video frames extracted setting up the whole dataset directory, and splitting dataset into training, validation and test dataset according to passed arguments.
