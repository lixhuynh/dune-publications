import subprocess

with open("../index.html", "w+") as output:
    subprocess.call(["python", "./backend.py"], stdout=output)