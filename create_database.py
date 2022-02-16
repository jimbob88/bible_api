import scandir_rs as scandir
import os

for root, dirs, files in scandir.walk.Walk("./sources"):
    for file in files:
        with open(os.path.join(root, file), "r", encoding="utf8") as f:
            print(f.read())
