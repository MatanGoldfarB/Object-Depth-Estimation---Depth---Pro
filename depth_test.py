from PIL import Image
import depth_pro
import cv2
import numpy as np
import torch
from ultralytics import YOLO

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

yolo_model = YOLO('yolo11s.pt')
image_path = 'data/testX1.jpg'
yolo_input = cv2.imread(image_path)
print("Shape (H, W, C):", yolo_input.shape)

results = yolo_model(yolo_input)

person_boxes = []
for result in results:
    boxes = result.boxes.xyxy.cpu().numpy()
    classes = result.boxes.cls.cpu().numpy()

    for box, cls in zip(boxes, classes):
        x1, y1, x2, y2 = map(int, box[:4])
        person_boxes.append((x1, y1, x2, y2))
        cv2.rectangle(yolo_input, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow('Person Detection', yolo_input)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Loading model")
# Load depth model and preprocessing transform
depth_model, transform = depth_pro.create_model_and_transforms()
depth_model.eval()

image, _, f_px = depth_pro.load_rgb(image_path)
depth_input = transform(image)

print("Calculating Depth")
prediction = depth_model.infer(depth_input, f_px=f_px) # type: ignore
depth = prediction["depth"] # in meters

print("Post model calculations")
depth_np = depth.squeeze().cpu().numpy()

for x1, y1, x2, y2 in person_boxes:
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    depth_value = depth_np[center_y, center_x]

    text = f'Depth: {depth_value:.2f}m'
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2
    font_thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

    text_x = x1
    text_y = y1 + 30
    rect_x1 = text_x - 5
    rect_y1 = text_y - text_size[1] - 10
    rect_x2 = text_x + text_size[0] + 5
    rect_y2 = text_y + 5

    cv2.rectangle(yolo_input, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 0, 0), -1)
    cv2.putText(yolo_input, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)


cv2.imshow('Object Detection with Depth', yolo_input)
cv2.waitKey(0)
cv2.destroyAllWindows()