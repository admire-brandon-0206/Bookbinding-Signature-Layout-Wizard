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


def getUserInput(argv):
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
            print(
                """
                --PDF SIGNATURE CREATOR--
                This program takes a PDF as input and rearranges and outputs the pdf into\n\
                signatures for bookbinding purposes. Blank pages are added at the end of the\n\
                document to create even signatures.
                This program has the following optional arguments
                -i : input 
                -o : output path
                -n : Number of signatures to split document into.
                """
            )
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
    
    return input_file,output_file,sig_num


def pageCalc(sig_num,pdf_object):
    """Calculate and return pages per signature."""

    pages = ceil(pdf_object.getNumPages()/sig_num)
    # Round up to the nearest multiple of 4. All new pages will consist of 
    # 4 of the original, 2 on each side. So the signatures need to be split into
    # exact multiples of 4.
    pages = int(4 * ceil(pages/4))
    # Print out
    print("")
    return pages


def buildOutput(pdf_object,output_object, pages, sig_num):
    """Build output for write"""

    # Get dimensions for filler pages
    _,_, w, h = pdf_object.getPage(1)['/MediaBox']

    for j in range(sig_num):
        for i in range(int(pages/2)):
            # Get original pages
            try:
                left = pdf_object.getPage((i)+(j*pages))
            except IndexError:
                left = PyPDF2.pdf.PageObject.createBlankPage(width =w,height=h)
            try:
                right = pdf_object.getPage((pages-i)+(j*pages))
            except IndexError:
                right = PyPDF2.pdf.PageObject.createBlankPage(width =w,height=h)


            # Merge pages into one
            left.mergeTranslatedPage(right, left.mediaBox.getUpperRight_x(),0, True)

            # Add page to output
            output_object.addPage(left)


def main(argv):
    in_path, out_path, sig_num = getUserInput(argv)
    print("Program started....")
    # Initialize the PyPDF2 objects
    pdf = PyPDF2.PdfFileReader(in_path)
    output = PyPDF2.PdfFileWriter()

    pages = pageCalc(sig_num, pdf)
    print(f"There will be {pages} pages per signature!")
    buildOutput(pdf,output,pages,sig_num)

    with open(out_path, "wb") as target:
        output.write(target)
    print(f"Job complete! File saved to: {out_path}")



if __name__ == "__main__":
    main(sys.argv[1:])
