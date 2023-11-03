import random

import cv2
from matplotlib import pyplot as plt

import albumentations as A
import os
import sys

KEYPOINT_COLOR = (0, 255, 0)

IM_WIDTH = -1
IM_HEIGHT = -1

# The kp format will be the required by Albumentations: (xy)


def formatLabels(file):
    annotationsFile = open(file, "r")
    annotations = annotationsFile.read()
    annotations = annotations.split('\n')
    bboxes = []
    kpts = []
    for kp in annotations:
        if (kp):
            splitKp = kp.split()
            xC, yC, width, height = splitKp[1:5]
            bboxes.append(
                [float(xC), float(yC), float(width), float(height), ])
            kpx, kpy = splitKp[-3:-1]
            kpts.append((float(kpx) * IM_WIDTH, float(kpy) * IM_HEIGHT))
            # print("Added kp({})".format(float(kpx)*IM_WIDTH))

    return [bboxes, kpts]


def createLabels(transformed):
    image = transformed['image']
    im_height, im_width = image.shape[:2]
    bboxes = transformed['bboxes']
    keypoints = transformed['keypoints']
    bbox_classes = transformed['bbox_classes']
    keypoints_classes = transformed['keypoints_classes']
    # print("Width: {}, height: {}".format(im_width, im_height))
    # print("bboxes {}".format(bboxes))
    # print("{}".format(bbox_classes))
    # print("keypoints {}".format(keypoints))
    # print("{}".format(keypoints_classes))

    labels = []
    class_index = "0"
    for box, whichBox in zip(bboxes, bbox_classes):
        line = ""
        kpX = 0
        kpY = 0
        kpV = 0  # Standard will be 0: not visible keypoint
        line += (class_index + " ")
        # print("Box {} for {}".format(box, whichBox.split('_')[1]))
        for boxParam in box:
            line += (str(boxParam) + " ")

        for kp, whichKp in zip(keypoints, keypoints_classes):
            if (whichBox.split('_')[1] == whichKp):
                # print("And a keypoint: {}".format(kp))
                kpX = kp[0]
                kpY = kp[1]
                kpV = 2

        line += (str(kpX / im_width) + " " +
                 str(kpY / im_height) + " " + str(kpV))
        labels.append(line)

    return labels


def augmentationPipeline():
    transformObject = A.Compose([
        # A.RandomSizedCrop(min_max_height=(256, 1025),
        #                   height=640, width=640, p=0.3),
        # A.HorizontalFlip(p=0.5),
        A.Perspective(p=1),
        A.Affine(rotate=[-360, 360], rotate_method="ellipse", p=1),
        A.OneOf([
                A.ChannelShuffle(p=0.1),
                A.HueSaturationValue(p=0.5),
                A.RGBShift(r_shift_limit=[-20, 80], p=0.7)
                ], p=0.8),
        A.OneOf([
                A.Equalize(p=0.3),
                A.RandomBrightnessContrast(p=0.5)
                ], p=0.4)

    ],
        bbox_params=A.BboxParams(format="yolo", label_fields=['bbox_classes']),
        keypoint_params=A.KeypointParams(
            format='xy', label_fields=['keypoints_classes']),
        p=1
    )
    return transformObject


def augmentImage(image, labels, augmentationPipeline):

    bbox_classes = ['box_worm1', 'box_worm2']
    keypoints_classes = ['worm1', 'worm2']

    # Get boxes and keypoints formatted for Albumentations
    bboxes, keypoints = formatLabels(os.path.join("./", labels))
    # print ("IN file {}".format(labels))
    # print("bboxes:{} kp:{}".format(bboxes, keypoints))

    try:
        transformed = augmentationPipeline(
            image=image,
            bboxes=bboxes,
            bbox_classes=bbox_classes,
            keypoints=keypoints,
            keypoints_classes=keypoints_classes,
        )
        return transformed

    except AssertionError:
        raise AssertionError("Wrong annotations for {}".format(labels))


def vis_keypoints(image, bboxes, keypoints, color=KEYPOINT_COLOR, diameter=5):
    image = image.copy()
    im_height, im_width = image.shape[:2]
    for (xC, yC, width, height) in bboxes:
        xmin = (xC - (width / 2)) * im_width
        xmax = (xC + (width / 2)) * im_width
        ymin = (yC - (height / 2)) * im_height
        ymax = (yC + (height / 2)) * im_height
        # print("xmin: {}\n ymin: {}\n xmax: {}\n ymax: {}".format(xmin, ymin, xmax, ymax))
        cv2.rectangle(image,
                      (int(xmin), int(ymin)),
                      (int(xmax), int(ymax)),
                      color=color,
                      thickness=2,
                      lineType=cv2.LINE_AA)
    for (x, y) in keypoints:
        cv2.circle(image, (int(x), int(y)), diameter, (0, 255, 0), -1)

    cv2.imshow("Window", image)
    while True:

        # it waits till we press a key
        key = cv2.waitKey(2000)

        # if we press esc
        if key >= 0:
            cv2.destroyAllWindows()
            break
        elif cv2.getWindowProperty('Window', cv2.WND_PROP_VISIBLE) < 1:
            cv2.destroyAllWindows()
            break
    cv2.waitKey(1)


def main():

    datasetBaseFolder = sys.argv[1]
    imagesDir = os.path.join(datasetBaseFolder, "images")
    labelsDir = os.path.join(datasetBaseFolder, "labels")

    imagesList = os.listdir(imagesDir)
    imagesList.sort()
    labelsList = os.listdir(labelsDir)
    imagesList.sort()

    augmentedDatasetPath = os.path.join("./augmentedDataset")
    imagesFolder = os.path.join(augmentedDatasetPath, "images")
    labelsFolder = os.path.join(augmentedDatasetPath, "labels")
    os.makedirs(imagesFolder, exist_ok=True)
    os.makedirs(labelsFolder, exist_ok=True)

    # number of new creations for each image
    numAugCreations = 3
    # Create augmentation pipeline
    transform = augmentationPipeline()

    for img, label in zip(imagesList, labelsList):

        print("Annotating {} with {}".format(img, label))

        frameName = img.split('.')[0]

        image = cv2.imread(os.path.join(imagesDir, img))
        labelsFileName = os.path.join(labelsDir, label)

        try:
            # Get original image shape
            global IM_WIDTH, IM_HEIGHT
            IM_HEIGHT, IM_WIDTH = image.shape[:2]
            # print("Original Shape: {} {}".format(IM_HEIGHT, IM_WIDTH))
        except AttributeError as e:
            print(
                "{}: Probably dataset format not correct. No split should be created before this point".format(e))

        try:
            for n in range(numAugCreations):

                # Transformed image and labels
                transformed = augmentImage(image, labelsFileName, transform)

                labels = createLabels(transformed)

                newImageFile = os.path.join(
                    imagesFolder, "{}aug{}.jpg".format(frameName, n))
                newLabelsFile = os.path.join(
                    labelsFolder, "{}aug{}.txt".format(frameName, n))

                # Write augmented image
                cv2.imwrite(newImageFile, transformed['image'])
                print("New image: {}".format(newImageFile))

                # vis_keypoints(
                #     transformed['image'], transformed['bboxes'], transformed['keypoints'])

                # Write augmented labels
                annotationFile = open(newLabelsFile, "a")
                for obj in labels:
                    annotationFile.write(obj)
                    annotationFile.write("\n")
                annotationFile.close()
        except AssertionError as e:
            print("Augmentation for {} cannot be created: {}".format(img, e))


if __name__ == "__main__":
    main()
