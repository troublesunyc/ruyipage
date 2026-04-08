# -*- coding: utf-8 -*-
"""
示例38: 通过 fpfile 自动处理 HTTP 代理认证

演示内容：
- 通过 set_proxy() 配置 HTTP 代理地址
- 通过 set_fpfile() 让内核自动读取 httpauth.username/password
- 访问 http://ipinfo.io/json 并打印返回内容

fpfile 示例内容：
    httpauth.username:your-proxy-username
    httpauth.password:your-proxy-password

说明：
- 该示例依赖外部代理服务可用
- 若代理失效、网络受限或目标站点不可访问，示例会失败
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ruyipage import FirefoxOptions, FirefoxPage


PROXY_HOST = "your-proxy-host"
PROXY_PORT = 8080
TARGET_URL = "http://ipinfo.io/json"
FPFILE_PATH = r"C:\path\to\your\profile1.txt"


def main():
    print("=" * 60)
    print("示例38: 通过 fpfile 自动处理 HTTP 代理认证")
    print("=" * 60)

    opts = FirefoxOptions()
    opts.set_proxy(f"http://{PROXY_HOST}:{PROXY_PORT}")
    opts.set_fpfile(FPFILE_PATH)
    opts.headless(False)

    page = FirefoxPage(opts)

    try:
        print("\n0. 已启用代理自动认证:")
        print(f"   代理: http://{PROXY_HOST}:{PROXY_PORT}")
        print(f"   fpfile: {FPFILE_PATH}")
        print("   认证信息将由内核从 fpfile 自动读取")

        print(f"\n1. 通过代理访问: {TARGET_URL}")
        page.get(TARGET_URL)
        page.wait(2)

        print("\n2. 页面标题:")
        print(f"   {page.title}")

        print("\n3. 响应内容:")
        body_text = (
            page.run_js("return document.body ? document.body.innerText : ''") or ""
        ).strip()
        print(body_text)

        print("\n4. 解析返回内容:")
        try:
            data = json.loads(body_text)
        except Exception:
            data = _extract_ipinfo_from_text(body_text)

        if isinstance(data, dict):
            print(f"   IP: {data.get('ip')}")
            print(f"   城市: {data.get('city')}")
            print(f"   地区: {data.get('region')}")
            print(f"   国家: {data.get('country')}")
            if data.get("status") or data.get("error") or data.get("message"):
                print(f"   状态: {data.get('status')}")
                print(f"   错误: {data.get('error')}")
                print(f"   消息: {data.get('message')}")
        else:
            print("   返回内容不是标准 JSON，可能是目标站限流或页面被中间页接管。")

        print("\n" + "=" * 60)
        print("[OK] fpfile 代理认证示例执行完成")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FAIL] 示例执行失败: {e}")
        raise
    finally:
        try:
            page.quit()
        except Exception:
            pass


def _extract_ipinfo_from_text(text):
    """从 ipinfo 页面展示文本中提取常见字段。"""
    if not text:
        return None

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    fields = {}
    keys = {
        "ip",
        "city",
        "region",
        "country",
        "loc",
        "org",
        "postal",
        "timezone",
        "readme",
    }
    i = 0
    while i < len(lines) - 1:
        key = lines[i]
        if key in keys:
            value = lines[i + 1].strip().strip('"')
            fields[key] = value
            i += 2
            continue
        i += 1

    return fields or None


if __name__ == "__main__":
    main()
