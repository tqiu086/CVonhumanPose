import cv2
from ultralytics import YOLO

def draw_simplified_pose(image, keypoints, confidence_threshold=0.3):
    """
    在视频帧中绘制简化版人体骨架，只关注头、肩、手臂、躯干和腿部。

    Args:
        image (np.array): 摄像头输入图像。
        keypoints (list): 关键点列表 [x, y, confidence]。
        confidence_threshold (float): 关键点可视化置信度阈值。
    """
    skeleton = [
        (5, 7), (7, 9),      # 左臂
        (6, 8), (8, 10),     # 右臂
        (11, 13), (13, 15),  # 左腿
        (12, 14), (14, 16),  # 右腿
        (5, 6),              # 肩连线
        (11, 12),            # 髋连线
        (5, 11), (6, 12),    # 肩到髋，构建躯干
        (0, 5), (0, 6)       # 鼻子到肩（头部连线）
    ]

    for person in keypoints:
        # 绘制关键点
        for i, keypoint in enumerate(person):
            x, y, conf = keypoint
            if conf > confidence_threshold:
                cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)

        # 连接骨架
        for start_idx, end_idx in skeleton:
            if (person[start_idx][2] > confidence_threshold and person[end_idx][2] > confidence_threshold):
                x1, y1 = int(person[start_idx][0]), int(person[start_idx][1])
                x2, y2 = int(person[end_idx][0]), int(person[end_idx][1])
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)


def draw_custom_pose(image, keypoints, confidence_threshold=0.3):
    """
    绘制符合自定义结构的骨架图，添加“脖子中点”连接。

    Args:
        image (np.array): 原图像。
        keypoints (list): 关键点坐标 [17, 3]。
        confidence_threshold (float): 可视化阈值。
    """
    custom_skeleton = [
        (1, 2),                 # 眼睛
        (5, 6),                 # 肩膀
        (11, 12),               # 髋部
        (5, 7), (7, 9),         # 左臂
        (6, 8), (8, 10),        # 右臂
        (11, 13), (13, 15),     # 左腿
        (12, 14), (14, 16)      # 右腿
    ]

    for person in keypoints:
        # 构造 neck 中点
        if person[5][2] > confidence_threshold and person[6][2] > confidence_threshold:
            neck_x = (person[5][0] + person[6][0]) / 2
            neck_y = (person[5][1] + person[6][1]) / 2
            neck_conf = (person[5][2] + person[6][2]) / 2
            neck = [neck_x, neck_y, neck_conf]
        else:
            neck = None

        # 绘制关键点
        for i, kp in enumerate(person):
            x, y, conf = kp
            if conf > confidence_threshold:
                cv2.circle(image, (int(x), int(y)), 4, (0, 255, 0), -1)

        # 绘制自定义骨架
        for start_idx, end_idx in custom_skeleton:
            if person[start_idx][2] > confidence_threshold and person[end_idx][2] > confidence_threshold:
                x1, y1 = int(person[start_idx][0]), int(person[start_idx][1])
                x2, y2 = int(person[end_idx][0]), int(person[end_idx][1])
                cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # 绘制额外的 neck 骨架
        if neck is not None:
            for idx in [5, 6, 11, 12]:
                if person[idx][2] > confidence_threshold:
                    x1, y1 = int(neck[0]), int(neck[1])
                    x2, y2 = int(person[idx][0]), int(person[idx][1])
                    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.circle(image, (int(neck[0]), int(neck[1])), 4, (0, 128, 255), -1)  # neck 点


def real_time_pose_estimation(camera_index=0, model_path='yolov8n-pose.pt', confidence_threshold=0.3):
    """
    实时摄像头人体姿态检测。

    Args:
        camera_index (int): 摄像头索引（默认 0）。
        model_path (str): YOLOv8-Pose 模型路径。
        confidence_threshold (float): 关键点置信度阈值。
    """
    print(f"🎥 正在打开摄像头索引 {camera_index}...")

    # 加载 YOLOv8-Pose 模型
    model = YOLO(model_path)
    print(f"✅ 成功加载模型: {model_path}")

    # 打开摄像头
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # 设置分辨率
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("❌ 错误: 无法打开摄像头！")
        return

    print("🚀 按 'q' 退出...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 错误: 读取摄像头帧失败！")
            break

        # 检测人体姿态
        results = model(frame, conf=confidence_threshold)
        keypoints = results[0].keypoints.data.cpu().numpy()  # 提取关键点

        # 绘制火柴人骨架
        draw_custom_pose(frame, keypoints)

        # 显示结果
        cv2.imshow("实时姿态检测", frame)

        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()
    print("✅ 退出程序，摄像头已释放。")


if __name__ == "__main__":
    real_time_pose_estimation()
