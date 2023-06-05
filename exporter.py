import subprocess

with open("output.txt", "w+") as output:
    subprocess.call(["python", "./backend.py"], stdout=output)