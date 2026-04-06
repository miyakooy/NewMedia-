import click
import os
import sys
import json

# 加载配置
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import config
except ImportError:
    click.echo(click.style("⚠️  配置文件不存在，请先复制 config.example.py 为 config.py 并填写配置", fg="yellow"))
    sys.exit(1)

from src.xhs import xhs_cli
from src.blog import blog_cli
from src.ppt import ppt_cli
from src.video import video_cli
from src.seo import KeywordResearch, ContentAuditor, GeoOptimizer, HotspotCrawler

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """TensorsLab NewMedia Kit - 一站式AI新媒体内容生产工具包"""
    pass

# 注册子命令
cli.add_command(xhs_cli, name="xhs")
cli.add_command(blog_cli, name="blog")
cli.add_command(ppt_cli, name="ppt")
cli.add_command(video_cli, name="video")

# SEO相关命令
@cli.group(name="seo")
def seo_cli():
    """SEO+GEO优化相关工具"""
    pass

@seo_cli.command(name="hotspot")
@click.option("--count", "-c", default=5, help="返回热点数量")
@click.option("--days", "-d", default=7, help="最近几天的热点")
def hotspot(count, days):
    """抓取近期热门话题"""
    crawler = HotspotCrawler()
    hotspots = crawler.get_latest_hotspots(count=count, days=days)
    click.echo(click.style(f"🔥 最近{days}天热门话题TOP{count}:", fg="red", bold=True))
    for i, hs in enumerate(hotspots, 1):
        click.echo(f"\n{i}. {hs['title']}")
        click.echo(f"   热度: {hs['hot_value']:,} | 平台: {hs['platform']} | 发布时间: {hs['publish_time']}")
        click.echo(f"   摘要: {hs['summary']}")

@seo_cli.command(name="keyword")
@click.option("--niche", "-n", default="AI营销", help="细分领域")
@click.option("--count", "-c", default=5, help="返回关键词数量")
def keyword(niche, count):
    """挖掘高价值低竞争关键词"""
    kr = KeywordResearch(niche=niche)
    keywords = kr.get_high_value_keywords(count=count)
    click.echo(click.style(f"🔑 {niche}领域高价值关键词TOP{count}:", fg="blue", bold=True))
    for i, kw in enumerate(keywords, 1):
        click.echo(f"\n{i}. {kw.keyword}")
        click.echo(f"   搜索量: {kw.search_volume:,}/月 | 竞争难度: {kw.difficulty:.1f} | 意图: {kw.intent}")
        click.echo(f"   相关关键词: {', '.join(kw.related_keywords)}")

@seo_cli.command(name="audit")
@click.argument("content_path", type=click.Path(exists=True))
@click.option("--keyword", "-k", help="目标关键词")
def audit(content_path, keyword):
    """审核内容质量（CORE-EEAT标准）"""
    with open(content_path, "r", encoding="utf-8") as f:
        content = f.read()
    title = os.path.basename(content_path).replace(".md", "")
    
    auditor = ContentAuditor()
    result = auditor.audit(content, title, keyword)
    
    click.echo(click.style(f"📋 内容质量审核结果:", fg="green", bold=True))
    click.echo(f"总分: {result.overall_score}/100 | {'✅ 通过' if result.passed else '❌ 未通过'}")
    click.echo(f"各维度得分: C(内容质量):{result.dimension_scores['C']} O(原创性):{result.dimension_scores['O']} R(相关性):{result.dimension_scores['R']} E(专业性):{result.dimension_scores['E']}")
    
    if result.veto_triggers:
        click.echo(click.style("\n❌ 否决项（必须修改）:", fg="red"))
        for v in result.veto_triggers:
            click.echo(f"   - {v}")
    
    if result.optimization_suggestions:
        click.echo(click.style("\n💡 优化建议:", fg="yellow"))
        for s in result.optimization_suggestions:
            click.echo(f"   - {s}")

@seo_cli.command(name="geo")
@click.argument("content_path", type=click.Path(exists=True))
@click.option("--keyword", "-k", help="目标关键词")
@click.option("--output", "-o", help="优化后内容输出路径")
def geo(content_path, keyword, output):
    """GEO优化（提升大模型引用率）"""
    with open(content_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    optimizer = GeoOptimizer()
    optimized = optimizer.optimize(content, keyword)
    suggestions = optimizer.get_optimization_suggestions(content)
    
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(optimized)
        click.echo(click.style(f"✅ 优化后内容已保存到: {output}", fg="green"))
    else:
        click.echo(click.style("✅ 优化后内容:", fg="green"))
        click.echo(optimized)
    
    if suggestions:
        click.echo(click.style("\n💡 进一步优化建议:", fg="yellow"))
        for s in suggestions:
            click.echo(f"   - {s}")

# 飞书相关命令
@cli.group(name="feishu")
def feishu_cli():
    """飞书多维表格相关工具"""
    pass

@feishu_cli.command(name="update-meta")
@click.option("--name", "-n", default=None, help="新的多维表格名称（不超过100字符）")
@click.option("--advanced/--no-advanced", default=None, help="开启/关闭高级权限")
@click.option("--app-token", default=None, help="多维表格 app_token（不传则从配置中解析）")
def update_meta(name, advanced, app_token):
    """更新多维表格元数据（名称、高级权限）"""
    if name is None and advanced is None:
        click.echo(click.style("⚠️  请至少指定 --name 或 --advanced/--no-advanced", fg="yellow"))
        return

    from src.utils.feishu_archive import update_bitable_meta, FeishuArchiveError

    try:
        app_info = update_bitable_meta(
            name=name,
            is_advanced=advanced,
            app_token=app_token,
        )
        click.echo(click.style(f"📋 返回信息: {json.dumps(app_info, ensure_ascii=False, indent=2)}", fg="cyan"))
    except FeishuArchiveError as exc:
        click.echo(click.style(f"❌ 更新失败: {exc}", fg="red"))


if __name__ == "__main__":
    cli()
