import numpy as np

class Grid:
    def __init__(self,size=512):
        self.size = size

    def uv_meshgrid(self):
        U = np.arange(0,self.size)/self.size - 0.5
        V = np.arange(0,self.size)/self.size - 0.5
        u,v = np.meshgrid(U,V)
        return u,v
