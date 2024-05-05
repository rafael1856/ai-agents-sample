import os
import subprocess
import sys

APP_PATH = os.path.dirname(sys.argv[0])
os.environ['OLLAMA_KEEP_ALIVE'] = '30'
os.environ['OLLAMA_DEBUG'] = '1'
os.environ['MODEL'] = 'llama3'

# remove old cache
subprocess.run(['rm', '-rf', '.cache'], check=True)

subprocess.run(['sudo', 'systemctl', 'restart', 'ollama'], check=True)

# Check if ollama is running a model
if not subprocess.run(['pgrep', '-f', 'ollama run'], stdout=subprocess.DEVNULL).returncode == 0:
    # If ollama serve is not running, start it
    with open(os.path.join(APP_PATH, 'server_run.log'), 'w') as f:
        subprocess.Popen(['ollama', 'run', os.environ['MODEL'], '--verbose'], stdout=f, stderr=subprocess.STDOUT)

# Check if ollama serve is running
if not subprocess.run(['pgrep', '-f', 'ollama serve'], stdout=subprocess.DEVNULL).returncode == 0:
    # If ollama serve is not running, start it
    # clean old logs
    os.remove(os.path.join(APP_PATH, 'server_serve.log'))
    with open(os.path.join(APP_PATH, 'server_serve.log'), 'w') as f:
        subprocess.Popen(['ollama', 'serve'], stdout=f, stderr=subprocess.STDOUT)

# Check if Conda environment 'aiagent2' is activated
if os.environ.get('CONDA_DEFAULT_ENV') != 'aiagent2':
    # If 'aiagent2' is not activated, activate it
    subprocess.run(['source', 'activate', 'aiagent2'], shell=True, check=True)

# Check if litellm is running
if not subprocess.run(['pgrep', '-f', 'litellm'], stdout=subprocess.DEVNULL).returncode == 0:
    # If litellm is not running, start it
    # clean old logs
    os.remove(os.path.join(APP_PATH, 'server_litellm.log'))
    with open(os.path.join(APP_PATH, 'server_litellm.log'), 'w') as f:
        subprocess.Popen(['litellm', '--model', 'ollama/' + os.environ['MODEL'], '--api_base', 'http://127.0.0.1:11434', '--debug'], stdout=f, stderr=subprocess.STDOUT)

# Start the application 
subprocess.run(['python', os.path.join(APP_PATH, 'multi-agents.py')], check=True)