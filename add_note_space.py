#! /usr/bin/python3

from PyPDF2 import PdfFileReader, PdfFileWriter
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Generate a note-taking pdf from a slide deck')
parser.add_argument("-i", "--input", help="input file", required=True)
parser.add_argument("-o", "--output", help="output file", required=True)

args = parser.parse_args()

file = args.input
new_name = args.output

# open the input pdf 
pdf = PdfFileReader(file)
template = PdfFileReader("notesslide.pdf")
new_pdf = PdfFileWriter()

# paginate the pdf
for page in range(pdf.getNumPages()):
    # get the page
    p = pdf.getPage(page)
    # add the page to the new pdf
    new_pdf.addPage(p)
    # add the notes template
    new_pdf.addPage(template.getPage(0))

# write the new pdf
with open(new_name, "wb") as f:
    new_pdf.write(f)

cmd = f"pdflatex --output-directory=out combine.tex"
subprocess.run(cmd.split())
cmd = f"gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/default -sOutputFile={new_name} out/combine.pdf"
subprocess.run(cmd.split())