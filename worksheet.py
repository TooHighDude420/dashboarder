import Modules.home
import Modules.officialmodule

class Plugin:
    def get_name(self):
        return __name__.replace('Modules.', '')
    
    def __init__(self):
        print('init testclass')
        
    def test_function(self):
        pass