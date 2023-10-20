import cv2
import numpy as np
import os

IM_WIDTH = 1280
IM_HEIGHT = 720


def draw_landmarks(image, landmarks):

    radius = 5
    # Check if image width is greater than 1000 px.
    # To improve visualization.
    if (image.shape[1] > 1000):
        radius = 5

    # for idx, kpt_data in enumerate(landmarks):
    loc_x, loc_y = landmarks[:2].astype("int").tolist()

    cv2.circle(image,
               (loc_x, loc_y),
               radius,
               color=(255, 0, 0),
               thickness=-1,
               lineType=cv2.LINE_AA)

    return image


def draw_boxes(image, detections, class_name="worm", score=None, color=(0, 255, 0)):

    font_size = 0.25 + 0.07 * min(image.shape[:2]) / 100
    font_size = max(font_size, 0.5)
    font_size = min(font_size, 0.8)
    text_offset = 3

    thickness = 0.5
    # Check if image width is greater than 1000 px.
    # To improve visualization.
    if (image.shape[1] > 1000):
        thickness = 2

    xCenter, yCenter, width, height = detections[:4].astype("int").tolist()
    xmin, ymin, xmax, ymax = detections[:4].astype("int").tolist()

    conf = round(float(detections[-1]), 2)
    cv2.rectangle(image,
                  (xmin, ymin),
                  (xmax, ymax),
                  color=color,
                  thickness=thickness,
                  lineType=cv2.LINE_AA)

    display_text = f"{class_name}"

    if score is not None:
        display_text += f": {score:.2f}"

    (text_width, text_height), _ = cv2.getTextSize(display_text,
                                                   cv2.FONT_HERSHEY_SIMPLEX,
                                                   font_size, 2)

    cv2.rectangle(image,
                  (xmin, ymin),
                  (xmin + text_width + text_offset, ymin -
                   text_height - int(15 * font_size)),
                  color=color, thickness=-1)

    image = cv2.putText(
        image,
        display_text,
        (xmin + text_offset, ymin - int(10 * font_size)),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_size,
        (0, 0, 0),
        2, lineType=cv2.LINE_AA,
    )

    return image


def visualize_annotations(image, box_data, keypoints_data):

    image = image.copy()

    box_data = np.asarray(box_data)
    keypoints_data = np.asarray(keypoints_data)

    shape_multiplier = np.array(image.shape[:2][::-1])  # (W, H).
    # Final absolute coordinates (xmin, ymin, xmax, ymax).
    denorm_boxes = np.zeros_like(box_data)

    # # De-normalize center coordinates from YOLO to (xmin, ymin).
    # denorm_boxes[:2] = (shape_multiplier / 2) * \
    #     (np.subtract((np.multiply(box_data[:2], 2)[:2]), box_data[2:]))
    # print("denorm_boxes: {}".format(denorm_boxes))

    # # De-normalize width and height from YOLO to (xmax, ymax).
    # denorm_boxes[2:] = denorm_boxes[:2] + \
    #     (box_data[2:] * shape_multiplier)

     # De-normalize center coordinates from YOLO to (xmin, ymin).
    denorm_boxes[:, :2] = (shape_multiplier/2.) * (2*box_data[:,:2] - box_data[:,2:])
 
    # De-normalize width and height from YOLO to (xmax, ymax).
    denorm_boxes[:, 2:] = denorm_boxes[:,:2] + box_data[:,2:]*shape_multiplier
 

    for boxes, kpts in zip(denorm_boxes, keypoints_data):
        # De-normalize landmark coordinates.
        kpts[:2] *= shape_multiplier
        image = draw_boxes(image, boxes)
        image = draw_landmarks(image, kpts)

    return image


def main():
    dir = "/home/alvaro/uja/tfg/datasets/customWormPoseDataset_v2/"
    file_name = "frame_00000177"
    annotationsFile = open(os.path.join(
        dir, "labels/train/{}.txt".format(file_name)), "r")
    annotations = annotationsFile.read()
    annotations = annotations.split('\n', 1)

    box_data = []
    keypoints_data = []
    for a in annotations:
        box = a.split()
        box = np.array(box[1:5], dtype=float)
        box_data.append(box)

        kp = a.split()
        kp = np.array(kp[5:], dtype=float)
        keypoints_data.append(kp)

    image = cv2.imread(os.path.join(
        dir, "images/train/{}.jpg".format(file_name)))
    image = visualize_annotations(image, box_data, keypoints_data)
    annotationsFile.close()

    cv2.imshow("Window", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    pass


if __name__ == "__main__":
    main()
