from pdf_tools import split_pdf_by_size

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog
)

class FileProcessorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Split Tool")

        self.layout = QVBoxLayout()

        # Label to show selected file
        self.label = QLabel("No file selected")
        self.layout.addWidget(self.label)

        # Button to select file
        self.select_button = QPushButton("Select File")
        self.select_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_button)

        # Button to run processing function
        self.run_button = QPushButton("Split PDF")
        self.run_button.clicked.connect(self.run_function)
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)
        self.file_path = None

    def select_file(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getOpenFileName(self, "Open File")
        if path:
            self.file_path = path
            self.label.setText(f"Selected: {path}")
        else:
            self.label.setText("No file selected")

    def run_function(self):
        if self.file_path:
            result = self.process_file(self.file_path)
            self.label.setText(f"Processed: {result}")
        else:
            self.label.setText("Please select a file first.")

    def process_file(self, path, file_size_limit_mb=5):
        # Replace this with your actual function logic
        # with open(path, "r", encoding="utf-8", errors="ignore") as f:
        #     return f"Length: {len(f.read())} chars"
        
            
        # filepath = "input/Arabic for Young Learners - Pupil Book 1.pdf"
        filepath = path
        
        filename= filepath.split('/')[-1]
        filename_without_extension = filename.split('.')[0]
        
        print(f"Splitting PDF: {filepath}")
        
        output_dir=f"output/{filename_without_extension}"
        output_filename_prefix = filename_without_extension + "_"
        # Example usage:
        split_pdf_by_size(filepath, file_size_limit_mb, output_filename_prefix , output_dir)  # Split into ~5MB chunks

        return f"PDF split into chunks in {output_dir}"

def main():
    print("Hello from pdf-split-tool!")
    app = QApplication(sys.argv)
    window = FileProcessorApp()
    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()