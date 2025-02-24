# modules/pose_estimation.py
from ultralytics import YOLO
import cv2
import os


def draw_pose_connections(image, keypoints, confidence_threshold=0.3):
    """
    绘制人体关键点并连接形成火柴人。

    Args:
        image (np.array): 输入图像。
        keypoints (list): 关键点列表 [x, y, confidence]。
        confidence_threshold (float): 关键点可视化置信度阈值。
    """
    # 修正后的 COCO 骨架连接关系 (去除索引 17)
    skeleton = [
    (0, 5), (0, 6),           # 头部与肩膀
    (5, 7), (7, 9),           # 左臂
    (6, 8), (8, 10),          # 右臂
    (5, 11), (6, 12),         # 肩膀到髋部（躯干）
    (11, 13), (13, 15),       # 左腿
    (12, 14), (14, 16),       # 右腿
    (11, 12)                  # 髋部连接
]


    # 绘制关键点和骨架
    for person in keypoints:
        # 绘制关键点
        for i, keypoint in enumerate(person):
            x, y, conf = keypoint
            if conf > confidence_threshold:
                cv2.circle(image, (int(x), int(y)), 4, (0, 255, 0), -1)

        # 绘制骨架连接
        for connection in skeleton:
            start_idx, end_idx = connection
            if (start_idx < len(person) and end_idx < len(person) and
                person[start_idx][2] > confidence_threshold and person[end_idx][2] > confidence_threshold):
                x1, y1 = int(person[start_idx][0]), int(person[start_idx][1])
                x2, y2 = int(person[end_idx][0]), int(person[end_idx][1])
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)


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
    print(f"✅ 成功加载模型: {model_path}")

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
    print(f"💾 检测结果已保存到: {output_path}")
