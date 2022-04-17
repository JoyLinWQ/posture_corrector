# Posture Corrector
This is a tool built using PeekingDuck's (v1.2.0) pose estimation to detect changes in sitting posture in a video recording.

# How to Use
This section explains the setup for a default run of the submitted solution detecting postures of a person facing right in the video.

1. Clone repository.
```
$ git clone https://github.com/JoyLinWQ/posture_corrector.git
$ cd posture_corrector
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
