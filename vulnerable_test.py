# vulnerable_test.py

import os
import subprocess
import sys
import requests
from flask import request


def command_injection():
    # Tainted input from web request
    user_cmd = request.args.get("cmd")

    # Dangerous sink
    os.system(user_cmd)


def subprocess_injection():
    arg = request.form.get("arg")
    subprocess.run(arg, shell=True)


def eval_usage():
    code = request.args.get("code")
    eval(code)


def exec_usage():
    dynamic_code = input("Enter Python code: ")
    exec(dynamic_code)


def unsafe_file_write():
    filename = request.args.get("filename")

    # Unsafe write
    with open(filename, "w") as f:
        f.write("Overwritten content")


def network_sink():
    data = request.args.get("data")

    # Tainted data sent externally
    requests.post("https://example.com/api", json={"payload": data})


def mixed_flow():
    x = request.args.get("value")
    y = x  # Propagation test
    os.system(y)


def safe_example():
    # This one should NOT trigger taint flow
    safe_cmd = "ls -la"
    os.system(safe_cmd)
