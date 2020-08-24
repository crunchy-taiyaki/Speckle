class FinalFitParameters():
    def __init__(self,flag):
        self.flag = flag
        self.dm21 = None        
        self.x2 = None        
        self.y2 = None        
        self.dm31 = None
        self.x3 = None
        self.y3 = None

        self.dm21_er = None
        self.x2_er = None
        self.y2_er = None
        self.dm31_er = None
        self.x3_er = None
        self.y3_er = None

    def print_values(self):
        print('---------------final results-----------------')
        print('dm21=',self.dm21,'+-',self.dm21_er,'[m]')
        print('x2=',self.x2,'+-',self.x2_er, '[px]')
        print('y2=',self.y2,'+-',self.y2_er, '[px]')
        if (self.flag == 'triple'):
            print('dm31=',self.dm31,'+-',self.dm31_er,'[m]')
            print('x3=',self.x3,'+-',self.x3_er, '[px]')
            print('y3=',self.y3,'+-',self.y3_er, '[px]')
