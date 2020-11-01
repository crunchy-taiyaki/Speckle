
class BinaryInitialParameters:

    def __init__(self,dm21,x2,y2):
        self.I1 = None
        self.dm21 = dm21
        self.x2 = x2
        self.y2 = y2

    def array(self):
        return np.array([self.I1,self.dm21,self.x2,self.y2])


class TripleInitialParameters:

    def __init__(self,dm21,x2,y2,dm31,x3,y3):
        self.I1 = None
        self.dm21 = dm21
        self.x2 = x2
        self.y2 = y2
        self.dm31 = dm31
        self.x3 = x3
        self.y3 = y3

    def array(self):
        return np.array([self.I1,self.dm21,self.x2,self.y2,self.dm31,self.x3,self.y3])