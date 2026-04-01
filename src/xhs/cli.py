import click
import os
import json
from datetime import datetime
import config
from src.utils import generate_image, archive_to_bitable, get_hotspots
from openai import OpenAI

client = OpenAI(api_key=config.OPENAI_API_KEY if hasattr(config, 'OPENAI_API_KEY') else None)

@click.group(name="xhs")
def xhs_cli():
    """小红书全自动营销工作流"""
    pass

@xhs_cli.command(name="generate")
@click.option("--topic", required=True, help="生成主题")
@click.option("--count", default=1, type=int, help="生成数量")
@click.option("--style", default=config.DEFAULT_IMAGE_STYLE, help="图片风格")
@click.option("--auto-archive", is_flag=True, default=True, help="是否自动归档到飞书多维表格")
@click.option("--output-dir", default=config.DEFAULT_OUTPUT_DIR + "/xhs", help="输出目录")
def generate(topic, count, style, auto_archive, output_dir):
    """生成小红书文案和配图"""
    os.makedirs(output_dir, exist_ok=True)
    click.echo(click.style(f"开始生成 {count} 篇小红书「{topic}」相关内容...", fg="blue"))
    
    for i in range(count):
        click.echo(click.style(f"\n正在生成第 {i+1}/{count} 篇内容...", fg="cyan"))
        
        # 1. 生成文案
        click.echo("正在生成文案...")
        prompt = f"""
        请生成一篇小红书风格的关于{topic}的文案，要求：
        1. 标题吸引人，自带emoji
        2. 内容活泼有趣，有互动引导，适合年轻用户
        3. 结尾带5-8个相关的话题标签
        4. 总字数在300-500字左右
        5. 符合小红书平台调性，多用语气词
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        copy = response.choices[0].message.content
        
        # 2. 生成配图
        click.echo("正在生成配图...")
        image_prompt = f"可爱风格插画，关于{topic}，小红书风格，1:1比例，明亮色彩，Q版，无文字"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"{output_dir}/{timestamp}_{i+1}.png"
        image_url = generate_image(image_prompt, style=style, aspect_ratio="1:1", output_path=image_path)
        
        # 3. 保存文案
        text_path = f"{output_dir}/{timestamp}_{i+1}.md"
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(copy)
        
        click.echo(click.style(f"✅ 第 {i+1} 篇生成完成：", fg="green"))
        click.echo(f"   文案：{text_path}")
        click.echo(f"   配图：{image_path}")
        
        # 4. 自动归档
        if auto_archive and hasattr(config, 'FEISHU_BITABLE_XHS_TABLE') and config.FEISHU_BITABLE_XHS_TABLE:
            click.echo("正在归档到飞书多维表格...")
            archive_to_bitable(
                table_url=config.FEISHU_BITABLE_XHS_TABLE,
                data={
                    "主题": topic,
                    "文案": copy,
                    "配图": image_url,
                    "生成时间": datetime.now().isoformat(),
                    "标签": ",".join([tag for tag in copy.split("#") if tag.strip()])
                }
            )
            click.echo("✅ 归档完成")
    
    click.echo(click.style(f"\n🎉 全部 {count} 篇内容生成完成！", fg="green", bold=True))

@xhs_cli.command(name="hotspot-generate")
@click.option("--count", default=3, type=int, help="生成数量")
@click.option("--style", default=config.DEFAULT_IMAGE_STYLE, help="图片风格")
def hotspot_generate(count, style):
    """根据实时热点生成小红书内容"""
    click.echo(click.style("正在抓取小红书实时热点...", fg="blue"))
    hotspots = get_hotspots(platform="xhs", limit=count)
    
    for hotspot in hotspots:
        click.echo(click.style(f"\n正在生成热点「{hotspot['title']}」相关内容...", fg="cyan"))
        generate.callback(topic=hotspot['title'], count=1, style=style, auto_archive=True, output_dir=config.DEFAULT_OUTPUT_DIR + "/xhs/hotspots")
