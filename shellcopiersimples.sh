#!/bin/bash

# Directory containing the PDF files
PDF_DIR="/home/brpl/od-seeds"
# Directory where the text files will be saved
TXT_DIR="/home/brpl/od-seeds"

# Create the output directory if it doesn't exist
mkdir -p "$TXT_DIR"

# Loop through all PDF files in the specified directory
for pdf_file in "$PDF_DIR"/*.pdf; do
    # Extract the base name of the PDF file (without directory and extension)
    base_name=$(basename "$pdf_file" .pdf)
    # Convert the PDF to a text file
    pdftotext "$pdf_file" "$TXT_DIR/$base_name.txt"
done

echo "Conversion completed!"
