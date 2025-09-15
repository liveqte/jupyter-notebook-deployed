import os
import subprocess
from pathlib import Path
import shutil

def show_path_info():
    print("🔍 Current PATH environment variable:")
    print(os.environ.get("PATH", "❌ PATH not set"))
    
    jupyter_path = shutil.which("jupyter")
    if jupyter_path:
        print(f"✅ Found 'jupyter' at: {jupyter_path}")
    else:
        print("❌ 'jupyter' command not found in PATH. You may need to add it manually.")

def generate_config():
    print("🛠 Checking Jupyter config...")
    config_path = Path.home() / ".jupyter" / "jupyter_server_config.py"
    if config_path.exists():
        print("⚙️ Config file already exists. Skipping generation.")
    else:
        print("📄 Generating new Jupyter config...")
        subprocess.run(["jupyter", "server", "--generate-config"], check=True)

def set_password():
    from jupyter_server.auth import passwd
    password = os.environ.get("PASS")
    if not password:
        print("❌ Environment variable PASS not set.")
        exit(1)
    hashed = passwd(password)
    config_path = Path.home() / ".jupyter" / "jupyter_server_config.py"
    with open(config_path, "a") as f:
        f.write(f"\nc.ServerApp.password = '{hashed}'\n")
        f.write("c.ServerApp.ip = '0.0.0.0'\n")
        f.write("c.ServerApp.open_browser = False\n")
        f.write("c.ServerApp.port = 8501\n")
    print("✅ Password and config updated.")

def start_server():
    print("🚀 Starting Jupyter Server...")
    subprocess.run("nohup jupyter server > jupyter.log 2>&1 &", shell=True)

if __name__ == "__main__":
    show_path_info()
    generate_config()
    set_password()
    start_server()
    print("🎉 Jupyter Server is now running on port 8501. Check jupyter.log for output.")
