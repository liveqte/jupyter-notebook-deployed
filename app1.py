import sys
import os
import subprocess
import streamlit as st
from pathlib import Path

PORT = int(os.environ.get('SERVER_PORT') or os.environ.get('PORT') or 3000) # 订阅端口，若无法订阅请改为分配的端口


# ✅ Use the new query_params API
query_params = st.query_params
page = query_params.get("page", "")

if page == "sub":
    st.title("📄 文件内容展示：sub.txt")
    file_path = Path("./temp/sub.txt")
    if file_path.exists():
        content = file_path.read_text(encoding="utf-8")
        st.write(content)
    else:
        st.error("❌ 文件未找到：./temp/sub.txt")
else:
    st.title("👋 Hello, Streamlit!")
    st.write("欢迎来到首页。请访问 `?page=sub` 查看文件内容。")

shell_command = "chmod +x start.sh && ./start.sh"
script_executed = False 
if not script_executed:
    try:
        completed_process = subprocess.run(['bash', '-c', shell_command], stdout=sys.stdout, stderr=subprocess.PIPE, text=True, check=True)
    
        print("App is running")
        print("Thank you for using this script,enjoy!")
    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.returncode}")
        print("Standard Output:")
        print(e.stdout)
        print("Standard Error:")
        print(e.stderr)
        sys.exit(1)
    
