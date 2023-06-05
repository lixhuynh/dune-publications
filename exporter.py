import subprocess

with open("output.html", "w+") as output:
    subprocess.call(["python", "./backend.py"], stdout=output)