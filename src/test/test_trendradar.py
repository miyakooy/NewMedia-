import os
import sys
from pathlib import Path


root_dir = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0, root_dir)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from src.trendradar.trendconfig import load_config
from src.trendradar.core import TrendRadarService


def main() -> None:
    print("================================")
    print("开始测试 TrendRadar 本地闭环")
    print("================================")

    config_path = os.path.join(root_dir, "config", "trendradar.example.json")
    print(f"📄 配置文件: {config_path}")

    cfg = load_config(config_path)
    service = TrendRadarService(cfg)

    hotspots = service.get_hotspots()
    brief = service.build_brief(keyword=cfg.keyword)

    print("\n✅ 热点列表测试通过")
    print(f"- 热点数量: {len(hotspots)}")
    for idx, item in enumerate(hotspots[:3], 1):
        print(f"  {idx}. [{item.platform}] {item.title} | {item.hot_value}")

    print("\n✅ 简报测试通过")
    print(f"- 简报命中数量: {brief['count']}")
    print(f"- 简报预览: {brief['brief'][:180].replace(chr(10), ' ')}")

    output_path = service.export_brief(keyword=cfg.keyword)
    print("\n✅ 导出测试通过")
    print(f"- 输出文件: {output_path}")
    print(f"- 文件存在: {os.path.exists(output_path)}")


if __name__ == "__main__":
    main()
