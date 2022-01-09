class Agent:
    def __init__(self , id:int , value:float , src:int , dest:int , speed:float , pos:tuple):
        self.id = id
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self.pos = pos