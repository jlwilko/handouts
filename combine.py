#! /usr/bin/python3
import subprocess
import sys
import argparse

parser = argparse.ArgumentParser(description='Generate a note-taking pdf from a slide deck')
parser.add_argument("-i", "--input", help="input file", required=True)
parser.add_argument("-o", "--output", help="output file", required=True)

args = parser.parse_args()
file = args.input
new_name = args.output

# todo im adding a comment from the github ios app
# AND SOME MORE STUFF HERE
cmd = "rm sep/*"
print(subprocess.run(cmd, shell=True))

cmd = f"pdfseparate {file} sep/slides_%d.pdf"
print(cmd)
subprocess.run(cmd.split())

ls = subprocess.Popen(('ls', 'sep'), stdout=subprocess.PIPE)
no_pages = int(subprocess.check_output(("wc", "-l"), stdin=ls.stdout))

s = ""

for i in range(1,no_pages+1):
    s += f"notesslide.pdf sep/slides_{i}.pdf "

cmd = f"pdfunite {s} out/combined.pdf"
subprocess.run(cmd.split())

cmd = f"pdflatex --output-directory=out combine.tex"
subprocess.run(cmd.split())
cmd = f"gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/default -sOutputFile={new_name} out/combine.pdf"
subprocess.run(cmd.split())
