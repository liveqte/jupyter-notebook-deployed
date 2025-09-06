#!/bin/bash
set -e

# 安装版本
VERSION="4.103.2"
ARCHIVE="code-server-${VERSION}-linux-amd64.tar.gz"
DIR="code-server-${VERSION}-linux-amd64"
URL="https://github.com/coder/code-server/releases/download/v${VERSION}/${ARCHIVE}"

# 下载并解压
curl -LsS -o "$ARCHIVE" "$URL"
tar -xzf "$ARCHIVE"

