import numpy as np

class Models:
    def binary(u,v,I1,dm21,x2,y2):
        DI2 = 10**(-0.4*dm21)
        result = I1**2*(1 + DI2**2 + 2*DI2*np.cos(2*np.pi*(v*x2 + u*y2)))
        return result

    def binary_fix_dm(u,v,dm21,I1,x2,y2):
        DI2 = 10**(-0.4*dm21)
        result = I1**2*(1 + DI2**2 + 2*DI2*np.cos(2*np.pi*(v*x2 + u*y2)))
        return result

    def binary_fix_xy(u,v,x2,y2,I1,dm21):
        DI2 = 10**(-0.4*dm21)
        result = I1**2*(1 + DI2**2 + 2*DI2*np.cos(2*np.pi*(v*x2 + u*y2)))
        return result

    def triple(u,v,I1,dm21,x2,y2,dm31,x3,y3):
        DI2 = 10**(-0.4*dm21)
        DI3 = 10**(-0.4*dm31)
        result = I1**2*(1 + DI2**2 + DI3**2 +\
        2*DI2*np.cos(2*np.pi*(v*x2 + u*y2)) +\
        2*DI3*np.cos(2*np.pi*(v*x3 + u*y3)) +\
        2*DI2*DI3*np.cos(2*np.pi*(v*(x2-x3) + u*(y2-y3))))
        return result


