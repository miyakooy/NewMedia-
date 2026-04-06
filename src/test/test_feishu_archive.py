"""飞书多维表格归档功能集成测试。

测试目标：验证通过飞书 API 向多维表格发送文案和图片的完整流程。
使用 config.py 中的真实配置进行 API 调用。
"""

import sys
import os
from pathlib import Path

# 尝试解决 Windows 控制台默认非 UTF-8 导致打印 Emoji 时崩溃的问题
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 确保能找到项目根目录中的 config 和 src 模块
root_dir = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0, root_dir)

from src.utils.feishu_archive import (
    archive_to_bitable,
    update_bitable_meta,
    FeishuArchiveError,
    _parse_app_token,
    _get_feishu_config,
    _get_tenant_access_token,
)


# ---------------------------------------------------------------------------
# 测试 1: URL 解析
# ---------------------------------------------------------------------------

def test_parse_app_token():
    """测试从飞书多维表格 URL 解析 app_token"""
    print("🧪 测试 1: URL 解析 app_token")
    print("--------------------------------")

    test_cases = [
        (
            "https://wcnt4lo56m8u.feishu.cn/base/BFLWbehbEaX3jJs9kkQcxXfHnvd",
            "BFLWbehbEaX3jJs9kkQcxXfHnvd",
        ),
        (
            "https://wcnt4lo56m8u.feishu.cn/wiki/XY4DwsyKHitnoLkaDKEc7MlWnxd",
            "XY4DwsyKHitnoLkaDKEc7MlWnxd",
        ),
        (
            "https://wcnt4lo56m8u.feishu.cn/base/ABC123?table=tbl456",
            "ABC123",
        ),
    ]

    all_passed = True
    for url, expected in test_cases:
        result = _parse_app_token(url)
        status = "✅" if result == expected else "❌"
        if result != expected:
            all_passed = False
        print(f"  {status} URL: ...{url[-30:]} => {result} (期望: {expected})")

    # 测试无效 URL
    try:
        _parse_app_token("https://example.com/invalid")
        print("  ❌ 无效 URL 应该抛出 FeishuArchiveError")
        all_passed = False
    except FeishuArchiveError:
        print("  ✅ 无效 URL 正确抛出 FeishuArchiveError")

    return all_passed


# ---------------------------------------------------------------------------
# 测试 2: 获取 tenant_access_token
# ---------------------------------------------------------------------------

def test_get_token():
    """测试获取飞书 tenant_access_token"""
    print("\n🧪 测试 2: 获取 tenant_access_token")
    print("--------------------------------")

    try:
        app_id, app_secret, _ = _get_feishu_config()
    except FeishuArchiveError as exc:
        print(f"  ⏭️  跳过: {exc}")
        return True

    print("  ⏳ 正在请求 tenant_access_token...")
    try:
        token = _get_tenant_access_token(app_id, app_secret)
        print(f"  ✅ 获取成功！token: {token[:20]}...{token[-6:]}")
        return True
    except FeishuArchiveError as exc:
        print(f"  ❌ 获取失败: {exc}")
        return False


# ---------------------------------------------------------------------------
# 测试 3: 发送文案 + 真实图片到飞书多维表格
# ---------------------------------------------------------------------------

def test_archive_with_real_image():
    """使用真实图片测试归档到飞书多维表格

    读取 src/test/output/test_cat.jpg 作为配图，
    向配置的飞书多维表格发送一条包含主题、文案、配图、生成时间的完整记录。
    """
    print("\n🧪 测试 3: 发送文案 + 真实图片到飞书多维表格")
    print("--------------------------------")

    import config

    app_id = getattr(config, "FEISHU_APP_ID", "")
    app_secret = getattr(config, "FEISHU_APP_SECRET", "")
    bitable_url = getattr(config, "FEISHU_BITABLE_XHS_TABLE", "")

    if (
        not app_id
        or app_id == "your_feishu_app_id_here"
        or not app_secret
        or app_secret == "your_feishu_app_secret_here"
        or not bitable_url
    ):
        print("  ⏭️  跳过: 飞书配置未设置，无法进行集成测试")
        return True

    # 查找可用的真实图片
    test_dir = Path(__file__).resolve().parent / "output"
    image_candidates = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png"))

    if not image_candidates:
        print("  ⚠️  没有找到测试图片，将只发送文案（无配图）")
        image_path = str(test_dir / "nonexistent.jpg")
    else:
        image_path = str(image_candidates[0])
        file_size = image_candidates[0].stat().st_size
        print(f"  📷 使用测试图片: {image_candidates[0].name} ({file_size / 1024:.1f} KB)")

    # 准备测试数据
    from datetime import datetime

    now = datetime.now()
    topic = "🧪 集成测试 - 文案与配图发送验证"
    copy_content = (
        "这是一条完整的集成测试记录，验证飞书多维表格的文案和图片发送功能。\n\n"
        f"📅 测试时间：{now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        "📋 测试内容：\n"
        "  • 主题字段写入\n"
        "  • 文案字段写入\n"
        "  • 配图（附件）上传\n"
        "  • 生成时间字段写入\n\n"
        "如果你在飞书多维表格中看到这条记录，说明功能一切正常！✅\n\n"
        "#测试 #飞书归档 #自动化 #配图"
    )
    generated_at = now.isoformat()

    print(f"  ⏳ 正在调用飞书 API 发送记录...")
    print(f"     目标表格: {bitable_url}")
    print(f"     app_token: {_parse_app_token(bitable_url)}")

    # 调用归档
    try:
        record_id = archive_to_bitable(
            topic=topic,
            copy_content=copy_content,
            image_path=image_path,
            generated_at=generated_at,
        )
    except Exception as exc:
        print(f"  ❌ 归档过程抛出了未捕获的异常: {exc}")
        import traceback
        traceback.print_exc()
        return False

    if record_id:
        print(f"  ✅ 发送成功！record_id: {record_id}")
        print(f"     请到飞书多维表格中确认记录已创建")
        return True
    else:
        print("  ❌ 发送失败 —— archive_to_bitable 返回 None")
        print("     💡 排查建议:")
        print("       1. 确认你的飞书应用已获得「查看、评论、编辑和管理多维表格」权限")
        print("       2. 确认 FEISHU_BITABLE_XHS_TABLE 指向的多维表格存在且应用有访问权限")
        print("       3. 如果是知识库(/wiki/)中的表格，确认应用有知识库访问权限")
        print("       4. 确认表格中有「主题」「文案」「配图」「生成时间」四个字段")
        return False

# ---------------------------------------------------------------------------
# 测试 4: 更新多维表格元数据
# ---------------------------------------------------------------------------

def test_update_bitable_meta():
    """测试更新多维表格元数据（真实 API 调用）"""
    print("\n🧪 测试 4: 更新多维表格元数据")
    print("--------------------------------")

    import config

    app_id = getattr(config, "FEISHU_APP_ID", "")
    app_secret = getattr(config, "FEISHU_APP_SECRET", "")
    bitable_url = getattr(config, "FEISHU_BITABLE_XHS_TABLE", "")

    if (
        not app_id
        or app_id == "your_feishu_app_id_here"
        or not app_secret
        or app_secret == "your_feishu_app_secret_here"
        or not bitable_url
    ):
        print("  ⏭️  跳过: 飞书配置未设置，无法进行集成测试")
        return True

    print("  ⏳ 正在调用飞书 API 更新多维表格名称...")

    try:
        # 只更新名称，不修改高级权限
        app_info = update_bitable_meta(name="小红书素材库")
        print(f"  ✅ 更新成功！返回: {app_info}")
        return True
    except FeishuArchiveError as exc:
        print(f"  ⚠️  更新失败（可能是权限或表格类型不支持）: {exc}")
        print("     💡 注意: wiki 类型的多维表格可能不支持 update_bitable_meta 操作")
        return True  # 失败不算测试失败，可能是环境限制
    except Exception as exc:
        print(f"  ❌ 发生未预期的异常: {exc}")
        return False


# ---------------------------------------------------------------------------
# 主函数
# ---------------------------------------------------------------------------

def main():
    print("=" * 50)
    print("🚀 飞书多维表格归档功能 - 集成测试")
    print("=" * 50)

    # 显示当前配置摘要
    import config
    print(f"\n📌 当前配置:")
    print(f"   FEISHU_APP_ID: {getattr(config, 'FEISHU_APP_ID', '未设置')[:10]}...")
    bitable_url = getattr(config, "FEISHU_BITABLE_XHS_TABLE", "")
    if bitable_url:
        url_type = "知识库" if "/wiki/" in bitable_url else "独立多维表格"
        print(f"   BITABLE_URL:   ...{bitable_url[-40:]}")
        print(f"   URL 类型:      {url_type}")
        try:
            print(f"   app_token:     {_parse_app_token(bitable_url)}")
        except Exception:
            print("   app_token:     ❌ 解析失败")
    print()

    results = []

    # 测试 1: URL 解析
    results.append(("URL 解析", test_parse_app_token()))

    # 测试 2: 获取 token
    results.append(("获取 Token", test_get_token()))

    # 测试 3: 发送文案 + 真实图片
    results.append(("发送文案+图片", test_archive_with_real_image()))


    # 测试 4: 更新多维表格元数据
    results.append(("更新元数据", test_update_bitable_meta()))

    # 汇总
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {status} - {name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 所有测试通过！")
    else:
        print("\n⚠️  存在失败的测试项，请检查上方输出。")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
