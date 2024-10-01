import face_recognition
import cv2
import os
import numpy as np
import gradio as gr
from PIL import Image, ImageDraw, ImageFont


# 定義高斯模糊函數
def apply_gaussian_blur(image):
    # image = cv2.convertScaleAbs(image, alpha=1.5, beta=50)
    
    # 应用高斯模糊降噪
    image = cv2.GaussianBlur(image, (3, 3), 0)
    
    # 转换到 YCrCb 色彩空间并应用直方图均衡化
    # ycrcb_img = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    # channels = cv2.split(ycrcb_img)
    # cv2.equalizeHist(channels[0], channels[0])
    # cv2.merge(channels, ycrcb_img)
    # image = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2BGR)
    
    # 锐化图像
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv2.filter2D(image, -1, kernel)
    return image

# 加載已知臉部編碼和名字
known_face_encodings = []
known_face_names = []

# 對於每個需要識別的人，加載參考圖片，並創建編碼
for person_image_path, person_name in [("data/統神.jpg", "統神"),("data/統神_01.jpg", "統神"),("data/國棟_02.jpg", "國棟"),("data/國棟_02.jpg", "國棟"),("data/國棟_03.jpg", "國棟"),("data/國棟_05.jpg", "國棟"),("data/胖子2.jpg","胖子"),("data/胖子.jpg","胖子"),("d2/image-3拷貝.jpg","林孟欣"),("d2/image-4.jpg","林孟欣")]:
    person_image = cv2.imread(person_image_path)
    person_image = apply_gaussian_blur(person_image)
    person_image = cv2.cvtColor(person_image, cv2.COLOR_BGR2RGB)  
    face_encoding = face_recognition.face_encodings(person_image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(person_name)

# 定義人臉識別函數
def recognize_face(input_image):
    image = np.array(input_image)
    blurred_image = apply_gaussian_blur(image)
    face_locations = face_recognition.face_locations(blurred_image)
    face_encodings = face_recognition.face_encodings(blurred_image, face_locations)

    # 将 OpenCV 图像转换为 PIL 图像以使用中文
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    # 选择使用的字体和大小，请确保路径正确
    font_path = 'Iansui-Regular.ttf'  # 替换为您的中文字体路径
    font_size = 30
    font = ImageFont.truetype(font_path, font_size)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # 绘制框和文本
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0), width=2)
        draw.text((left + 6, bottom - font_size - 6), name, fill=(10, 10, 10), font=font)

    # 将 PIL 图像转换回 numpy 数组
    return np.array(pil_image)

iface = gr.Interface(
    fn=recognize_face, 
    inputs=gr.components.Image(),
    outputs="image",
    title="preprocessing 臉部偵測",
    description="請上傳一張圖片"
)

iface.launch()