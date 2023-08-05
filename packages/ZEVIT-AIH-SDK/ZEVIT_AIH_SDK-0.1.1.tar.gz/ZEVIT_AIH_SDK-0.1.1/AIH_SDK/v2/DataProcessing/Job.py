from AIH_SDK.v2.v2Object import v2Object


class Job(v2Object):
    
    def __init__(self):
        super().__init__()
        self._api = 'dp'
        self._endpoint = 'Jobs'