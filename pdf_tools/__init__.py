
from PyPDF2 import PdfReader, PdfWriter
import os



def split_pdf_by_size(input_pdf, max_size_mb, output_filename_prefix="part_", output_dir="output", progress_callback= lambda message : print(message)):
    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages)
    max_size_bytes = max_size_mb * 1024 * 1024

    os.makedirs(output_dir, exist_ok=True)

    start_page = 0
    part = 1

    while start_page < total_pages:
        writer = PdfWriter()
        current_size = 0
        end_page = start_page

        # Try adding pages until size exceeds
        while end_page < total_pages:
            writer.add_page(reader.pages[end_page])

            # Estimate file size in memory
            from io import BytesIO
            temp_stream = BytesIO()
            writer.write(temp_stream)
            current_size = temp_stream.tell()

            if current_size > max_size_bytes:
                # Remove last page that caused overflow
                writer = PdfWriter()
                for i in range(start_page, end_page):  # exclude end_page
                    writer.add_page(reader.pages[i])
                break

            end_page += 1

        # Write current part to disk
        part_path = os.path.join(output_dir, f"{output_filename_prefix}{part}.pdf")
        with open(part_path, "wb") as f:
            writer.write(f)

        actual_size_mb = os.path.getsize(part_path) / (1024 * 1024)
        progress_callback(f"    Created: ({actual_size_mb:.2f} MB, pages {start_page+1} to {end_page - 1 + 1}) {part_path}")

        start_page = end_page
        part += 1

        