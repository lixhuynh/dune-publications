import subprocess

with open("../index.html", "w+") as output:
    subprocess.call(["python", "./script.py"], stdout=output)