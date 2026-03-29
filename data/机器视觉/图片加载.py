from PIL import Image
import numpy as np
import cv2
import os

image_path = r'C:\Users\QQQQQ\Desktop\问题代码.png'

# ---------- 裁剪与压缩参数（可按需修改）----------
# 裁剪方式二选一：
# 1) 固定区域：CROP_BOX = (left, upper, right, lower)，例如 (100, 50, 500, 400)
# 2) 交互式：USE_INTERACTIVE_CROP = True，运行后用鼠标框选区域按 Enter 确认
CROP_BOX = []  # 不裁剪保持 []；固定裁剪填 (left, upper, right, lower)
USE_INTERACTIVE_CROP = False  # True=先显示图，框选区域后裁剪

# 是否保存压缩后的图片
SAVE_COMPRESSED = True
COMPRESS_QUALITY = 85  # JPEG 质量 1-95，越小文件越小

try:
    # 使用 Pillow 打开图片
    pil_image = Image.open(image_path).convert('RGB')
    print("Pillow 成功打开了图片！")

    # ---------- 裁剪（固定区域 或 交互式框选）----------
    if CROP_BOX:
        left, upper, right, lower = CROP_BOX
        pil_image = pil_image.crop((left, upper, right, lower))
        print(f"已裁剪为区域: ({left}, {upper}, {right}, {lower})")
    elif USE_INTERACTIVE_CROP:
        opencv_tmp = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        roi = cv2.selectROI("框选裁剪区域 (选好后按 Enter)", opencv_tmp, fromCenter=False)
        cv2.destroyWindow("框选裁剪区域 (选好后按 Enter)")
        x, y, w, h = (int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3]))
        if w > 0 and h > 0:
            pil_image = pil_image.crop((x, y, x + w, y + h))
            print(f"已按框选裁剪: ({x}, {y}, {x + w}, {y + h})")

    # ---------- 压缩并保存（可选）----------
    if SAVE_COMPRESSED:
        base, ext = os.path.splitext(image_path)
        out_path = f"{base}_cropped_compressed.jpg"
        pil_image.save(out_path, 'JPEG', quality=COMPRESS_QUALITY, optimize=True)
        print(f"已压缩保存到: {out_path} (质量={COMPRESS_QUALITY})")

    # 将图片转换为 OpenCV 格式 (BGR)
    opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # 显示图片
    cv2.imshow('pil_image', opencv_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except Exception as e:
    print(f"Pillow 打开图片时出错: {e}")
