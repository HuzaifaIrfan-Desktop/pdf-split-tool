from pdf_tools import split_pdf_by_size
from pathlib import Path

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog,
    QSpinBox, QHBoxLayout
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
        self.select_button = QPushButton("Select PDF File")
        self.select_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_button)
        
        # File size limit input
        self.size_layout = QHBoxLayout()
        self.size_label = QLabel("PDF Part Size limit (MB):")
        self.size_input = QSpinBox()
        self.size_input.setRange(1, 10000)  # 1MB to 10GB
        self.size_input.setValue(5)  # default value
        self.size_layout.addWidget(self.size_label)
        self.size_layout.addWidget(self.size_input)
        self.layout.addLayout(self.size_layout)

        # Button to run processing function
        self.run_button = QPushButton("Split PDF")
        self.run_button.clicked.connect(self.run_function)
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)
        self.file_path = None

    def select_file(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getOpenFileName(self,  "Select PDF file", "",  "PDF File (*.pdf)")
        if path:
            self.file_path = path
            self.label.setText(f"Selected: {path}")
        else:
            self.label.setText("No file selected")

    def run_function(self):
        if self.file_path:
                    # Get value from the spin box
            file_size_limit_mb = self.size_input.value()
            
            result = self.process_file(self.file_path, file_size_limit_mb)
            self.label.setText(f"Processed: {result}")
        else:
            self.label.setText("Please select a file first.")

    def process_file(self, filepath, file_size_limit_mb=5):
            
        # filepath = "input/Arabic for Young Learners - Pupil Book 1.pdf"
        path = Path(filepath)
        filename = path.name # e.g., "file.pdf"
        extension = path.suffix  # e.g., ".pdf"
        filename_without_extension = path.stem  # e.g., "file"
        
        print(f"Splitting PDF: {filepath}")
        
        output_dir=f"output/{filename_without_extension}"
        output_filename_prefix = filename_without_extension + "_"
        # Example usage:
        split_pdf_by_size(filepath, file_size_limit_mb, output_filename_prefix , output_dir)  # Split into ~5MB chunks
        print(f"PDF split into chunks in {output_dir}")
        
        return f"PDF split into chunks in {output_dir}"

def main():
    print("Hello from pdf-split-tool!")
    app = QApplication(sys.argv)
    window = FileProcessorApp()
    window.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()