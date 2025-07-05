from pdf_tools import split_pdf_by_size

from pathlib import Path            
import os
import sys

from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread


# Worker class to run in background
class SplitWorker(QObject):
    finished = pyqtSignal()
    message = pyqtSignal(str)

    def __init__(self, file_path, file_size_limit_mb):
        super().__init__()

        self.file_path=file_path
        self.file_size_limit_mb=file_size_limit_mb
    
        # file_path = "input/Arabic for Young Learners - Pupil Book 1.pdf"
        path = Path(file_path)
        filename = path.name # e.g., "file.pdf"
        extension = path.suffix  # e.g., ".pdf"
        filename_without_extension = path.stem  # e.g., "file"
        
        self.output_dir=f"output/{filename_without_extension}"
        self.output_filename_prefix = filename_without_extension + "_"

        

    @pyqtSlot()
    def run(self):
        split_pdf_by_size(self.file_path, self.file_size_limit_mb, self.output_filename_prefix , self.output_dir, progress_callback=self.message.emit)  # Split into ~5MB chunks
        
        self.message.emit(f"PDF split into chunks in {self.output_dir}")
        self.finished.emit()


class Backend(QObject):
    message = pyqtSignal(str)  # Signal to send messages to QML

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = ""

    @pyqtSlot()
    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_path = selected_files[0]
                self.message.emit(f"Selected file: {self.file_path}")
            else:
                self.message.emit("No file selected.")
        else:
            self.message.emit("File dialog canceled.")

    @pyqtSlot(int)
    def run(self, file_size_limit_mb):
        if not self.file_path:
            self.message.emit("No file selected. Please select a file first.")
            return
        
    
        # Set up the thread and worker
        self.thread = QThread()
        self.worker = SplitWorker(
            file_path=self.file_path,
            file_size_limit_mb=file_size_limit_mb
        )
        self.worker.moveToThread(self.thread)

        self.worker.message.connect(self.message.emit)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.message.emit(f"Splitting file: {self.file_path} with file size limit: {file_size_limit_mb}")
        
        self.thread.started.connect(self.worker.run)
        self.thread.start()   


def main():
    print("Hello from pdf-split-tool!")

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)  # Expose to QML


    # Detect if we're in a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        qml_path = os.path.join(sys._MEIPASS, 'ui.qml')
    else:
        qml_path = os.path.join(os.path.dirname(__file__), 'ui.qml')
        
    engine.load(qml_path)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()