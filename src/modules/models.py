import numpy as np

class Models:
    def binary(u,v,ofset,DM21,x2,y2):
        DI2 = 10**(-0.4*DM21)
        #x1 = 0; y1 = 0
        result = ofset**2*(1 + DI2**2 + 2*DI2*np.cos(2*np.pi*(v*x2 + u*y2)))
        return result

    def triple(u,v,ofset,DM21,DM31,x2,y2,x3,y3):
        DI2 = 10**(-0.4*DM21)
        DI3 = 10**(-0.4*DM31)
        #x1 = 0; y1 = 0
        result = ofset**2*(1 + DI2**2 + DI3**2 +\
        2*DI2*np.cos(2*np.pi*(v*x2 + u*y2)) +\
        2*DI3*np.cos(2*np.pi*(v*x3 + u*y3)) +\
        2*DI2*DI3*np.cos(2*np.pi*(v*(x2-x3) + u*(y2-y3))))
        return result
