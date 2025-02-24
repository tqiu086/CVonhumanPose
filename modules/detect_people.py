# modules/detect_people.py
from ultralytics import YOLO
import cv2
import os


def detect_people_in_image(image_path, model_path='yolov8l.pt', output_dir='output', conf=0.25):
    """
    检测图片中的人物并在输出时保持原始输入图片的尺寸。

    Args:
        image_path (str): 输入图片路径。
        model_path (str): YOLO 模型路径，默认 'yolov8l.pt'。
        output_dir (str): 检测结果保存目录。
        conf (float): 检测置信度阈值。
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ 图片路径不存在 -> {image_path}")

    model = YOLO(model_path)
    print(f"✅ 成功加载模型: {model_path}")

    original_image = cv2.imread(image_path)
    if original_image is None:
        raise ValueError(f"❌ 无法读取图片 -> {image_path}")

    results = model(original_image, conf=conf, classes=[0])
    annotated_image = results[0].plot()

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"detected_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, annotated_image)
    print(f"💾 检测结果已保存到: {output_path}")
