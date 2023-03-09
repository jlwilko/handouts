#! /usr/bin/python3

from pikepdf import Pdf
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Generate a note-taking pdf from a slide deck')
parser.add_argument("-i", "--input", help="input filename", required=True)
parser.add_argument("-o", "--output", help="output filename", required=True)

args = parser.parse_args()

input_file: str = args.input
output_file: str = args.output

# open the input pdf 
pdf = Pdf.open(input_file)
template = Pdf.open("notesslide.pdf")
lines_page = template.pages[0]
combined_pdf = Pdf.new()

# paginate the pdf
for i, page in enumerate(pdf.pages):
    # add the notes template
    combined_pdf.pages.append(lines_page)
    # add the page to the new pdf
    combined_pdf.pages.append(page)

# write the new pdf
combined_pdf.save(output_file)

cmd = f"pdflatex --output-directory=out combine.tex"
subprocess.run(cmd.split())
cmd = f"gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/default -sOutputFile={output_file} out/combine.pdf"
subprocess.run(cmd.split())