import os
from datetime import datetime, timedelta
from PyPDF2 import PdfReader, PdfWriter
from changeMetaD import change_metadata_in_directory, change_pdf_metadata

def merge_pdfs(first_page_folder, template_pdf_path, output_folder, output_folder_MD, creation_date):
    # Read the template PDF (2-3 pages)
    template_reader = PdfReader(template_pdf_path)

    # List all PDFs in the first page folder
    first_page_pdfs = [f for f in os.listdir(first_page_folder) if f.endswith('.pdf')]
    count = 0;

    # Process each PDF in the first page folder
    for pdf_file in first_page_pdfs:
        # Create a PdfReader for the first page PDF
        first_page_pdf_path = os.path.join(first_page_folder, pdf_file)
        first_page_reader = PdfReader(first_page_pdf_path)

        # Create a PdfWriter to merge PDFs
        pdf_writer = PdfWriter()

        # Add the first page from the first page PDF
        pdf_writer.add_page(first_page_reader.pages[0])  # Assumes the first page is the one to use

        # Add all pages from the template PDF
        for page_num in range(1, len(template_reader.pages)):
            pdf_writer.add_page(template_reader.pages[page_num])

        # Define the output PDF path (same name as the first page PDF)
        output_pdf_path = os.path.join(output_folder, pdf_file)

        # Write the merged PDF to the output folder
        with open(output_pdf_path, "wb") as output_file:
            pdf_writer.write(output_file)
        # Metadata change here
        file = os.path.join(output_folder, pdf_file)
        output_pdf = os.path.join(output_folder_MD, pdf_file)
        change_pdf_metadata(file, output_pdf, creation_date)
        #print(f"Merged {pdf_file} and saved to {output_pdf}")
        count += 1

    print(f"Merged {count} PDFs")

if __name__ == "__main__":
    # Metadata change
    start_date = datetime(2024, 11, 27)  # Example start date
    # Define the folders and template path
    first_page_folder = './firstPageDocs/'
    template_pdf_path = './templatePDFDocs/template.pdf'
    output_folder = './results'
    output_folder_MD = './results_MD/'

    # Make sure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Call the function to merge PDFs

    #end_date = datetime(2024, 11, 3)  # Example end date
    offset_minutes = 5  # Example offset between consecutive timestamps
    merge_pdfs(first_page_folder, template_pdf_path, output_folder, output_folder_MD, start_date)

    #change_metadata_in_directory(output_folder, "random", start_date, end_date, offset_minutes)
