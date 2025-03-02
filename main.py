# main.py
from modules.detect_people import detect_people_in_image
from modules.pose_estimation import pose_estimation


def main():
    # human detection starts
    print("Starting detection of the figure...")
    imagepath = 'd:/YOLO/pose/618faee0bc1a59a1fac612afb63f843.jpg'

    detect_people_in_image(
        image_path=imagepath,
        model_path='yolov8l.pt',
        output_dir='d:/YOLO/people_output',
        conf=0.25
    )

    # testing for pose estimation
    print("Starting pose estimate...")
    pose_estimation(
        image_path=imagepath,
        model_path='yolov8n-pose.pt',
        output_dir='d:/YOLO/pose_output',
        conf=0.3
    )


if __name__ == "__main__":
    main()
