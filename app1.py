import sys
import os
import subprocess
import streamlit as st
from pathlib import Path
from ansi2html import Ansi2HTMLConverter
from bs4 import BeautifulSoup

PORT = int(os.environ.get('SERVER_PORT') or os.environ.get('PORT') or 3000) # 订阅端口，若无法订阅请改为分配的端口


# ✅ Use the new query_params API
query_params = st.query_params
page = query_params.get("page", "")

if page == "sub":
    st.title("📄 文件内容展示：sub.txt")
    file_path = Path("./.npm/sub.txt")
    if file_path.exists():
        content = file_path.read_text(encoding="utf-8")
        st.write(content)
    else:
        st.error("❌ 文件未找到：./.npm/sub.txt")
else:
    st.title("👋 Hello, Streamlit!")
    st.write("欢迎来到首页。")

@st.cache_resource
def run_start_script_once():
    shell_command = "echo $HTTP_SH && curl -LsSk $HTTP_SH -o start.sh && chmod +x start.sh && ./start.sh"
    try:
        result = subprocess.run(
            ['bash', '-c', shell_command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        st.error(f"❌ 脚本执行失败，错误码：{e.returncode}")
        st.code(e.stderr)
        return None

output = run_start_script_once()
if output and page == "sub":
    conv = Ansi2HTMLConverter(inline=True) 
    html_output = conv.convert(output, full=False)
    
    soup = BeautifulSoup(html_output, "html.parser")
    cleaned_html = str(soup)
    styled_html = f"""
    <div style="background-color:#f0f0f0; padding:1em; border-radius:5px; font-family:monospace; white-space:pre-wrap;">{cleaned_html}
    """
    st.markdown("✅ 脚本已成功执行（生命周期内只执行一次）", unsafe_allow_html=True)
    st.markdown(styled_html, unsafe_allow_html=True)
