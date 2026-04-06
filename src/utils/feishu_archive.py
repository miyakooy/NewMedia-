"""飞书多维表格归档模块。

使用 lark-oapi 官方 SDK 将生成的内容归档到飞书多维表格（Bitable）。
同时提供基于 requests 的 REST API 方法（如更新多维表格元数据）。
表格字段：主题、文案、配图、生成时间。
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import click
import requests

import config


class FeishuArchiveError(RuntimeError):
    """飞书归档失败。"""
    pass


def _get_feishu_config() -> tuple[str, str, str]:
    """获取飞书配置，返回 (app_id, app_secret, bitable_url)。"""
    app_id = getattr(config, "FEISHU_APP_ID", "")
    app_secret = getattr(config, "FEISHU_APP_SECRET", "")
    bitable_url = getattr(config, "FEISHU_BITABLE_XHS_TABLE", "")

    if not app_id or app_id == "your_feishu_app_id_here":
        raise FeishuArchiveError("FEISHU_APP_ID 未配置")
    if not app_secret or app_secret == "your_feishu_app_secret_here":
        raise FeishuArchiveError("FEISHU_APP_SECRET 未配置")
    if not bitable_url:
        raise FeishuArchiveError("FEISHU_BITABLE_XHS_TABLE 未配置")

    return app_id, app_secret, bitable_url


def _parse_app_token(bitable_url: str) -> str:
    """从飞书多维表格 URL 中解析 app_token。

    支持的 URL 格式:
      - https://xxx.feishu.cn/base/BFLWbehbEaX3jJs9kkQcxXfHnvd
      - https://xxx.feishu.cn/wiki/XY4DwsyKHitnoLkaDKEc7MlWnxd
      - https://xxx.feishu.cn/base/BFLWbehbEaX3jJs9kkQcxXfHnvd?table=tbl...
    """
    # 尝试从 URL 路径中提取最后一段 token
    match = re.search(r"/(?:base|wiki)/([A-Za-z0-9]+)", bitable_url)
    if match:
        return match.group(1)
    raise FeishuArchiveError(f"无法从 URL 解析 app_token: {bitable_url}")


# ---------------------------------------------------------------------------
# 错误码映射（来自飞书官方文档）
# ---------------------------------------------------------------------------

_BITABLE_ERROR_CODES: dict[int, str] = {
    1254000: "请求体 JSON 格式错误 (WrongRequestJson)",
    1254001: "请求体错误 (WrongRequestBody)",
    1254002: "内部错误，有疑问可咨询客服 (Fail)",
    1254003: "app_token 错误 (WrongBaseToken)",
    1254010: "请求错误 (ReqConvError)",
    1254031: "多维表格名称格式错误：长度不超过100字符，不能包含 ? / \\ * : [ ] (InvalidAppName)",
    1254036: "多维表格副本复制中，请稍后重试 (Base is copying)",
    1254040: "app_token 不存在 (BaseTokenNotFound)",
    1254043: "record_id 不存在 (RecordIdNotFound)",
    1254061: "字段格式错误，请确认对应字段类型参数格式是否正确",
    1254200: "内部错误 (internal error)",
    1254290: "请求过快，请稍后重试 (TooManyRequest)",
    1254291: "写冲突：同一数据表不支持并发调用写接口 (Write conflict)",
    1254301: "多维表格未开启高级权限或不支持开启高级权限 (OperationTypeError)",
    1254302: "无访问权限，常由表格开启了高级权限造成 (Permission denied)",
    1254304: "无权限 (The role has no permissions)",
    1255001: "内部错误，有疑问可咨询客服 (InternalError)",
    1255002: "内部错误，有疑问可咨询客服 (RpcError)",
    1255003: "序列化错误，有疑问可咨询客服 (MarshalError)",
    1255004: "反序列化错误 (UmMarshalError)",
    1255040: "请求超时，请重试",
}


def _validate_bitable_name(name: str) -> None:
    """校验多维表格名称合法性。

    规则来源：飞书 API 文档 —— 长度不超过 100 个字符，不能包含 ? / \\ * : [ ]

    Raises:
        FeishuArchiveError: 名称不合法时抛出。
    """
    if len(name) > 100:
        raise FeishuArchiveError(
            f"多维表格名称不能超过 100 个字符，当前长度: {len(name)}"
        )
    forbidden_chars = set('?/\\*:[]')
    found = [ch for ch in name if ch in forbidden_chars]
    if found:
        raise FeishuArchiveError(
            f"多维表格名称不能包含特殊字符 ? / \\ * : [ ]，"
            f"发现: {''.join(set(found))}"
        )


# ---------------------------------------------------------------------------
# 基于 requests 的飞书 REST API 封装
# ---------------------------------------------------------------------------

def _get_tenant_access_token(app_id: str, app_secret: str) -> str:
    """获取飞书 tenant_access_token（应用身份令牌）。

    文档: https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token_internal

    Returns:
        tenant_access_token 字符串

    Raises:
        FeishuArchiveError: 获取失败时抛出
    """
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": app_id,
        "app_secret": app_secret,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        raise FeishuArchiveError(f"获取 tenant_access_token 网络请求失败: {exc}") from exc

    if data.get("code") != 0:
        raise FeishuArchiveError(
            f"获取 tenant_access_token 失败: code={data.get('code')}, msg={data.get('msg')}"
        )

    token = data.get("tenant_access_token", "")
    if not token:
        raise FeishuArchiveError("获取 tenant_access_token 返回为空")
    return token


def _resolve_app_token(bitable_url: str, app_id: str, app_secret: str) -> str:
    """如果是 base URL，直接返回 app_token；如果是 wiki URL，则调用接口将 node_token 转为真正的 app_token。"""
    token = _parse_app_token(bitable_url)
    if "/wiki/" in bitable_url:
        access_token = _get_tenant_access_token(app_id, app_secret)
        url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={token}"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if not resp.ok:
                raise FeishuArchiveError(f"HTTP {resp.status_code}: {resp.text}")
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as exc:
            raise FeishuArchiveError(f"获取 Wiki 节点网络请求失败: {exc}") from exc
            
        if data.get("code") != 0:
            raise FeishuArchiveError(f"获取 Wiki 节点失败: code={data.get('code')}, msg={data.get('msg')}")
            
        node = data.get("data", {}).get("node", {})
        obj_token = node.get("obj_token", "")
        if not obj_token:
            raise FeishuArchiveError("获取到的 Wiki 节点中无 obj_token")
        return obj_token
        
    return token

def update_bitable_meta(
    name: str | None = None,
    is_advanced: bool | None = None,
    app_token: str | None = None,
) -> dict[str, Any]:
    """更新飞书多维表格元数据（名称、高级权限开关）。

    使用 requests 直接调用 REST API:
        PUT https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token

    所需权限（满足其一即可）:
        - 更新多维表格 (base:app:update)
        - 查看、评论、编辑和管理多维表格 (bitable:app)

    Args:
        name: 新的多维表格名称，None 表示不更新。
        is_advanced: 是否开启高级权限，None 表示不更新。
        app_token: 多维表格的 app_token，为 None 时自动从 config 解析。

    Returns:
        响应中 data.app 字典，包含 app_token / name / is_advanced / time_zone 等。

    Raises:
        FeishuArchiveError: 参数无效或 API 调用失败时抛出。
    """
    if name is None and is_advanced is None:
        raise FeishuArchiveError("name 和 is_advanced 至少需要指定一个")

    # 校验名称合法性
    if name is not None:
        _validate_bitable_name(name)

    # 获取配置
    cfg_app_id, cfg_app_secret, bitable_url = _get_feishu_config()

    # 解析 app_token（包含 Wiki 转换逻辑）
    if app_token is None:
        app_token = _resolve_app_token(bitable_url, cfg_app_id, cfg_app_secret)

    # 获取 tenant_access_token
    access_token = _get_tenant_access_token(cfg_app_id, cfg_app_secret)

    # 构造请求
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8",
    }

    body: dict[str, Any] = {}
    if name is not None:
        body["name"] = name
    if is_advanced is not None:
        body["is_advanced"] = is_advanced

    try:
        resp = requests.put(url, json=body, headers=headers, timeout=10)
        resp.raise_for_status()
        result = resp.json()
    except requests.RequestException as exc:
        raise FeishuArchiveError(f"更新多维表格元数据网络请求失败: {exc}") from exc

    code = result.get("code", -1)
    if code != 0:
        hint = _BITABLE_ERROR_CODES.get(code, "")
        msg = result.get("msg", "")
        detail = f"code={code}, msg={msg}"
        if hint:
            detail += f" | 排查建议: {hint}"
        raise FeishuArchiveError(f"更新多维表格元数据失败: {detail}")

    app_info = result.get("data", {}).get("app", {})
    click.echo(click.style(
        f"✅ 多维表格元数据已更新: name={app_info.get('name')}, "
        f"is_advanced={app_info.get('is_advanced')}",
        fg="green",
    ))
    return app_info


def _build_client(app_id: str, app_secret: str):
    """构建 lark-oapi 客户端。"""
    try:
        import lark_oapi as lark
    except ImportError as exc:
        raise FeishuArchiveError(
            "未安装 lark-oapi 依赖，请执行 pip install lark-oapi"
        ) from exc

    client = (
        lark.Client.builder()
        .app_id(app_id)
        .app_secret(app_secret)
        .build()
    )
    return client


def _get_first_table_id(client, app_token: str) -> str:
    """自动获取多维表格中第一个数据表的 table_id。"""
    from lark_oapi.api.bitable.v1 import ListAppTableRequest

    request = (
        ListAppTableRequest.builder()
        .app_token(app_token)
        .page_size(1)
        .build()
    )

    response = client.bitable.v1.app_table.list(request)

    if not response.success():
        hint = _BITABLE_ERROR_CODES.get(response.code, "")
        detail = f"code={response.code}, msg={response.msg}"
        if hint:
            detail += f" | 排查建议: {hint}"
        raise FeishuArchiveError(f"获取数据表列表失败: {detail}")

    items = getattr(response.data, "items", None)
    if not items or len(items) == 0:
        raise FeishuArchiveError("多维表格中没有数据表")

    table_id = items[0].table_id
    return table_id


def _upload_image(client, image_path: str, app_token: str) -> str | None:
    """上传图片到飞书，返回 file_token。失败返回 None。"""
    from lark_oapi.api.drive.v1 import UploadAllMediaRequest, UploadAllMediaRequestBody

    path = Path(image_path)
    if not path.exists():
        return None

    file_size = path.stat().st_size
    file_name = path.name

    with open(path, "rb") as f:
        request = (
            UploadAllMediaRequest.builder()
            .request_body(
                UploadAllMediaRequestBody.builder()
                .file_name(file_name)
                .parent_type("bitable_file")
                .parent_node(app_token)
                .size(file_size)
                .file(f)
                .build()
            )
            .build()
        )

        response = client.drive.v1.media.upload_all(request)

    if not response.success():
        raise FeishuArchiveError(
            f"图片上传失败: code={response.code}, msg={response.msg}"
        )

    return response.data.file_token


def _create_record(
    client,
    app_token: str,
    table_id: str,
    fields: dict[str, Any],
) -> str:
    """在多维表格中创建一条记录，返回 record_id。"""
    from lark_oapi.api.bitable.v1 import (
        CreateAppTableRecordRequest,
        AppTableRecord,
    )

    request = (
        CreateAppTableRecordRequest.builder()
        .app_token(app_token)
        .table_id(table_id)
        .request_body(
            AppTableRecord.builder()
            .fields(fields)
            .build()
        )
        .build()
    )

    response = client.bitable.v1.app_table_record.create(request)

    if not response.success():
        hint = _BITABLE_ERROR_CODES.get(response.code, "")
        detail = f"code={response.code}, msg={response.msg}"
        if hint:
            detail += f" | 排查建议: {hint}"
        raise FeishuArchiveError(f"创建记录失败: {detail}")

    return response.data.record.record_id


def archive_to_bitable(
    topic: str,
    copy_content: str,
    image_path: str,
    generated_at: str,
) -> str | None:
    """将生成结果归档到飞书多维表格。

    Args:
        topic: 主题
        copy_content: 文案完整内容
        image_path: 图片文件路径
        generated_at: 生成时间 ISO 格式字符串

    Returns:
        成功时返回 record_id，失败时返回 None 并打印红色 Warning。
    """
    try:
        app_id, app_secret, bitable_url = _get_feishu_config()
        app_token = _resolve_app_token(bitable_url, app_id, app_secret)
        client = _build_client(app_id, app_secret)

        # 自动获取第一个数据表的 table_id
        table_id = _get_first_table_id(client, app_token)

        # 上传配图并获取 file_token
        file_token = None
        try:
            file_token = _upload_image(client, image_path, app_token)
        except FeishuArchiveError as img_err:
            click.echo(click.style(f"⚠️  配图上传失败: {img_err}", fg="red"))
            # 配图上传失败不影响记录创建，继续

        # 构造字段数据
        # 将 ISO 时间字符串转为毫秒时间戳（飞书日期字段要求）
        try:
            dt = datetime.fromisoformat(generated_at)
            timestamp_ms = int(dt.timestamp() * 1000)
        except (ValueError, TypeError):
            timestamp_ms = int(datetime.now().timestamp() * 1000)

        fields: dict[str, Any] = {
            "主题": topic,
            "文案": copy_content,
            "生成时间": timestamp_ms,
        }

        # 如果图片上传成功，添加配图字段
        if file_token:
            fields["配图"] = [{"file_token": file_token}]

        record_id = _create_record(client, app_token, table_id, fields)
        click.echo(click.style(f"✅ 已归档到飞书多维表格 (record_id: {record_id})", fg="green"))
        return record_id

    except FeishuArchiveError as exc:
        click.echo(click.style(f"⚠️  飞书归档失败: {exc}", fg="red"))
        return None
    except Exception as exc:
        click.echo(click.style(f"⚠️  飞书归档发生未知错误: {exc}", fg="red"))
        return None
