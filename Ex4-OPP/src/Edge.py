class Edge:
    def __init__(self , src:int , dst:int , w:float):
        self.src = src
        self.dst = dst
        self.w = w

    def getKey(self):
        return (self.src , self.dst)

    def getSrc(self):
        return self.src

    def getDst(self):
        return self.dst

    def getWeight(self):
        return self.w
