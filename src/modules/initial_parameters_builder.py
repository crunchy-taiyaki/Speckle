import numpy as np

class BinaryInitialParameters:

    def __init__(self,dm21,x2,y2):
        self.I1 = None
        self.dm21 = dm21
        self.x2 = x2
        self.y2 = y2

    def array(self):
        return np.array([self.I1,self.dm21,self.x2,self.y2])

class BinaryInitialParametersFixDM:

    def __init__(self,x2,y2):
        self.I1 = None
        self.x2 = x2
        self.y2 = y2

    def array(self):
        return np.array([self.I1,self.x2,self.y2])

class BinaryInitialParametersFixXY:

    def __init__(self,dm21):
        self.I1 = None
        self.dm21 = dm21

    def array(self):
        return np.array([self.I1,self.dm21])

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

class TripleInitialParametersFixDM:

    def __init__(self,dx2,y2,dx3,y3):
        self.I1 = None
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3

    def array(self):
        return np.array([self.I1,self.x2,self.y2,self.x3,self.y3])

class TripleInitialParametersFixXY:

    def __init__(self,dm21,dm31):
        self.I1 = None
        self.dm21 = dm21
        self.dm31 = dm31

    def array(self):
        return np.array([self.I1,self.dm21,self.dm31])