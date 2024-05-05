import os
import subprocess
import sys

APP_PATH = os.path.dirname(sys.argv[0])

subprocess.run(['sudo', 'systemctl', 'stop', 'ollama'], check=True)

# Check if ollama serve is running
if subprocess.run(['pgrep', '-f', 'ollama serve'], stdout=subprocess.DEVNULL).returncode == 0:
    # If ollama serve is running, kill it
    subprocess.run(['pkill', '-f', 'ollama serve'], check=True)

# Check if ollama is running a model
if subprocess.run(['pgrep', '-f', 'ollama run'], stdout=subprocess.DEVNULL).returncode == 0:
    # If ollama run is running, kill it
    subprocess.run(['pkill', '-f', 'ollama run'], check=True)

# Check if litellm is running
if subprocess.run(['pgrep', '-f', 'litellm'], stdout=subprocess.DEVNULL).returncode == 0:
    # If litellm is running, kill it
    subprocess.run(['pkill', '-f', 'litellm'], check=True)

# clean old logs
# os.remove('logs/*.log') # Uncomment this line if you want to remove logs