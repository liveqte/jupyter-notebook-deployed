#!/usr/bin/env python3
import sys
import json
import base64
import urllib.parse
import re

def parse_vmess(link):
    data = base64.urlsafe_b64decode(link.split("://")[1] + "==").decode('utf-8')
    config = json.loads(data)
    outbound = {
        "type": "vmess",
        "tag": config.get("ps", "vmess-out"),
        "server": config["add"],
        "server_port": int(config["port"]),
        "uuid": config["id"],
        "security": config.get("scy", "auto"),
        "alter_id": int(config.get("aid", 0)),
    }
    if config.get("net") == "ws":
        path = config.get("path", "/")
        # Parse ?ed= from path
        match = re.search(r'\?ed=(\d+)', path)
        transport = {
            "type": "ws",
            "headers": {"Host": config.get("host", "")} if config.get("host") else {}
        }
        if match:
            ed_value = int(match.group(1))
            transport["max_early_data"] = ed_value
            transport["early_data_header_name"] = "Sec-WebSocket-Protocol"
            # Remove ?ed= from path for Sing-box compatibility
            path = re.sub(r'\?ed=\d+', '', path)
        transport["path"] = path
        outbound["transport"] = transport
    if config.get("tls") == "tls":
        alpn_list = config.get("alpn", "").split(",") if config.get("alpn") else []
        outbound["tls"] = {
            "enabled": True,
            "server_name": config.get("sni") or config.get("host", ""),
            "insecure": config.get("insecure", "0") == "1",
            "alpn": alpn_list,
            "utls": {"enabled": True, "fingerprint": config.get("fp", "chrome")}
        }
    return outbound

def parse_vless(link):
    parsed = urllib.parse.urlparse(link)
    query = urllib.parse.parse_qs(parsed.query)
    outbound = {
        "type": "vless",
        "tag": "vless-out",
        "server": parsed.hostname,
        "server_port": parsed.port,
        "uuid": parsed.username,
    }
    if query.get("security") == ["tls"]:
        alpn_list = query.get("alpn", [""])[0].split(",") if query.get("alpn") else []
        outbound["tls"] = {
            "enabled": True,
            "server_name": query.get("sni", [None])[0] or "",
            "insecure": query.get("allowInsecure", ["0"])[0] == "1",
            "alpn": alpn_list,
            "utls": {"enabled": True, "fingerprint": query.get("fp", ["chrome"])[0]}
        }
    if query.get("type") == ["ws"]:
        path = query.get("path", ["/"])[0]
        # Parse ?ed= from path
        match = re.search(r'\?ed=(\d+)', path)
        transport = {
            "type": "ws",
            "headers": {"Host": query.get("host", [""])[0]} if query.get("host") else {}
        }
        if match:
            ed_value = int(match.group(1))
            transport["max_early_data"] = ed_value
            transport["early_data_header_name"] = "Sec-WebSocket-Protocol"
            # Remove ?ed= from path for Sing-box compatibility
            path = re.sub(r'\?ed=\d+', '', path)
        transport["path"] = path
        outbound["transport"] = transport
    if query.get("flow"):
        outbound["flow"] = query["flow"][0]
    return outbound

if len(sys.argv) != 2:
    print("用法: python3 vlink_to_singbox.py 'vmess://... 或 vless://...'")
    sys.exit(1)
link = sys.argv[1]
if link.startswith("vmess://"):
    outbound = parse_vmess(link)
elif link.startswith("vless://"):
    outbound = parse_vless(link)
else:
    print("不支持的链接类型")
    sys.exit(1)

full_config = {
    "log": {"level": "info"},
    "inbounds": [{
        "type": "mixed",
        "tag": "mixed-in",
        "listen": "127.0.0.1",
        "listen_port": 1080,
        "sniff": True,
        "sniff_override_destination": True
    }],
    "outbounds": [outbound],
    "route": {"final": outbound["tag"]}
}

print(json.dumps(full_config, indent=2))
# 可选：保存到文件
# with open("singbox_config.json", "w") as f:
#     json.dump(full_config, f, indent=2)
