import xml.etree.ElementTree as ET
import os
import shutil
import random
import sys


# Return whether the point coordinates pased are contained on the square
WORM_CLASS_INDEX = 0
IM_WIDTH = -1
IM_HEIGHT = -1


def pointContained(pointX, pointY, sqrX1, sqrY1, sqrX2, sqrY2):
  if (pointX >= sqrX1 and pointX <= sqrX2 and pointY >= sqrY1 and pointY <= sqrY2):
    return True
  return False


def pointContained(point, box):
  x_coef = IM_WIDTH * 0.1
  y_coef = IM_HEIGHT * 0.05
  if (point.coordX >= (box.coordX1 - x_coef) and point.coordX <= (box.coordX2 + x_coef) and point.coordY >= (box.coordY1 - y_coef) and point.coordY <= (box.coordY2 + y_coef)):
    return True
  return False


class Point:
  def __init__(self, pX, pY):
    self.coordX = pX
    self.coordY = pY

  def __repr__(self):
    return ("<Point(x,y)>:{}, {}".format(self.coordX, self.coordY))


class Box:
  def __init__(self, pX1, pY1, pX2, pY2):
    self.coordX1 = pX1
    self.coordY1 = pY1
    self.coordX2 = pX2
    self.coordY2 = pY2

  def __repr__(self):
    return("<Box(x1,y1,x2,y2)>: {}, {}, {}, {}".
           format(self.coordX1, self.coordY1, self.coordX2, self.coordY2))

# Data for each worm annotation


class WormAnnotatedData:
  def __init__(self, point=None, box=None):

    # Inicialice point and box if passed
    self.point = point
    self.box = box

  def getPoint(self):
    return self.point

  def getBox(self):
    return self.box

  def __repr__(self):
    if (self.point):
      return(self.point.__repr__())
    elif (self.box):
      return(self.box.__repr__())
    else:
      return ("")


class ImageInfo:
  def __init__(self, frame):
    self.imageName = 'img_N' + frame
    self.frameNum = frame
    self.wormData = []

  def addPoint(self, pX, pY):
    self.wormData.append(WormAnnotatedData(point=Point(pX, pY)))

  def addPoint(self, point):
    self.wormData.append(WormAnnotatedData(point=point))

  def addBox(self, xtl, ytl, xbr, ybr):
    self.wormData.append(WormAnnotatedData(box=Box(xtl, ytl, xbr, ybr)))

  def addBox(self, box):
    self.wormData.append(WormAnnotatedData(box=box))

  def getPoints(self):
    toRet = []
    for el in self.wormData:
      if el.getPoint():
        toRet.append(el.getPoint())
    return toRet

  def getBoxes(self):
    toRet = []
    for el in self.wormData:
      if el.getBox():
        toRet.append(el.getBox())
    return toRet

  def __repr__(self):
    return ("<Frame {}>: {}".format(self.frameNum, self.wormData))


class NormalicedObject:
  def __init__(self, point, box):
    self.classIndex = WORM_CLASS_INDEX
    self.xCenter = (
        (((box.coordX2 - box.coordX1) / 2) + box.coordX1) / IM_WIDTH)
    self.yCenter = (
        (((box.coordY2 - box.coordY1) / 2) + box.coordY1) / IM_HEIGHT)
    self.width = ((box.coordX2 - box.coordX1) / IM_WIDTH)
    self.height = ((box.coordY2 - box.coordY1) / IM_HEIGHT)
    self.keypoints = []
    self.keypoints.append(
        Point(point.coordX / IM_WIDTH, point.coordY / IM_HEIGHT))
    self.kpVisibility = 2

  def __repr__(self):
    return ("{} {} {} {} {} {} {} {}".format(self.classIndex, self.xCenter, self.yCenter, self.width, self.height, self.keypoints[0].coordX, self.keypoints[0].coordY, self.kpVisibility))


def parseXML(xmlFile):
  # Create tree element
  tree = ET.parse(xmlFile)

  # Get root element
  root = tree.getroot()

  # List for all labels at the job
  allLabels = []

  # Iterate over meta items
  for item in root.findall('./meta/job/labels'):

    for labelField in item:
      newLabel = {}
      for labelItems in labelField:
        # Add each field from label to the dictionary
        newLabel[labelItems.tag] = labelItems.text.encode('utf8')
      allLabels.append(newLabel)

  imageWidth = -1
  imageHeight = -1
  # Obtain absolute image width and height for later compute relative point positions
  for sizeFields in root.findall('./meta/original_size'):
    for field in sizeFields:
      if (field.tag == 'width'):
        global IM_WIDTH
        imageWidth = int(field.text)
        IM_WIDTH = imageWidth
      if (field.tag == 'height'):
        global IM_HEIGHT
        imageHeight = int(field.text)
        IM_HEIGHT = imageHeight
  # print("Width:{}, height:{}".format(imageWidth, imageHeight))

  # Create a dictionary frame:ImageInfo. For each frame a new entry will be created
  frames = {}

  # Find tracks in data
  for track in root.findall('./track'):
    # print(track.get('label'), track.get('id'))
    # For each marked element check if its frame has been added
    for markedEl in track:
      frameNum = markedEl.get('frame')
      frameHeadPoints = markedEl.get('points')
      frameBoxX1 = markedEl.get('xtl')
      frameBoxY1 = markedEl.get('ytl')
      frameBoxX2 = markedEl.get('xbr')
      frameBoxY2 = markedEl.get('ybr')

      # If track is for head then Create a Point object corresponding to the head
      if (track.get('label') == 'head'):
        head = Point(float(frameHeadPoints.split(
            ',')[0]), float(frameHeadPoints.split(',')[1]))
        # print("New head point created:{}".format(head))

      # If track is for box then Create a Box object corresponding to the box
      elif (track.get('label') == 'worm_box'):
        box = Box(float(frameBoxX1), float(frameBoxY1),
                  float(frameBoxX2), float(frameBoxY2))
        # print("New box created:{}".format(box))

      # If the dictionary entry corresponding to the frame has not been created, create one
      if (not frames.get(frameNum)):
        # print("Frame {} added".format(frameNum))
        # Create the ImageInfo object corresponding to the frame
        frames[frameNum] = ImageInfo(frameNum)

      # The object info found will be added to the current ImageInfo
      if (track.get('label') == 'head'):  # Adding a head point
        frames[frameNum].addPoint(head)
      elif (track.get('label') == 'worm_box'):  # Adding a box points
        frames[frameNum].addBox(box)

  return frames


# Return an array of objects, each corresponds to a worm in the image.
def getObjectsNormaliced(points, boxes):
  toRet = []
  for box in boxes:
    for point in points:
      if pointContained(point=point, box=box):
        toRet.append(NormalicedObject(point=point, box=box))
  return toRet


def setUpYoloDataset(frames, framesImagesDir):
  framesKeyList = list(frames.keys())

  # Import images folder
  # framesImagesDir = os.path.join('..', 'framesExtracted/')
  framesList = os.listdir(framesImagesDir)
  framesList.sort()

  # Create directories
  datasetLabelsDir = os.path.join('..', 'dataset', 'labels')
  datasetImagesDir = os.path.join('..', 'dataset', 'images')

  try:
    os.makedirs(datasetLabelsDir, exist_ok=False)
    print("Directory {} created".format(datasetLabelsDir))
    os.makedirs(datasetImagesDir, exist_ok=False)
    print("Directory {} created".format(datasetImagesDir))
  except OSError as error:
    print("Directory {} cannot be created".format(error))

  frameKeysIterator = iter(framesKeyList)
  nextKey = next(frameKeysIterator)

  for frame in framesList:

    originalImagePath = os.path.join(framesImagesDir, frame)
    destinationPath = os.path.join(datasetImagesDir, frame)
    splitName = frame.split('_', 1)
    frameNumStr = splitName[1].split('.')[0]
    frameNumInt = int(frameNumStr)

    if (frameNumInt == int(nextKey)):
      shutil.copyfile(originalImagePath, destinationPath)
      print("\nframe_{}:".format(frameNumStr))
      frame = frames.get(nextKey)
      objects = getObjectsNormaliced(frame.getPoints(), frame.getBoxes())
      # print(objects)
      annotationFile = open(os.path.join(
          datasetLabelsDir, "frame_{}.txt".format(frameNumStr)), "a")
      # print("Data will be writted to {}".format(annotationFile))
      for obj in objects:
        # print(obj)
        annotationFile.write(obj.__repr__())
        annotationFile.write("\n")

      annotationFile.close()
      try:
        nextKey = next(frameKeysIterator)
      except StopIteration as e:
        pass


def splitDataset(train, val, test, datasetDir):
  if ((train + val + test) != 100):
    print("Not valid split")
  else:
    print(os.listdir(datasetDir))
    labelsDir = os.path.join(datasetDir, "labels")
    imagesDir = os.path.join(datasetDir, "images")
    if (len(os.listdir(labelsDir)) != len(os.listdir(imagesDir))):
      print("Images/labels dir incomplete!")
    else:
      labelsList = os.listdir(labelsDir)
      labelsList.sort()
      imagesList = os.listdir(imagesDir)
      imagesList.sort()
      numItems = len(labelsList)
      numTrain = numItems * (train / 100)
      numVal = numItems * (val / 100)
      numTest = numItems - (numTrain + numVal)

      merged = list(zip(labelsList, imagesList))
      random.shuffle(merged)

      labelsList = [item[0] for item in merged]
      imagesList = [item[1] for item in merged]

      labelsTrainDir = os.path.join(labelsDir, "train")
      labelsValDir = os.path.join(labelsDir, "val")
      labelsTestDir = os.path.join(labelsDir, "test")

      imagesTrainDir = os.path.join(imagesDir, "train")
      imagesValDir = os.path.join(imagesDir, "val")
      imagesTestDir = os.path.join(imagesDir, "test")

      try:
        os.mkdir(labelsTrainDir)
        print("Directory {} created".format(labelsTrainDir))
        os.mkdir(labelsValDir)
        print("Directory {} created".format(labelsValDir))
        os.mkdir(labelsTestDir)
        print("Directory {} created".format(labelsTestDir))

        os.mkdir(imagesTrainDir)
        print("Directory {} created".format(imagesTrainDir))
        os.mkdir(imagesValDir)
        print("Directory {} created".format(imagesValDir))
        os.mkdir(imagesTestDir)
        print("Directory {} created".format(imagesTestDir))

        index = 0
        while index < numItems:
          while (index < (numItems - numVal - numTest)):
            print("File {} to move".format(index))
            shutil.move(os.path.join(labelsDir, labelsList[index]), os.path.join(
                labelsTrainDir, labelsList[index]))
            shutil.move(os.path.join(imagesDir, imagesList[index]), os.path.join(
                imagesTrainDir, imagesList[index]))
            print("Moving {} to {}".format(os.path.join(
                labelsDir, labelsList[index]), os.path.join(labelsTrainDir, labelsList[index])))
            print("Moving {} to {}".format(os.path.join(
                imagesDir, imagesList[index]), os.path.join(imagesTrainDir, imagesList[index])))
            index += 1
          while (index < (numItems - numTest)):
            print("File {} to move".format(index))
            shutil.move(os.path.join(labelsDir, labelsList[index]), os.path.join(
                labelsValDir, labelsList[index]))
            shutil.move(os.path.join(imagesDir, imagesList[index]), os.path.join(
                imagesValDir, imagesList[index]))
            print("Moving {} to {}".format(os.path.join(
                labelsDir, labelsList[index]), os.path.join(labelsValDir, labelsList[index])))
            print("Moving {} to {}".format(os.path.join(
                imagesDir, imagesList[index]), os.path.join(imagesValDir, imagesList[index])))
            index += 1
          while (index < numItems):
            print("File {} to move".format(index))
            shutil.move(os.path.join(labelsDir, labelsList[index]), os.path.join(
                labelsTestDir, labelsList[index]))
            shutil.move(os.path.join(imagesDir, imagesList[index]), os.path.join(
                imagesTestDir, imagesList[index]))
            print("Moving {} to {}".format(os.path.join(
                labelsDir, labelsList[index]), os.path.join(labelsTestDir, labelsList[index])))
            print("Moving {} to {}".format(os.path.join(
                imagesDir, imagesList[index]), os.path.join(imagesTestDir, imagesList[index])))
            index += 1

      except OSError as error:
        print(error)


def main():

  # First arguments passed is annotations xml file
  frames = parseXML(sys.argv[1])

  # Second argument passed is dataset for imageFrames
  setUpYoloDataset(frames, sys.argv[2])

  splitDataset(80, 10, 10, "../dataset")


if __name__ == "__main__":
  main()