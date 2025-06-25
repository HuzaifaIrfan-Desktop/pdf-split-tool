from pdf_tools import split_pdf_by_size

def main():
    print("Hello from pdf-split-tool!")
    
    input_dir = "input"
    filename="Arabic for Young Learners - Pupil Book 1.pdf"
    filename_without_extension = filename.split('.')[0]
    filepath = f"{input_dir}/{filename}"
    print(f"Splitting PDF: {filepath}")
    
    output_dir=f"output/{filename_without_extension}"
    output_filename_prefix = filename_without_extension + "_"
    # Example usage:
    split_pdf_by_size(filepath, 5, output_filename_prefix , output_dir)  # Split into ~5MB chunks


if __name__ == "__main__":
    main()
