import sys
import os
import random
import shutil

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

    datasetDir = sys.argv[1]
    train = input("Input train split(0/100): ")
    val = input("Input validation split(0/100): ")
    test = input("Input test split(0/100): ")
    splitDataset(int(train), int(val), int(test), datasetDir)


if __name__ == "__main__":
  main()
