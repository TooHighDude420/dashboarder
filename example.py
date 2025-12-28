import sys, os, settings, json

from pathlib import Path
from Modules import officialmodule
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class ImageTileViewer(QWidget):
    def __init__(self, image_files):
        super().__init__()

        if not image_files:
            raise ValueError("The list of image files cannot be empty.")

        self.columns = 4
        self.row = self.col = 0
        self.official = officialmodule.Plugin()
        self.make_meta()        
        self.image_files = image_files
        self.init_ui()
        self.load_from_meta()

    def make_meta(self):
        self.metadata_path = settings.ROOT_DIR / "ModuleData" / "example"
        if not os.path.exists(self.metadata_path):
            os.makedirs(self.metadata_path, exist_ok=True)
            
            with open(self.metadata_path / "metadata.json", mode="w") as metadata:
                metadata.write("""
                    {\n
                    \t"module-name":"example",\n
                    \t"execs":{\n
                    \t}\n
                    \n}"""
                    )
                metadata.close()
        
        with open(self.metadata_path / "metadata.json", "r", encoding="utf-8") as f:
            metaData = json.load(f)
        
        self.metadata = metaData

    def write_to_meta(self, **kwargs):
        qurl = QUrl.fromLocalFile(kwargs['path'])
        icon = kwargs['icon']
        self.metadata["execs"][kwargs["name"]] = {"exe":f"{qurl}", "img":f"{icon}"}
        
        with open(self.metadata_path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=4)

    def load_from_meta(self):
        if len(self.metadata["execs"]) > 0:
            for name, items in self.metadata["execs"].items():
                exe_path = items.get("exe")
                img_path = items.get("img")
                
                exe_path = QUrl(exe_path)
                
                self.dyn_tile(exe_path, name=name, img=img_path)
                    
    def launch_add_app(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file",
            "",
            "All Files (*);;Images (*.png *.jpg *.jpeg)"
        )

        if file_path:
            self.dyn_tile(file_path)

    def get_img_from_url(self, url_path):
        from configparser import ConfigParser
        
        config = ConfigParser()
        config.read(url_path, encoding="utf-8")

        # Get the icon file path
        icon_file = config.get("InternetShortcut", "IconFile", fallback=None)
        icon_index = config.getint("InternetShortcut", "IconIndex", fallback=0)
        
        return icon_file
        
    
    def dyn_tile(self, file_path, **kwargs):
        if type(file_path) is str:
            tmp_path = Path(file_path)
            icon_file = self.get_img_from_url(tmp_path)
            tmp_name = tmp_path.stem
            tmp_action = lambda event: QDesktopServices.openUrl(QUrl(QUrl.fromLocalFile(file_path)))

            tmp_tile = self.create_tile(icon_file, tmp_name, tmp_action)
            self.add_to_grid(tmp_tile)
            self.write_to_meta(name=tmp_name, path=file_path, icon=icon_file)
        else:
            tmp_name = kwargs['name']
            tmp_image = kwargs['img']
            tmp_action = lambda event: QDesktopServices.openUrl(file_path)

            tmp_tile = self.create_tile(tmp_image, tmp_name, tmp_action)
            self.add_to_grid(tmp_tile)

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        
        self.filehandle_widget = QWidget()

        self.filehandle_layout = QHBoxLayout(self.filehandle_widget)
        self.filehandle_layout.setAlignment(Qt.AlignCenter)

        self.official.register_button(self.filehandle_layout, "Add App!", self.launch_add_app)
        
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(10)
        
        self.main_layout.addWidget(self.grid_widget)
        self.main_layout.addWidget(self.filehandle_widget)

    def add_to_grid(self, *widgets):
        for widget in widgets:
            self.grid_layout.addWidget(widget, self.row, self.col)

            self.col += 1
            if self.col >= self.columns:
                self.col = 0
                self.row += 1

    def create_tile(self, image_path: str, text: str, luanch) -> QWidget:
        tile = QWidget()

        layout = QVBoxLayout(tile)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(4)

        image_label = QLabel()
        
        if type(image_path) is not str:
            image_path = image_path.toLocalFile() 
        
        if Path(image_path).suffix == ".ico":
            icon = QIcon(image_path)
            image_label.setPixmap(
                icon.pixmap(128, 128)
            )
        else:
            pixmap = QPixmap(image_path)
            image_label.setPixmap(
                pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            
        image_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        
        image_label.mouseDoubleClickEvent = luanch
        layout.addWidget(image_label)
        layout.addWidget(text_label)

        return tile