import os
import subprocess
import getpass
from pathlib import Path

def install_jupyter():
    print("📦 Installing Jupyter Notebook...")
    subprocess.run(["pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run(["pip", "install", "jupyter"], check=True)

def generate_config():
    print("🛠 Generating Jupyter config...")
    subprocess.run(["jupyter", "notebook", "--generate-config"], check=True)

def set_password():
    from notebook.auth import passwd
    password = getpass.getpass("🔐 Enter a password for Jupyter Notebook: ")
    hashed = passwd(password)
    config_path = Path.home() / ".jupyter" / "jupyter_notebook_config.py"
    with open(config_path, "a") as f:
        f.write(f"\nc.NotebookApp.password = u'{hashed}'\n")
        f.write("c.NotebookApp.ip = '0.0.0.0'\n")
        f.write("c.NotebookApp.open_browser = False\n")
        f.write("c.NotebookApp.port = 8888\n")
    print("✅ Password and config updated.")

def start_jupyter():
    print("🚀 Starting Jupyter Notebook...")
    subprocess.run(["nohup", "jupyter", "notebook", ">", "jupyter.log", "2>&1", "&"], shell=True)

if __name__ == "__main__":
    install_jupyter()
    generate_config()
    set_password()
    start_jupyter()
    print("🎉 Jupyter Notebook is now running on port 8888. Check jupyter.log for output.")
