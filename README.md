# Posture Corrector
This is a tool built using [PeekingDuck's (v1.2.0)](https://github.com/aimakerspace/PeekingDuck) [pose estimation](https://peekingduck.readthedocs.io/en/latest/tutorials/01_hello_cv.html#pose-estimation) to detect changes in sitting posture in a video recording.

# How to Use
This section explains the setup for a default run of the submitted solution detecting postures of a person facing right in the video.

1. Clone repository.
```
$ git clone https://github.com/JoyLinWQ/posture_corrector.git
$ cd posture_corrector/pose_estimation
```

2. Create a virtual environment (python 3.6 to 3.9) and install PeekingDuck. For Apple Silicon Mac users, follow Custom Install [here](https://peekingduck.readthedocs.io/en/latest/getting_started/03_custom_install.html#apple-silicon-mac-installation).
```
$ conda create --name my_pd python=3.9
$ conda activate my_pd
$ pip install -U peekingduck 
```

3. Run Posture Corrector!
```
$ peekingduck run
```

4. Watch the output in a new popup window (below), where pose estimation draws shoulder and hip keypoints that are used to calculate whether a particular posture is good or bad. This output will be automatically saved to `"...\posture_corrector\pose_estimation\PeekingDuck\data\output\<timestamp>.mp4"` when the run is completed.

![solution_gif](https://github.com/JoyLinWQ/posture_corrector/blob/main/pose_estimation/PeekingDuck/data/output/solution/right-Trim.gif)


A good posture is where the shoulder keypoint is before the hip keypoint, and vice versa. A small offset is added to the hip keypoint to correct slight differences in estimated poses from actual posture.

# Customize to your desired video
This section guides more adventurous users to add your own video data source with simple changes to the configuration file.

## A. Get data
You can source for your own video containing either right-facing or left-facing postures. You may trim the video to ensure that there is a human present in all frames.

For videos obtained from YouTube, you may refer to Step 1 below.
1. Convert YouTube video to MP4 using [Online Video Converter](https://onlinevideoconverter.pro/en28/youtube-downloader-mp4).
2. Trim video to desired frames of interest.
3. Store trimmed videos in `data` folder.

Sample videos:
Two samples of trimmed video containing left-facing or right-facing postures are available in `...\posture_corrector\pose_estimation\data\sample\` for your use.

## B. Configure script
Before running, perform 3 simple configurations for your custom data sources in `pose_estimation/pipeline_config.yml` and `pose_estimation\src\custom_nodes\dabble\assess.py`. The sample containing right-facing posture is used as an example here.

1. **Input source** in `pipeline_config.yml`:
Update the path to your input video source, relative to the project folder `posture_corrector/pose_estimation`.

Example:
```
- input.visual:
    source: data/sample/right.mp4
```

2. **Direction** in `assess.py`:
Update the direction in which person is facing in the video, either to "left" or "right".

Example:
```
DIRECTION = "right"
```

3. **Offset** in `assess.py`:
You may wish to adjust the offset to see which value is more suitable for your video of interest. This uses scaled x coordinates of keypoints instead of actual image coordinates.

Example:
```
OFFSET = 0.05
```

4. Run:
```
$ cd posture_corrector/pose_estimation
$ peekingduck run
```

# Future Improvements
1. More keypoints like ears and knees can be included to have a better overall assessment of the posture. 

2. Real-time video streaming from a camera strategically placed at a user's left or right side may be used as an input data source, and the output posture detected could be sent to user's mobile application. A desired feedback could be short warning beeps when bad posture is detected so that user can instantly correct his/her posture.

# Author
Joy Lin [Email](jlwq07@hotmail.com) | [GitHub Repository Link](https://github.com/JoyLinWQ/posture_corrector)

Submitted: April 2022

# Acknowledgements
1. PeekingDuck (v1.2.0) developed by AI Singapore Computer Vision Hub
    - [GitHub](https://github.com/aimakerspace/PeekingDuck)
    - [Documentation](https://peekingduck.readthedocs.io/en/latest/)
2. Videos used in submission:
    - Sample (right-facing): [Best posture for sitting](https://www.youtube.com/watch?v=TOd_e5iZ9tM)
    - Sample (left-facing): [How to fix & improve your sitting posture](https://www.youtube.com/watch?v=2ArrRPr2huU)
    - Solution (right-facing): [Sitting posture correction](https://www.youtube.com/watch?v=IWUJbYS5VnU)
