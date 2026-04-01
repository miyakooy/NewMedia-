import requests
import os
import time
from tqdm import tqdm
import config

class TensorsLabAPI:
    def __init__(self):
        self.api_key = config.TENSORSLAB_API_KEY
        self.base_url = config.TENSORSLAB_API_BASE
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_image(self, prompt, style="cute", aspect_ratio="1:1", output_path=None):
        """生成图片"""
        endpoint = f"{self.base_url}/images/generations"
        payload = {
            "prompt": prompt,
            "style": style,
            "aspect_ratio": aspect_ratio,
            "n": 1,
            "quality": "high"
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        task_id = response.json()["task_id"]
        
        # 轮询任务状态
        with tqdm(desc="生成图片中", unit="s") as pbar:
            while True:
                status_response = requests.get(f"{self.base_url}/tasks/{task_id}", headers=self.headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                if status_data["status"] == "completed":
                    image_url = status_data["result"]["images"][0]["url"]
                    break
                elif status_data["status"] == "failed":
                    raise Exception(f"图片生成失败: {status_data.get('error', '未知错误')}")
                
                time.sleep(2)
                pbar.update(2)
        
        # 下载图片
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            image_response = requests.get(image_url)
            with open(output_path, "wb") as f:
                f.write(image_response.content)
            return output_path
        
        return image_url
    
    def generate_video(self, prompt, image_url=None, duration=15, aspect_ratio="9:16", output_path=None):
        """生成视频"""
        endpoint = f"{self.base_url}/videos/generations"
        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "n": 1
        }
        
        if image_url:
            payload["image_url"] = image_url
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        task_id = response.json()["task_id"]
        
        # 轮询任务状态
        with tqdm(desc="生成视频中", unit="s") as pbar:
            while True:
                status_response = requests.get(f"{self.base_url}/tasks/{task_id}", headers=self.headers)
                status_response.raise_for_status()
                status_data = status_response.json()
                
                if status_data["status"] == "completed":
                    video_url = status_data["result"]["videos"][0]["url"]
                    break
                elif status_data["status"] == "failed":
                    raise Exception(f"视频生成失败: {status_data.get('error', '未知错误')}")
                
                time.sleep(5)
                pbar.update(5)
        
        # 下载视频
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            video_response = requests.get(video_url)
            with open(output_path, "wb") as f:
                f.write(video_response.content)
            return output_path
        
        return video_url

# 全局实例
tensorslab_api = TensorsLabAPI()

def generate_image(prompt, **kwargs):
    return tensorslab_api.generate_image(prompt, **kwargs)

def generate_video(prompt, **kwargs):
    return tensorslab_api.generate_video(prompt, **kwargs)
