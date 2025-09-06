#!/bin/bash
set -e

# 设置运行目录
mkdir -p /tmp/code-server/{config,data,cache,extensions}

# 启动 code-server（假设你已安装在当前目录）
npx code-server \
  --host 0.0.0.0 \
  --port 8080 \
  --auth none \
  --user-data-dir /tmp/code-server/data \
  --extensions-dir /tmp/code-server/extensions
