#!/bin/bash
set -e

# 设置版本号
VERSION="4.103.2"
ARCHIVE="code-server-${VERSION}-linux-amd64.tar.gz"
DIR="code-server-${VERSION}-linux-amd64"
URL="https://github.com/coder/code-server/releases/download/v${VERSION}/${ARCHIVE}"
EXEC="./${DIR}/bin/code-server"

# 创建运行目录
mkdir -p /tmp/code-server/{config,data,cache,extensions}

# 设置环境变量，重定向所有写入路径
export HOME=/tmp/code-server
export XDG_CONFIG_HOME=/tmp/code-server/config
export XDG_DATA_HOME=/tmp/code-server/data
export XDG_CACHE_HOME=/tmp/code-server/cache
export CODE_SERVER_EXTENSIONS=/tmp/code-server/extensions

# 下载并解压 code-server（如果未存在）
if [ -f "$EXEC" ]; then
  echo "✅ 已存在 code-server 可执行文件，跳过下载"
else
  echo "📦 正在下载 code-server v${VERSION}..."
  curl -LsS -o "$ARCHIVE" "$URL"
  echo "📂 正在解压..."
  tar -xzf "$ARCHIVE"
fi

# 启动 code-server，监听 8080 端口，无认证
$EXEC \
  --port 8080 \
  --auth none \
  --user-data-dir /tmp/code-server/data \
  --extensions-dir /tmp/code-server/extensions
