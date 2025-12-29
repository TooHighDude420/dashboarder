from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import settings

class Widget(QWidget):
    ACTIONS = {}
    
    def __init__(self, parent=None, **kwargs):
        super(Widget, self).__init__(parent)

        items = kwargs["items"]
        widgets = kwargs["widgets"]
        self.menu_widget = QListWidget()
        
        for key, val in items.items():
            item = QListWidgetItem(f"{val.get_name()}")
            self.ACTIONS[val.get_name()] = val.action
            item.setTextAlignment(Qt.AlignCenter)
            self.menu_widget.addItem(item)
            
        for key, val in widgets.items():
            if (hasattr(val, "action")  and hasattr(val, "get_name")):
                item = QListWidgetItem(f"{val.get_name()}")
                self.ACTIONS[val.get_name()] = val.action
                item.setTextAlignment(Qt.AlignCenter)
                self.menu_widget.addItem(item)
            else:
                print(f"Module {key} has no action/get_name")
                
        self.content_layout = QVBoxLayout()
        images = []
        
        for image in settings.IMAGE_DIR.iterdir():
            images.append(image)

        self.main_widget = QWidget()
        self.main_stack = QStackedWidget()
        self.content_layout.addWidget(self.main_stack)
        self.main_widget.setLayout(self.content_layout)

        self.lay = QHBoxLayout(self)
        self.lay.addWidget(self.menu_widget, 1)
        self.lay.addWidget(self.main_widget, 4)
        
        self.setLayout(self.lay)
        self.menu_widget.currentItemChanged.connect(self.on_item_changed)

    def on_item_changed(self, current, _):
        action = self.ACTIONS.get(current.text())
        if action:
            res = action()

            print(res, type(res))
            
            if isinstance(res, QWidget):
                self.main_stack.addWidget(res)
                self.main_stack.setCurrentWidget(res)


def get_name():
    return __name__.replace('Modules.', '')