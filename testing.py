import os
import cv2
import time
from backend import dual_ports_password
from modules.pose_estimation import pose_estimation

def test_pose_estimation(input_dir='pose', output_dir='pose_output', model_path='yolov8n-pose.pt', conf=0.3):
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"输入目录不存在: {input_dir}")
    os.makedirs(output_dir, exist_ok=True)
    input_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not input_files:
        print("输入目录中没有找到图片文件！")
        return False
    print(f"检测到 {len(input_files)} 张图片，开始处理...")
    for file_name in input_files:
        input_path = os.path.join(input_dir, file_name)
        print(f"处理: {file_name} ...")
        pose_estimation(input_path, model_path, output_dir, conf)
    output_files = [f for f in os.listdir(output_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if len(input_files) == len(output_files):
        print(f"测试通过！输入: {len(input_files)} 张, 输出: {len(output_files)} 张。")
        return True
    else:
        print(f"测试失败！输入: {len(input_files)} 张, 但输出: {len(output_files)} 张。")
        return False
def list_available_cameras(max_tested=10):
    available_cameras = []
    
    print("正在检测可用摄像头...")
    for i in range(max_tested):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # 使用 DirectShow 避免摄像头冲突
        if cap.isOpened():
            available_cameras.append(i)
            print(f"摄像头可用: Index {i}")
        cap.release()

    if not available_cameras:
        print("未找到可用摄像头！")
    else:
        print(f"可用摄像头列表: {available_cameras}")

    return available_cameras

if __name__ == "__main__":
    test_pose_estimation()
    list_available_cameras()