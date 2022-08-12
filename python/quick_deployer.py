from subprocess import Popen, PIPE, STDOUT  
from flask import Flask, request
import requests as r
from threading import Thread
import os
app = Flask(__name__)

TOKEN = "TOKEN" #e.g. ghp_KLIzyd4rQX5x577tBtahHTbMrmRXZW1NyIgK
REPO = 'THE TARGET GITHUB REPO'   # e.g. salut1618/autonomous
START_COMMAND = "ACTUAL COMAND TO START THE BIGGER PROJECT"  #e.g. "python app.py"

BRANCH_NAME = 'main'   #e.g. main
URL = f" https://{TOKEN}@github.com/{REPO}"
UPDATE_COMMAND = f"git init; git remote add origin {URL} ; git fetch origin main ; git reset --hard FETCH_HEAD"
os.environ['PYTHONUNBUFFERED'] = '1'

def create_com(com, is_shell=False):
    return Popen(com, shell=is_shell,stderr=STDOUT, stdout=PIPE, env=os.environ)

def process_stdout_logger(p, is_main=False):
    while True:
        output = p.stdout.readline()
        if p.poll() is not None:
            break
        if output:
            output = output.decode()
            print("[MAIN]" if is_main else "[UPDATER]",output, end="")

main_proc = create_com(UPDATE_COMMAND, True)
process_stdout_logger(main_proc)
main_proc = create_com(START_COMMAND, True)
Thread(target=process_stdout_logger,args=(main_proc,True,)).start()


@app.route('/payload', methods=["POST"])
def payload():
    global main_proc
    ev = request.headers.get("X-Github-Event")
    if ev == "push":
        print("[CLONER] New push detected. Updating files...")
        main_proc.kill()
        main_proc = create_com(UPDATE_COMMAND, True)
        process_stdout_logger(main_proc)
        main_proc = create_com(START_COMMAND, True)
        Thread(target=process_stdout_logger,args=(main_proc,True,)).start()
    return '1'

app.run(host='0.0.0.0', port= os.environ['PORT'] if 'PORT' in os.environ else 80)
