from typing import Optional, Union, List, Tuple
import torch
from PIL import Image
from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration
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
        self.model_name = "Salesforce/instructblip-flan-t5-xl"
        
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
            self.processor = InstructBlipProcessor.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            )
            
            # 加载模型
            self.model = InstructBlipForConditionalGeneration.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir,
                torch_dtype=torch.float16,
                device_map="auto" if self.device == "cuda" else None,
            ).to(self.device)
            
            print("模型加载完成！")
    
    def _split_image(self, image: Image.Image, num_blocks: int = 2) -> List[Tuple[Image.Image, Tuple[int, int]]]:
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
        image,
        prompt="请详细分析这个界面截图。描述：1. 界面的主要内容和标题 2. 所有可见的文本信息 3. 界面布局和设计特点 4. 按钮、图标等交互元素。请用中文回答，尽可能详细。",
        max_length=512,
        num_beams=5,
        temperature=0.7,
    ):
        """分析图像内容。
        
        Args:
            image: PIL.Image对象
            prompt: 分析提示词
            max_length: 生成文本的最大长度
            num_beams: beam search的beam数量
            temperature: 生成文本的随机性，越大越随机
            
        Returns:
            str: 分析结果
        """
        self._load_model()
        
        # 如果输入是路径，加载图像
        if isinstance(image, str):
            image = Image.open(image)
        
        # 处理图像
        inputs = self.processor(
            images=image,
            text=prompt,
            return_tensors="pt"
        ).to(self.device)
        
        # 生成回答
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            num_beams=num_beams,
            temperature=temperature,
            do_sample=temperature > 0,
        )
        
        # 解码回答
        response = self.processor.batch_decode(
            outputs,
            skip_special_tokens=True
        )[0].strip()
        
        return response
    
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