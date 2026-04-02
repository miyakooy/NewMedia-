import sys
import os
from pathlib import Path

# 确保能找到项目根目录中的 config 和 src 模块 (当前位于 src/test/ 测试文件夹)
root_dir = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0, root_dir)

from src.utils.tensorslab_api import generate_image

def main():
    print("================================")
    print("🚀 开始测试图片生成功能 (SeeDreamV5 Lite)")
    print("================================")
    
    from datetime import datetime
    prompt = "一只可爱的卡通小猫正在玩毛线球，明亮的色彩，3D渲染风格"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    output_path = os.path.join(output_dir, f"test_cat_{timestamp}.jpg")
    
    print(f"🌟 提示词: {prompt}")
    print(f"📁 预期输出路径: {output_path}")
    print("--------------------------------\n")
    
    try:
        # 调用图片生成
        result = generate_image(
            prompt=prompt,
            aspect_ratio="1:1",
            output_path=output_path
        )
        
        print("\n✅ 测试完成：响应成功！")
        print(f"🎉 返回结果 (本地路径): {result}")
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(f"✔️ 确认图片文件已保存到本地: {output_path} ({file_size:.2f} KB)")
        else:
            print("⚠️ 警告：虽然接口没有报错，但是本地没找到文件，这可能是接口同步返回了下载失败，或者是 url 解析错误。")
            
    except Exception as e:
        print(f"\n❌ 测试失败！")
        print(f"🔴 错误信息: {e}")

if __name__ == "__main__":
    main()
