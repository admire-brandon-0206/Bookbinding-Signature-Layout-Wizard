"""
This program takes a pdf and outputs a new pdf with the pages rearranged for bookbinding in the working directory.

The program has 2 required arguments:
1) number of signatures
2) path to input pdf

This program has the following optional arguments
-h : help
-o : output path

"""

import sys, getopt, PyPDF2
from math import ceil

def main(argv):
    """Driver code for program."""

    # Parse arguments
    input_file = ''
    output_file = './output.pdf'
    sig_num = 0
    try:
        opts, args = getopt.getopt(argv, "hoi:n:")
    except getopt.GetoptError:
        print("Invalid arguments, -h for help.")
        sys.exit(2)
    except ValueError:
        print("Not enough arguments! -h for help.")
    for opt, arg in opts:
        if opt == '-h':
            print("--PDF SIGNATURE CREATOR--\n\n\
This program takes a PDF as input and rearranges and outputs the pdf into\n\
signatures for bookbinding purposes. Blank pages are added at the end of the\n\
document to create even signatures.\n\n\
This program has the following optional arguments\n\
-i : input \n\
-o : output path \n\
-n : Number of signatures to split document into.")
            sys.exit()
        elif opt == '-i':
            input_file = arg
        elif opt == '-o':
            output_file = arg
        elif opt == '-n':
            try:
                sig_num = int(arg)
            except ValueError:
                print("The number of signatures must be a whole number.")
                sys.exit(2)

    # Initialize the PyPDF2 objects
    pdf = PyPDF2.PdfFileReader(input_file)
    output = PyPDF2.PdfFileWriter()

    # Calculate pages per signature
    pages = ceil(pdf.getNumPages()/sig_num)
    # Round up to the nearest multiple of 4
    pages = int(4 * ceil(pages/4))

    # Get dimensions for filler page
    _,_, w, h = pdf.getPage(1)['/MediaBox']
    
    # Prepare output doc
    for j in range(sig_num):
        for i in range(int(pages/2)):
            # Get original pages
            try:
                left = pdf.getPage((i)+(j*pages))
            except IndexError:
                left = PyPDF2.pdf.PageObject.createBlankPage(width =w,height=h)
            try:
                right = pdf.getPage((pages-i)+(j*pages))
            except IndexError:
                right = PyPDF2.pdf.PageObject.createBlankPage(width =w,height=h)


            # Merge pages into one
            left.mergeTranslatedPage(right, left.mediaBox.getUpperRight_x(),0, True)

            # Add page to output
            output.addPage(left)


    # Write output
    with open(output_file, "wb") as target:
        output.write(target)


if __name__ == "__main__":
    main(sys.argv[1:])