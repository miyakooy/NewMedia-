import sys
import os
from pathlib import Path

# 确保能找到项目根目录中的 config 和 src 模块 (当前位于 src/test/ 测试文件夹)
root_dir = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0, root_dir)

from src.utils.tensorslab_api import generate_video

def main():
    print("================================")
    print("🚀 开始测试视频生成功能 (SeedanceV1.5 Pro)")
    print("================================")
    
    prompt = "图片中的人物抱着一只猫，在海边散步，可爱的3D渲染风格"
    image_url = "https://tslvideo.s3.us-west-2.amazonaws.com/images/input/2026/03/31/f6a4d239_5924a5_source1.jpg"
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    output_path = os.path.join(output_dir, f"test_video_{timestamp}.mp4")
    
    print(f"🌟 提示词: {prompt}")
    print(f"🖼️ 垫图URL: {image_url}")
    print(f"📁 预期输出路径: {output_path}")
    print("--------------------------------\n")
    
    try:
        # 调用视频生成
        result = generate_video(
            prompt=prompt,
            image_url=image_url,
            duration=5,
            aspect_ratio="9:16",
            output_path=output_path
        )
        
        print("\n✅ 测试完成：响应成功！")
        print(f"🎉 返回结果 (本地路径/URL): {result}")
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✔️ 确认视频文件已保存到本地: {output_path} ({file_size:.2f} MB)")
        else:
            print("⚠️ 警告：虽然接口没有报错，但是本地没找到文件。")
            
    except Exception as e:
        print(f"\n❌ 测试失败！")
        print(f"🔴 错误信息: {e}")

if __name__ == "__main__":
    main()
