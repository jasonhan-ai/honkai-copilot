from typing import Optional, Union, List, Tuple
import torch
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import os
import base64
from io import BytesIO

class VLMController:
    """视觉语言模型控制器"""
    
    def __init__(self, device: str = None):
        """
        初始化视觉语言模型控制器
        
        Args:
            device: 运行设备，可选 "cuda", "mps", "cpu"，默认自动选择
        """
        self.device = self._get_device() if device is None else device
        self.model = None
        self.processor = None
        
        # 模型配置
        self.model_name = "microsoft/trocr-base-handwritten"
        
        # 确保模型缓存目录存在
        self.cache_dir = os.path.join(os.path.expanduser("~"), ".cache/huggingface/hub")
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_device(self) -> str:
        """自动选择可用的设备"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        return "cpu"
    
    def _convert_image_to_base64(self, image):
        """Convert PIL image to base64 string with size optimization."""
        # Resize image if it's too large (max dimension 192)
        max_size = 192
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to grayscale to reduce size
        image = image.convert('L')
        
        # Compress image with very low quality
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=20, optimize=True)
        buffer.seek(0)
        
        # Convert to base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return image_base64
    
    def _load_model(self):
        """懒加载模型"""
        if self.model is None:
            print(f"正在加载模型 {self.model_name}...")
            
            # 加载处理器
            self.processor = TrOCRProcessor.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            )
            
            # 加载模型
            self.model = VisionEncoderDecoderModel.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            ).to(self.device)
            
            print("模型加载完成！")
    
    def _split_image(self, image: Image.Image, num_blocks: int = 3) -> List[Tuple[Image.Image, Tuple[int, int]]]:
        """
        将图像分割成多个小块
        
        Args:
            image: 输入图像
            num_blocks: 分割成几块（每边），总块数为num_blocks^2
            
        Returns:
            List of tuples (image_block, (x, y)) where x, y are block coordinates
        """
        width, height = image.size
        block_width = width // num_blocks
        block_height = height // num_blocks
        blocks = []
        
        for y in range(num_blocks):
            for x in range(num_blocks):
                left = x * block_width
                top = y * block_height
                right = left + block_width
                bottom = top + block_height
                
                # 处理最后一行/列可能的边界问题
                if x == num_blocks - 1:
                    right = width
                if y == num_blocks - 1:
                    bottom = height
                
                block = image.crop((left, top, right, bottom))
                blocks.append((block, (x, y)))
        
        return blocks
    
    def analyze_image(
        self,
        image: Union[Image.Image, str],
        prompt: str = None,  # 不再使用prompt参数
        max_length: int = 128,
        num_blocks: int = 3,
    ) -> str:
        """
        分析图像并识别文本
        
        Args:
            image: PIL Image对象或图像文件路径
            prompt: 不再使用，保留参数以保持兼容性
            max_length: 最大生成长度
            num_blocks: 将图像分成几块（每边），总块数为num_blocks^2
            
        Returns:
            识别出的文本
        """
        self._load_model()
        
        # 如果输入是路径，加载图像
        if isinstance(image, str):
            image = Image.open(image)
        
        # 分割图像
        blocks = self._split_image(image, num_blocks)
        all_texts = []
        
        # 分析每个块
        for i, (block, (x, y)) in enumerate(blocks):
            print(f"\n分析第 {i+1}/{len(blocks)} 块图像 (位置: {x}, {y})...")
            
            # 转换为RGB模式（如果需要）
            if block.mode != 'RGB':
                block = block.convert('RGB')
            
            # 处理图像
            pixel_values = self.processor(block, return_tensors="pt").pixel_values.to(self.device)
            
            # 生成文本
            generated_ids = self.model.generate(
                pixel_values,
                max_length=max_length
            )
            
            # 解码文本
            generated_text = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=True
            )[0]
            
            if generated_text.strip():  # 只添加非空文本
                all_texts.append(f"区域 ({x+1}, {y+1}): {generated_text}")
        
        # 合并所有文本
        combined_text = "\n\n".join(all_texts)
        
        return combined_text if combined_text else "未检测到任何文本"
    
    def batch_analyze_images(
        self,
        images: List[Union[Image.Image, str]],
        prompts: List[str],
        **kwargs
    ) -> List[str]:
        """
        批量分析多张图像
        
        Args:
            images: 图像列表，每个元素可以是PIL Image对象或图像文件路径
            prompts: 对应的提示词列表
            **kwargs: 传递给analyze_image的其他参数
            
        Returns:
            回答列表
        """
        assert len(images) == len(prompts), "图像数量必须与提示词数量相同"
        return [
            self.analyze_image(image, prompt, **kwargs)
            for image, prompt in zip(images, prompts)
        ] 