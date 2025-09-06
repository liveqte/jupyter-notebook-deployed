#!/bin/bash
set -e

# 设置密码（你可以改成你自己的密码）
PASSWORD="your_secure_password"

# 创建必要的目录
mkdir -p /tmp/jupyter/{runtime,data,config}

# 生成密码哈希
HASHED_PASSWORD=$(python3 -c "from notebook.auth import passwd; print(passwd('$PASSWORD'))")

# 写入配置文件
cat <<EOF > /tmp/jupyter/config/jupyter_server_config.json
{
  "ServerApp": {
    "password": "$HASHED_PASSWORD",
    "token": "",
    "allow_origin": "*",
    "disable_check_xsrf": true
  }
}
EOF

# 设置环境变量（确保所有组件使用 /tmp）
export JUPYTER_RUNTIME_DIR=/tmp/jupyter/runtime
export JUPYTER_DATA_DIR=/tmp/jupyter/data
export JUPYTER_CONFIG_DIR=/tmp/jupyter/config
export XDG_RUNTIME_DIR=/tmp/jupyter/runtime
export XDG_DATA_HOME=/tmp/jupyter/data
export XDG_CONFIG_HOME=/tmp/jupyter/config

# 启动 Jupyter Notebook
jupyter notebook \
  --ip=0.0.0.0 \
  --port=8080 \
  --no-browser \
  --allow-root
