import numpy as np

def classify_pose(keypoints: np.ndarray) -> str:
    """
    判断动作：举左手、举右手、举双手、双手平举

    Args:
        keypoints: np.ndarray, shape (17, 3), COCO 格式关键点 x, y, confidence

    Returns:
        str: 动作名称
    """

    # 提取关键点
    nose = keypoints[0]
    left_shoulder = keypoints[5]
    right_shoulder = keypoints[6]
    left_wrist = keypoints[9]
    right_wrist = keypoints[10]

    conf_thresh = 0.3

    # 判断置信度
    l_ok = left_wrist[2] > conf_thresh
    r_ok = right_wrist[2] > conf_thresh
    nose_y = nose[1]

    # --- 高度判断 ---
    def is_raised(wrist):
        return wrist[1] < nose_y  # 举过头顶

    def is_horizontal(wrist, shoulder):
        return abs(wrist[1] - shoulder[1]) < 40 and wrist[1] > nose_y  # 与肩同高 & 在鼻子下

    # --- 判断逻辑 ---
    if l_ok and r_ok:
        if is_raised(left_wrist) and is_raised(right_wrist):
            return "举双手"
        elif is_horizontal(left_wrist, left_shoulder) and is_horizontal(right_wrist, right_shoulder):
            return "双手平举"
    elif l_ok and is_raised(left_wrist):
        return "举左手"
    elif r_ok and is_raised(right_wrist):
        return "举右手"

    return "未识别"
