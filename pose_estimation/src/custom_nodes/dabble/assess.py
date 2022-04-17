"""
Custom node for assessing good or bad posture.
"""

from typing import Any, List, Tuple, Dict
import cv2
from peekingduck.pipeline.nodes.node import AbstractNode

# setup global constants
FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)       # opencv loads file in BGR format
RED = (255, 0, 0)
YELLOW = (0, 255, 255)
BLACK = (51, 0, 0)
THRESHOLD = 0.1               # ignore keypoints below this threshold
OFFSET = 0.03                 # offset between hip and shoulder scaled x coordinates
DIRECTION = "right"           # right-facing checks shoulder>hip, left-facing checks shoulder<hip
KP_RIGHT_SHOULDER = 6         # PoseNet's skeletal keypoints
KP_RIGHT_HIP = 12
KP_LEFT_SHOULDER = 5
KP_LEFT_HIP = 11

def map_keypoint_to_image_coords(
    keypoint: List[float], image_size: Tuple[int, int]
) -> List[int]:
    """Second helper function to convert relative keypoint coordinates to
    absolute image coordinates.
    Keypoint coords ranges from 0 to 1
    where (0, 0) = image top-left, (1, 1) = image bottom-right.

    Args:
        bbox (List[float]): List of 2 floats x, y (relative)
        image_size (Tuple[int, int]): Width, Height of image

    Returns:
        List[int]: x, y in integer image coords
    """
    width, height = image_size[0], image_size[1]
    x, y = keypoint
    x *= width
    y *= height
    return int(x), int(y)

def draw_text(img, x, y, text_str: str, color_code, fontscale: float):
   """Helper function to call opencv's drawing function,
   to improve code readability in node's run() method.
   """
   return cv2.putText(
      img=img,
      text=text_str,
      org=(x, y),
      fontFace=cv2.FONT_HERSHEY_SIMPLEX,
      fontScale=fontscale,
      color=color_code,
      thickness=2,
   )


class Node(AbstractNode):
    """Custom node to display shoulder, hip keypoints and determine posture.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)

        self.shoulder_before_hip = None
        self.posture = None

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node assesses the sitting posture of humans based on shoulder 
        to hip coordinate keypoints.

        Args:
            inputs (dict): Dictionary with keys "all".

        Returns:
            outputs (dict): Dictionary with keys "img".
        """
        # get required inputs from pipeline
        img = inputs["img"]
        keypoints = inputs["keypoints"]
        keypoint_scores = inputs["keypoint_scores"]

        img_size = (img.shape[1], img.shape[0])  # image width, height

        # print keypoint labels for shoulders and hips
        the_keypoints = keypoints[0]              # image only has one person
        the_keypoint_scores = keypoint_scores[0]  # only one set of scores
        right_shoulder = None
        right_hip = None
        left_shoulder = None
        left_hip = None

        for i, keypoints in enumerate(the_keypoints):

            keypoint_score = the_keypoint_scores[i]

            if keypoint_score >= THRESHOLD:
                x, y = map_keypoint_to_image_coords(keypoints.tolist(), img_size)
                # x_y_str = f"({x}, {y})"

                if i == KP_RIGHT_SHOULDER:
                    right_shoulder = keypoints
                    the_color = RED
                    kp_name_str = "right shoulder"
                elif i == KP_RIGHT_HIP:
                    right_hip = keypoints
                    the_color = RED
                    kp_name_str = "right hip"
                elif i == KP_LEFT_SHOULDER:
                    left_shoulder = keypoints
                    the_color = YELLOW
                    kp_name_str = "left shoulder"
                elif i == KP_LEFT_HIP:
                    left_hip = keypoints
                    the_color = YELLOW
                    kp_name_str = "left hip"
                else:
                    the_color = BLACK
                    kp_name_str = ""

                # print(i, x_y_str, keypoints, kp_name_str, keypoint_score)
                img = draw_text(img, x, y, kp_name_str, the_color, 0.7)

        # assign shoulder and hip
        if (left_shoulder is not None and left_hip is not None):
            hip = left_hip
            shoulder = left_shoulder
        elif (right_shoulder is not None and right_hip is not None):
            hip = right_hip
            shoulder = right_shoulder
        else:
            if left_shoulder is None and right_shoulder is None:
                shoulder = None
            elif left_shoulder is None:
                shoulder = right_shoulder
            elif right_shoulder is None:
                shoulder = left_shoulder

            if left_hip is None and right_hip is None:
                hip = None
            elif left_hip is None:
                hip = right_hip
            elif right_hip is None:
                hip = left_hip
        # print("shoulder vs hip", shoulder, hip)

        # compare shoulder and hip
        if (hip is not None and shoulder is not None):
            if DIRECTION == "right":
                if shoulder[0] > (hip[0] - OFFSET):
                    self.shoulder_before_hip = True
                    self.posture = "Bad :("
                else:
                    self.shoulder_before_hip = False
                    self.posture = "Good :)"
            elif DIRECTION == "left":
                if shoulder[0] < (hip[0] + OFFSET):
                    self.shoulder_before_hip = True
                    self.posture = "Bad :("
                else:
                    self.shoulder_before_hip = False
                    self.posture = "Good :)"

        posture_str = f"Posture: {self.posture}"
        img = draw_text(img, 50, 50, posture_str, BLACK, 1)

        return {"img": img}