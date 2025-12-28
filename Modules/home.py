from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from example import ImageTileViewer

import settings

class Widget(QWidget):
    ACTIONS = {}
    
    def __init__(self, parent=None, **kwargs):
        super(Widget, self).__init__(parent)

        items = kwargs["items"]
        self.menu_widget = QListWidget()
        
        for key, val in items.items():
            item = QListWidgetItem(f"{val.get_name()}")
            self.ACTIONS[val.get_name()] = val.action
            item.setTextAlignment(Qt.AlignCenter)
            self.menu_widget.addItem(item)    

        content_layout = QVBoxLayout()
        images = []
        
        for image in settings.IMAGE_DIR.iterdir():
            images.append(image)

        main_widget = QWidget()
        main_stack = QStackedWidget()
        imageHandle = ImageTileViewer(images)
        main_stack.addWidget(imageHandle)
        content_layout.addWidget(main_stack)
        main_widget.setLayout(content_layout)

        layout = QHBoxLayout(self)
        layout.addWidget(self.menu_widget, 1)
        layout.addWidget(main_widget, 4)
        
        self.setLayout(layout)
        self.menu_widget.currentItemChanged.connect(self.on_item_changed)

    def on_item_changed(self, current, _):
        action = self.ACTIONS.get(current.text())
        if action:
            action()

def get_name():
    return __name__.replace('Modules.', '')