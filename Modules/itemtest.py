class Plugin:
    def get_name(self):
        return __name__.replace('Modules.', '')
    
    def __init__(self):
        print('init testclass')
        
    def action(self):
        print(f"action {self.get_name()} executed")