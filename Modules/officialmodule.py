from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout

class Plugin():
    def get_name(self):
        return __name__.replace('Modules.', '')
    
    def register_button(self, layout, text, function=None, **kwargs):
        tmpbutton = QPushButton(f"{text}")
        
        if function and len(kwargs) > 0:
            tmpbutton.clicked.connect(lambda: function(**kwargs))
        elif function:
            tmpbutton.clicked.connect(function)
        
        layout.addWidget(tmpbutton)  
        
    def read_from_css(self, path, cssclass):
        with open(path, mode='r') as handle:
            classcont = ""
            found = False

            for line in handle:
                if '}' in line:
                    break
                
                if found:
                    classcont += line + "\n"
                
                if cssclass in line:
                    found = True
                                         
        return classcont
    
    def action(self):
        print(f"action {self.get_name()} executed")