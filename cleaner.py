from os.path import basename
import os

files = os.listdir()
for i in files:
    if ".txt" in i:
        os.remove(i)