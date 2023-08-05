from AIH_SDK.v2.v2Object import v2Object


class MainSystem(v2Object):
    
    def __init__(self, id:str=None):
        super().__init__()
        
        self._api = 'assets'
        self._endpoint = 'mainsystems'
        
        if id:
            self.get(id)
    
    
        
            
        
    