# WormPoseTools
Tools suite for Worm Pose estimation.

The main workflow used is retrieving annotated data from a video in CVAT.ai in XML format. Given that exporting frames is not supported, [extract frames tool](https://github.com/alvarodcastro/WormPoseTools/tree/main/extractFrames) will split the video passed in frames. Given the video frames and annotations in XML format, [XMLtoYolo tool](https://github.com/alvarodcastro/WormPoseTools/tree/main/xmlToYolo) will set up a Yolo-format dataset for training.
Video could be downloaded from Google Drive storage using [downloadVideo tool](https://github.com/alvarodcastro/WormPoseTools/tree/main/downloadDriveVideo).
Two set up dataset could be joined using [JoinDataset tool](https://github.com/alvarodcastro/WormPoseTools/tree/main/joinDatasets)
