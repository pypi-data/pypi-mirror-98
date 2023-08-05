from AIH_SDK.AIHClient import AIHClient
from AIH_SDK.v2.v2Object import v2Object


class Equipment(v2Object):
    
    def __init__(self, id:str=None):
        super().__init__()
        
        self._api = 'assets'
        self._endpoint = 'equipment'
        
        if id:
            self.get(id)

        
            
        
    