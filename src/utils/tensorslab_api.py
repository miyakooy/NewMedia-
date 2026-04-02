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
        endpoint = f"{self.base_url}/images/seedreamv5"
        
        payload = {
            "category": "seedreamv5",
            "prompt": prompt,
            "batchsize": "1",
            "resolution": aspect_ratio
        }
        
        req_headers = self.headers.copy()
        req_headers.pop("Content-Type", None)
        
        files = {k: (None, str(v)) for k, v in payload.items()}
        
        response = requests.post(endpoint, files=files, headers=req_headers)
        response.raise_for_status()
        
        res_data = response.json()
        if res_data.get("code") != 1000:
            raise Exception(f"图片生成失败: {res_data.get('msg', '未知错误')}")
            
        data = res_data.get("data", {})
        image_url = data.get("url")
        task_id = data.get("taskid")
        
        if not image_url and task_id:
            # 轮询任务状态
            poll_endpoint = f"{self.base_url}/images/infobytaskid"
            with tqdm(desc="生成图片中", unit="s") as pbar:
                while True:
                    status_payload = {"taskid": task_id}
                    # 轮询接口要求application/json格式，这与self.headers的默认设置一致
                    status_response = requests.post(poll_endpoint, json=status_payload, headers=self.headers)
                    status_response.raise_for_status()
                    status_res = status_response.json()
                    
                    if status_res.get("code") != 1000:
                        raise Exception(f"查询任务状态失败: {status_res.get('msg', '未知错误')}")
                        
                    status_data = status_res.get("data", {})
                    image_status = status_data.get("image_status")
                    
                    if str(image_status) == "3":
                        urls = status_data.get("url", [])
                        if isinstance(urls, list) and len(urls) > 0:
                            image_url = urls[0]
                        else:
                            image_url = urls
                        break
                    elif str(image_status) == "4":
                        raise Exception(f"图片生成失败: {status_res.get('msg', '未知错误')}")
                    
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
        endpoint = f"{self.base_url}/video/seedancev15pro"
        payload = {
            "prompt": prompt,
            "duration": duration,
            "ratio": aspect_ratio,
            "resolution": "720p"
        }
        
        if image_url:
            payload["imageUrl"] = image_url
            
        req_headers = self.headers.copy()
        req_headers.pop("Content-Type", None)
        
        files = {k: (None, str(v)) for k, v in payload.items()}
        
        response = requests.post(endpoint, files=files, headers=req_headers)
        response.raise_for_status()
        
        res_data = response.json()
        if str(res_data.get("code")) not in ("1000", "123"):
            raise Exception(f"视频生成请求失败: {res_data.get('msg', '未知错误')}")
            
        data = res_data.get("data", {})
        task_id = data.get("taskid")
        video_url = data.get("url")
        
        if not video_url and task_id:
            # 轮询任务状态
            poll_endpoint = f"{self.base_url}/video/infobytaskid"
            with tqdm(desc="生成视频中", unit="s") as pbar:
                while True:
                    status_payload = {"taskid": task_id}
                    status_response = requests.post(poll_endpoint, json=status_payload, headers=self.headers)
                    status_response.raise_for_status()
                    status_res = status_response.json()
                    
                    if str(status_res.get("code")) not in ("1000", "123"):
                        raise Exception(f"查询任务状态失败: {status_res.get('msg', '未知错误')}")
                        
                    status_data = status_res.get("data", {})
                    task_status = status_data.get("task_status")
                    
                    if str(task_status) == "3":
                        urls = status_data.get("url", [])
                        if isinstance(urls, list) and len(urls) > 0:
                            video_url = urls[0]
                        else:
                            video_url = urls
                        break
                    elif str(task_status) == "4":
                        raise Exception(f"视频生成失败: {status_res.get('msg', '未知错误')}")
                    
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
