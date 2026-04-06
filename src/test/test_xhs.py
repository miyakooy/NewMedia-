import sys
import os
from pathlib import Path

# 确保能找到项目根目录中的 config 和 src 模块
root_dir = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0, root_dir)

from src.xhs.service import XHSService, XHSGenerationError

def main():
    print("================================")
    print("🚀 开始测试小红书主题生成功能 (XHSService)")
    print("================================")
    
    topic = "测试驱动开发(TDD)的最佳实践"
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "xhs_test")
    
    print(f"🌟 测试主题: {topic}")
    print(f"📁 预期输出目录: {output_dir}")
    print("--------------------------------\n")
    
    try:
        service = XHSService()
        print("⏳ 正在结合 Gemini/OpenAI 生成文案，并调用 TensorsLab 生成图片...")
        print("💡 这通常需要 15 - 30 秒左右，请耐心等待...")
        
        result = service.generate_from_topic(
            topic=topic,
            output_dir=output_dir,
            style="ins",
            auto_archive=True,  # 开启飞书归档测试
        )
        
        print("\n✅ 测试完成：小红书内容生成成功！")
        print(f"🎉 返回结果:")
        print(f"  - 主题: {result.topic}")
        print(f"  - 文案路径: {result.copy_path}")
        print(f"  - 图片路径: {result.image_path}")
        print(f"  - 生成时间: {result.generated_at}")
        
        # 验证文件是否存在
        print("\n📊 文件落盘检测:")
        if os.path.exists(result.copy_path):
            file_size = os.path.getsize(result.copy_path) / 1024
            print(f"✔️ 确认文案已保存: {result.copy_path} ({file_size:.2f} KB)")
        else:
            print("⚠️ 警告：找不到文案文件。")
            
        if os.path.exists(result.image_path):
            file_size = os.path.getsize(result.image_path) / 1024
            print(f"✔️ 确认图片已保存: {result.image_path} ({file_size:.2f} KB)")
        else:
            print("⚠️ 警告：找不到图片文件。")
            
    except XHSGenerationError as e:
        print(f"\n❌ 生成失败 (XHSGenerationError)！")
        print(f"🔴 错误信息: {e}")
    except Exception as e:
        print(f"\n❌ 测试发生未知异常！")
        print(f"🔴 系统错误: {e}")

if __name__ == "__main__":
    main()
