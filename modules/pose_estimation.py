# modules/pose_estimation.py
from ultralytics import YOLO
import cv2
import os


def draw_pose_connections(image, keypoints, confidence_threshold=0.3):
    """
    绘制定制骨架：加入 neck 和 pelvis 两个中点，连接更合理。

    Args:
        image (np.array): 图像。
        keypoints (list): 每人 [17, 3] 的关键点列表。
        confidence_threshold (float): 最小置信度。
    """

    skeleton = [
        (1, 2),      # 左眼 - 右眼
        (0, 17),     # 鼻子 - neck
        (5, 7), (7, 9),    # 左臂
        (6, 8), (8, 10),   # 右臂
        (17, 5), (17, 6),  # neck - 肩
        (18, 11), (18, 12),# pelvis - 髋
        (11, 13), (13, 15),# 左腿
        (12, 14), (14, 16),# 右腿
        (17, 18)           # neck - pelvis
    ]

    for person in keypoints:
        keypts = person.tolist()

        # -- 构造 neck --
        if person[5][2] > confidence_threshold and person[6][2] > confidence_threshold:
            neck = [
                (person[5][0] + person[6][0]) / 2,
                (person[5][1] + person[6][1]) / 2,
                (person[5][2] + person[6][2]) / 2
            ]
        else:
            neck = [0, 0, 0]

        # -- 构造 pelvis --
        if person[11][2] > confidence_threshold and person[12][2] > confidence_threshold:
            pelvis = [
                (person[11][0] + person[12][0]) / 2,
                (person[11][1] + person[12][1]) / 2,
                (person[11][2] + person[12][2]) / 2
            ]
        else:
            pelvis = [0, 0, 0]

        # 添加两个中点到关键点列表（作为索引 17、18）
        keypts.append(neck)    # index 17
        keypts.append(pelvis)  # index 18

        # 绘制所有关键点
        for x, y, conf in keypts:
            if conf > confidence_threshold:
                cv2.circle(image, (int(x), int(y)), 4, (0, 255, 0), -1)

        # 绘制骨架线
        for i, j in skeleton:
            if keypts[i][2] > confidence_threshold and keypts[j][2] > confidence_threshold:
                x1, y1 = int(keypts[i][0]), int(keypts[i][1])
                x2, y2 = int(keypts[j][0]), int(keypts[j][1])
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 2)


def pose_estimation(image_path, model_path='yolov8n-pose.pt', output_dir='output_pose', conf=0.3):
    """
    使用 YOLOv8-Pose 模型检测人体姿态并绘制火柴人骨架。

    Args:
        image_path (str): 输入图片路径。
        model_path (str): 姿态估计模型路径。
        output_dir (str): 输出目录。
        conf (float): 置信度阈值。
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片路径不存在 -> {image_path}")

    model = YOLO(model_path)
    print(f"成功加载模型: {model_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"无法读取图片 -> {image_path}")

    results = model(image, conf=conf)

    # 提取包含置信度的关键点 (x, y, confidence)
    keypoints = results[0].keypoints.data.cpu().numpy()

    draw_pose_connections(image, keypoints)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"pose_detected_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, image)
    print(f"检测结果已保存到: {output_path}")
