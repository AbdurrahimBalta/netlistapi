import torch
from PIL import Image
import io

def get_yolov5():
    # local best.pt
    model = torch.hub.load('ultralytics/yolov5', 'custom',
                      path='model/best_V2.pt', force_reload=True) 
  # local repo
    model.conf = 0.6
    return model


# def get_image_from_bytes(binary_image, max_size=1024):
#     input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
#     width, height = input_image.size
#     resize_factor = min(max_size / width, max_size / height)
#     resized_image = input_image.resize(
#         (
#             int(input_image.width * resize_factor),
#             int(input_image.height * resize_factor),
#         )
#     )
#     return resized_image

import cv2
import numpy as np

def get_image_from_bytes(binary_image, max_size=512):
    nparr = np.frombuffer(binary_image, np.uint8)
    input_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    height, width = input_image.shape[:2]
    resize_factor = min(max_size / width, max_size / height)
    resized_image = cv2.resize(input_image, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_AREA)
    return resized_image

