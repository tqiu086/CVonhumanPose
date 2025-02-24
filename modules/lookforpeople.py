from ultralytics import YOLO
import cv2
import os

def draw_boxes_without_labels(image, results, box_color=(255, 0, 0), thickness=2):
    """
    自定义绘制边框，不显示类别和得分。

    Args:
        image (np.array): 原始图像。
        results: YOLO 检测结果。
        box_color (tuple): 边框颜色 (B, G, R)。
        thickness (int): 边框线条粗细。
    Returns:
        image (np.array): 绘制边框后的图像。
    """
    for result in results:
        for box in result.boxes:
            xyxy = box.xyxy[0].cpu().numpy().astype(int)  # 获取边界框坐标
            x1, y1, x2, y2 = xyxy
            cv2.rectangle(image, (x1, y1), (x2, y2), box_color, thickness)
    return image

def detect_people_from_camera(model_path='yolov8l.pt', camera_index=0, width=1920, height=1080, imgsz=1080, conf=0.25):
    """
    从摄像头实时检测人物并框出检测结果。

    Args:
        model_path (str): YOLO 模型文件路径
        camera_index (int): 摄像头索引
        width (int): 摄像头分辨率宽度
        height (int): 摄像头分辨率高度
        imgsz (int): YOLO 输入图片大小
        conf (float): 置信度阈值
    """
    model = YOLO(model_path)
    print(f"成功加载模型: {model_path}")

    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    if not cap.isOpened():
        print("错误: 无法访问摄像头。")
        return

    print(f"正在从摄像头索引 {camera_index} 捕捉视频... 按 'q' 退出。")

    # 实时检测循环
    while True:
        ret, frame = cap.read()
        if not ret:
            print("错误: 无法读取摄像头帧。")
            break

        # YOLO 检测 (classes=[0] 只检测 person 类别)
        results = model(frame, imgsz=imgsz, conf=conf, classes=[0])

        annotated_frame = results[0].plot()

        cv2.imshow('YOLO 实时人物检测 (1080p)', annotated_frame)

        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("👋 检测已停止。")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("摄像头已释放，窗口已关闭。")


def detect_people_in_image(image_path, model_path='yolov8l.pt', output_dir='output', conf=0.25):
    """
    检测图片中的人物(person 类别）并在输出时保持原始输入图片的尺寸。

    Args:
        image_path (str): 输入图片路径。
        model_path (str): YOLO 模型路径，默认 'yolov8l.pt'。
        output_dir (str): 检测结果保存目录。
        conf (float): 检测置信度阈值，默认 0.25。
    """
    # 检查图片路径
    if not os.path.exists(image_path):
        raise FileNotFoundError(f" 图片路径不存在 -> {image_path}")

    # 加载 YOLO 模型
    model = YOLO(model_path)
    print(f"成功加载模型: {model_path}")

    # 读取原始图片
    original_image = cv2.imread(image_path)
    if original_image is None:
        raise ValueError(f"无法读取图片 -> {image_path}")

    original_height, original_width = original_image.shape[:2]

    # YOLO 检测（classes=[0] 表示只检测 "person" 类别）
    results = model(original_image, imgsz=original_height, conf=conf, classes=[0])

    annotated_image = draw_boxes_without_labels(original_image, results, box_color=(0, 255, 0), thickness=2)


    cv2.imshow('检测结果', annotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"detected_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, annotated_image)
    print(f"检测结果已保存到: {output_path}")

def main():
    """主函数，用于调用检测方法。"""
    # detect_people_from_camera(
    #     model_path='yolov8l.pt', 
    #     camera_index=0,
    #     width=1920,
    #     height=1080,
    #     imgsz=1080,
    #     conf=0.25
    # )

    image_path = 'd:/YOLO/input/people4.jpg' 
    detect_people_in_image(
        image_path=image_path,
        model_path='yolov8l.pt',           
        output_dir='d:/YOLO/output',       
        conf=0.25                          
    )
    # 测试git
if __name__ == "__main__":
    main()
