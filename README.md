# PDF-Signature-Creator

This program takes in a PDF and rearragnes and outputs into signatures for bookbinding.

In bookbinding pages are split into mini-booklets called signatures that are then sewn together. Since the mini booklets each have a spine, layout of the pages by hand is difficult and prone to error, especially for larger projects. This program aims to automate the process and take human error out of the question.

The program requires a number of signatures to be entered. The correct number to enter will vary based on the thickness of your paper, the size of your book, and the size of paper. A rough estimate can be done by dividing the number of pages in your original document by the number of signatures, and then folding that many pages in half. They should fold realativly easily and lay mostly flat. If they want to bow out and do not sit reletivly flat, more signatures will be required. As a rule of thumb, less signatures is better, and more than 2-3 is recomended.

Each signature MUST be a multiple of 4, since there are 2 orignial pages per new page, and each new page will be front and back. The program adds blank pages to the document to handle this.

# Arguments

Required:
-i Input path, must be a PDF.
-n Number of signatures

Optional:
-o Output path, defaults to ".\output.pdf"

# Usage Example

PDF_Signature_Creator.py -i <path to original PDF> -n <number of signatures>
  
output:
"Program started...."
"There will be 12 pages per signature!"

Examples of input and output are in the repository.

TO DO:
------
-Add multi PDF support
-Add scaling and multiple paper size options. (Currenly handled by print dialoge)
