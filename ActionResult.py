class ActionResult :
    def __init__(self, payload:any, type:str='View', code:int=200 ):
        self.type       = type
        self.payload    = payload
        self.code       = code