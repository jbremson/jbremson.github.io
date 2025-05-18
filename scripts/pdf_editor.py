from PyPDF2 import PdfReader, PdfWriter


def delete_page_two(input_pdf, output_pdf):
    # Open the input PDF
    reader = PdfReader(input_pdf)

    # Create a PDF writer object
    writer = PdfWriter()

    # Check if PDF has at least 2 pages
    if len(reader.pages) < 2:
        print("Error: PDF has fewer than 2 pages.")
        return

    # Add all pages except page 2 (index 1)
    for i in range(len(reader.pages)):
        if i != 1:  # Skip page 2
            writer.add_page(reader.pages[i])

    # Write the output PDF
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)
    print(f"Page 2 removed. New PDF saved as {output_pdf}")


# Example usage
input_pdf = "/Users/jbremson/Downloads/bremson_autopia_dissertation.pdf"  # Replace with your PDF file path
output_pdf = "../docs/bremson_autopia_dissertation.pdf"
delete_page_two(input_pdf, output_pdf)