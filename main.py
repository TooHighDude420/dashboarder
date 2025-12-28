import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QApplication, QPushButton, QWidget, QVBoxLayout
from pathlib import Path
from PySide6.QtWidgets import QStackedWidget
import inspect, importlib, os
import settings

MODULES_REFS = {}
LOADED_CLASSES = {}
LOADED_WIDGETS = {}

#load modules and store refrences for seprate use
def load_modules():
    loaded = []

    for file in settings.MODULES_DIR.iterdir():
        if file.suffix == ".py" and file.name != "__init__.py":
            module_name = f"Modules.{file.stem}"
            module = importlib.import_module(module_name)
            MODULES_REFS[file.stem] = module
            loaded.append(module)
            print("Loaded:", module_name)

    for module in loaded:
        if inspect.getmembers(module, inspect.isclass):
            try:
                tmp_ref = module.Plugin()
                LOADED_CLASSES[tmp_ref.get_name()] = tmp_ref
            except:
                LOADED_WIDGETS[module.get_name()] = module
                
        elif hasattr(module, "main"):
            module.main()
        else:
            raise RuntimeError("Invalid plugin")
        
def check_sheet(regen=None):
    worksheet = Path(settings.ROOT_DIR) / "worksheet.py"
    
    if not worksheet.exists() or regen:
        modlist = []
        for module in settings.MODULES_DIR.iterdir():
            if module.suffix == ".py" and module.name != "__init__.py":
               module_name = f"Modules.{module.stem}"
               modlist.append(module_name)
        
        with open(worksheet, mode='w') as handle:
            for mod in range(len(modlist)):
                handle.write(f"import {modlist[mod]}\n")
            
            template = "\n" \
            "#to register a module use main\n" \
            "\n" \
            "#def main():\n" \
            "#   print('loaded')\n" \
            "\n" \
            "#to register a class use the class, it MUST be named Plugin for now\n" \
            "#it also MUST have get_name\n" \
            "\n" \
            "#class Plugin:\n" \
            "#\tdef get_name(self):\n" \
            "#\t\treturn __name__.replace('Modules.', '')\n" \
            "\n" \
            "#\tdef __init__(self):\n" \
            "#\t\tprint('init testclass')"
            handle.write(template)
            handle.close()
    
def show_widget(stack, widget_cls):
    widget = widget_cls(items=LOADED_CLASSES)
    stack.addWidget(widget)
    stack.setCurrentWidget(widget)
    
def main():    
    load_modules()
    
    check_sheet()
    
    official = LOADED_CLASSES["officialmodule"]

    app = QApplication([])
    
    screen = app.primaryScreen()
    
    SCREEN_HEIGHT = screen.size().height()
    SCREEN_WIDTH = screen.size().width()
    
    stack = QStackedWidget()

    window = QWidget()
    window.setMaximumHeight(SCREEN_HEIGHT)
    window.setMaximumWidth(SCREEN_WIDTH)
    window.showMaximized()
    window.setWindowTitle("Main app")
    
    layout = QVBoxLayout(window)
    layout.addWidget(stack)

    home_widget = LOADED_WIDGETS["home"].Widget
    
    show_widget(stack, home_widget)
    # official.register_button(layout,"widget test",show_widget,stack=stack,widget_cls=LOADED_WIDGETS["home"].Widget)

    window.show()
    
    app.exec()

main()