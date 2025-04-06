import easyocr
import numpy as np
import ssl
import os
from typing import List, Tuple, Optional
from PIL import Image

class OCRController:
    def __init__(self, download_enabled: bool = True):
        """
        初始化OCR控制器
        
        Args:
            download_enabled: 是否允许下载模型文件，如果为False则使用本地模型
        """
        self._reader = None
        self._download_enabled = download_enabled
        
        # 设置模型存储路径
        self.model_dir = os.path.join(os.path.expanduser("~"), ".EasyOCR")
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
    
    @property
    def reader(self):
        """懒加载OCR读取器"""
        if self._reader is None:
            if not self._download_enabled:
                # 禁用SSL证书验证（仅用于测试）
                ssl._create_default_https_context = ssl._create_unverified_context
            self._reader = easyocr.Reader(['en', 'ch_sim'], model_storage_directory=self.model_dir)
        return self._reader

    def recognize_image(self, image: Image.Image, region: Optional[Tuple[int, int, int, int]] = None) -> List[Tuple[List[Tuple[int, int]], str, float]]:
        """
        对图像进行OCR识别
        
        Args:
            image: PIL Image对象
            region: 可选的区域参数 (left, top, width, height)，如果不指定则对整个图像进行识别
        
        Returns:
            List of tuples, each containing:
            - List of coordinates [(x1,y1), (x2,y2), (x3,y3), (x4,y4)] for text bounding box
            - Detected text string
            - Confidence score
        """
        if region:
            left, top, width, height = region
            image = image.crop((left, top, left + width, top + height))
        
        # 转换为numpy数组
        img_array = np.array(image)
        
        # 执行OCR
        result = self.reader.readtext(img_array)
        
        # 如果指定了区域，需要调整坐标
        if region:
            left, top = region[:2]
            adjusted_result = []
            for bbox, text, conf in result:
                adjusted_bbox = [
                    (int(x + left), int(y + top)) for x, y in bbox
                ]
                adjusted_result.append((adjusted_bbox, text, conf))
            return adjusted_result
        
        return [([(int(x), int(y)) for x, y in bbox], text, conf) for bbox, text, conf in result] 