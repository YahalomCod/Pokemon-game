class Node:
    def __init__(self , id:int , pos:tuple = None):
        self.id = id
        self.pos = pos

    def getId(self) -> int:
        return self.id

    def getPos(self) -> tuple:
        return self.pos

    def __repr__(self):
        return "ID :"f"{self.id}"