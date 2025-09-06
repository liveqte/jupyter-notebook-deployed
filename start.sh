#!/bin/bash
set -e

# 设置运行目录
mkdir -p /tmp/code-server/{config,data,cache,extensions}

# 启动 code-server（假设你已安装在当前目录）
./code-server-4.103.2-linux-amd64/bin/code-server \
  --port 8080 \
  --auth none \
  --user-data-dir /tmp/code-server/data \
  --extensions-dir /tmp/code-server/extensions
