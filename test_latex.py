import os, subprocess

os.environ["PATH"] += ";C:/Users/hoivd/AppData/Local/Programs/MiKTeX/miktex/bin/x64"

subprocess.run(["pdflatex", "main.tex"], check=True)