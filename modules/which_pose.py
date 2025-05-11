import numpy as np

def classify_pose(keypoints: np.ndarray) -> str:
    """
    判断动作：举左手、举右手、举双手、双手平举
    加强了对关键点置信度的判断，避免误判。
    """

    # 提取关键点
    nose = keypoints[0]
    left_shoulder = keypoints[5]
    right_shoulder = keypoints[6]
    left_wrist = keypoints[9]
    right_wrist = keypoints[10]

    conf_thresh = 0.3

    # 定义是否关键点存在
    def valid(p):
        return p[2] > conf_thresh

    # --- 高度判断 ---
    def is_raised(wrist, reference):
        return wrist[1] < reference[1]

    def is_horizontal(wrist, shoulder, reference):
        return abs(wrist[1] - shoulder[1]) < 40 and wrist[1] > reference[1]

    # 所有点置信度
    l_ok = valid(left_wrist)
    r_ok = valid(right_wrist)
    nose_ok = valid(nose)
    l_sh_ok = valid(left_shoulder)
    r_sh_ok = valid(right_shoulder)

    if l_ok and r_ok and nose_ok and is_raised(left_wrist, nose) and is_raised(right_wrist, nose):
        return "Both Hands Up"

    # 单手举手要放在中间，不能被上面的 if 拦截
    elif l_ok and nose_ok and is_raised(left_wrist, nose):
        return "Left Hand Up"
    elif r_ok and nose_ok and is_raised(right_wrist, nose):
        return "Right Hand Up"

    elif l_ok and r_ok and l_sh_ok and r_sh_ok and nose_ok and \
        is_horizontal(left_wrist, left_shoulder, nose) and \
        is_horizontal(right_wrist, right_shoulder, nose):
        return "Arms Sideways"

    return "Unknown"
