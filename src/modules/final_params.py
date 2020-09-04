import numpy as np
from initial_parameters import DataFiles
from fit import FitParameters, FitResult
from stats import ResultSample

class Coordinate():
    def __init__(self,x=None,y=None,x_er=None,y_er=None,\
                     paralactic_angle=None,paralactic_angle_er=None,\
                     scale=None,scale_er=None):
        self.x = x # [x] = 1px
        self.y = y # [y] = 1px
        self.alpha_in_px = None # [alpha] = 1 px
        self.delta_in_px = None # [beta] = 1 px
        self.alpha = None # [alpha] = 1 arcsec
        self.delta = None # [beta] = 1 arcsec
        self.r = None
        self.theta = None
        self.paralactic_angle = paralactic_angle # [paralactic_angle] = 1 radian
        self.scale = scale # [scale] = 1 arcsec/px
        #errors
        self.x_er = x_er
        self.y_er = y_er
        self.alpha_in_px_er = None
        self.delta_in_px_er = None
        self.alpha_er = None
        self.delta_er = None
        self.r_er = None
        self.theta_er = None
        self.paralactic_angle_er = paralactic_angle_er
        self.scale_er = scale_er

    def calc_equtorial(self):
        self.alpha_in_px = self.x*np.cos(self.paralactic_angle) - self.y*np.sin(self.paralactic_angle)
        self.delta_in_px = self.x*np.sin(self.paralactic_angle) + self.y*np.cos(self.paralactic_angle)
        self.alpha_in_px_er = np.sqrt(self.x_er**2*np.cos(self.paralactic_angle)**2+self.y_er**2*np.sin(self.paralactic_angle)**2 +
                                self.paralactic_angle_er**2*(self.x*np.sin(self.paralactic_angle)+self.y*np.cos(self.paralactic_angle))**2)
        self.delta_in_px_er = np.sqrt(self.x_er**2*np.sin(self.paralactic_angle)**2+self.y_er**2*np.cos(self.paralactic_angle)**2 +
                                self.paralactic_angle_er**2*(self.x*np.cos(self.paralactic_angle)-self.y*np.sin(self.paralactic_angle))**2)

        #calc alpha and delta in arcsec:
        self.alpha = self.alpha_in_px*self.scale
        self.alpha_er = np.sqrt(self.scale**2*self.alpha_in_px_er**2 + self.alpha**2*self.scale_er**2)
        self.delta = self.delta_in_px*self.scale
        self.delta_er = np.sqrt(self.scale**2*self.delta_in_px_er**2 + self.delta**2*self.scale_er**2)

    def calc_polar(self):
        self.r = np.sqrt(self.alpha**2 + self.delta**2)
        self.theta = (np.arctan2(self.delta,self.alpha))*180/np.pi
        #errors
        self.r_er = np.sqrt(self.alpha**2*self.alpha_er**2 + self.delta**2*self.delta_er**2)/self.r
        #theta error calculation
        part1 = 1./(1+(self.delta/self.alpha)**2)**2
        self.theta_er = (part1*np.sqrt(self.delta_er**2/self.alpha**2 + self.delta**2*self.alpha_er**2/self.alpha**2))*180/np.pi

    def read_input(self,file):
        info = []
        with open(file, 'r') as input:
            for line in input:
                text = line.strip()
                if text.startswith('#'):
                    continue
                info.append(text)
        info = [x if x!='-' else None for x in info] #exchange '-' to None
        self.scale = float(info[3])
        self.scale_er = float(info[4])
        return info

    def calc_paralactic_angle(self,angle_config_file):
        info = self.read_input(angle_config_file)
        pi = np.pi
        fi = float(info[0])*pi/180. # BTA latitude in radians
        nonhorizontality = float(info[1])*pi/180. # in radians
        nonhorizontality_er = float(info[2])*pi/180. # in radians
        ra_h = (float(info[5])+float(info[6]))/2 # mean right ascension hours
        ra_m = (float(info[7])+float(info[8]))/2 # mean right ascension minuts
        ra_s = (float(info[9])+float(info[10]))/2 # mean right ascension sec
        dec_d = (float(info[11])+float(info[12]))/2 # mean declination degrees
        dec_m = (float(info[13])+float(info[14]))/2 # mean declination minuts
        dec_s = (float(info[15])+float(info[16]))/2 # mean declination sec
        st_h = (float(info[17])+float(info[18]))/2 # mean sideric time hours
        st_m = (float(info[19])+float(info[20]))/2 # mean sideric time minuts
        s = st_h + st_m/60.
        r = ra_h + ra_m/60. + ra_s/(60.*60)
        if dec_d >=0.:
            d = (dec_d+dec_m/60. + dec_s/(60.*60.))*pi/180.
        else:
            d = -1*(np.abs(dec_d) + dec_m/60. + dec_s/(60.*60.))*pi/180.
        t = (s - r)*15.*pi/180.
        self.paralactic_angle = (np.arctan(np.sin(t)/(np.tan(fi)*np.cos(d) - np.sin(d)*np.cos(t)))) #in radian

        #paralactic angle's error calculation...
        fi_er = 0.0001*pi/180. #fi_er = 1e-4 deg
        d_er = 0.1*pi/(180*3600) #d_er = 0.1 arcsec
        s_er = 6.*pi/(180.*3600) #s_er = 6 arcsec
        r_er = pi/(180.*3600) #r_er = 1 arcsec 
        t_er = np.sqrt(s_er**2 + r_er**2)*15.*pi/180 # in radians
        part1 = (np.tan(fi)*np.cos(d)- np.sin(d)*np.cos(t))
        part2 = 1.0 / (1 + np.sin(t)**2/part1**2)
        df_fi = -part2*np.sin(t)*np.cos(d) / (np.cos(fi)**2*part1**2)
        df_d = part2*np.sin(t)*(np.tan(fi)*np.sin(d)+np.cos(t)*np.cos(d)) / part1**2
        df_t = part2*(np.cos(t)*part1 - np.sin(t)*np.sin(d)*np.sin(t)) / part1**2
        self.paralactic_angle_er = np.sqrt(df_fi**2*fi_er**2 + df_d**2*d_er**2 + df_t**2*t_er**2)

        #add nonhorizontality
        self.paralactic_angle += nonhorizontality
        self.paralactic_angle_er = np.sqrt(self.paralactic_angle_er**2 + nonhorizontality_er**2)



class FinalFitParameters():
    def __init__(self,flag):
        self.flag = flag
        self.dm21 = None        
        self.x2 = None        
        self.y2 = None        
        self.dm31 = None
        self.x3 = None
        self.y3 = None
        #errors
        self.dm21_er = None
        self.x2_er = None
        self.y2_er = None
        self.dm31_er = None
        self.x3_er = None
        self.y3_er = None

    def print_values(self):
        print('---------------xy dm results-----------------')
        print('dm21=',self.dm21,'+-',self.dm21_er,'[m]')
        print('x2=',self.x2,'+-',self.x2_er, '[px]')
        print('y2=',self.y2,'+-',self.y2_er, '[px]')
        if (self.flag == 'triple'):
            print('dm31=',self.dm31,'+-',self.dm31_er,'[m]')
            print('x3=',self.x3,'+-',self.x3_er, '[px]')
            print('y3=',self.y3,'+-',self.y3_er, '[px]')

    def save_to(self,filename):
        with open(filename,'w') as output:
            output.write('dm21='+ str(self.dm21) + '+-' + str(self.dm21_er) + '\n')
            output.write('x2=' + str(self.x2) + '+-' + str(self.x2_er) + '\n')
            output.write('y2=' + str(self.y2) + '+-' + str(self.y2_er) + '\n')
            if (self.flag == 'triple'):
                output.write('dm31='+ str(self.dm31) + '+-' + str(self.dm31_er) + '\n')
                output.write('x3=' + str(self.x3) + '+-' + str(self.x3_er) + '\n')
                output.write('y3=' + str(self.y3) + '+-' + str(self.y3_er) + '\n')


def final_result(filename_config,fit_parameters_config,angle_config):
    #read config file
    files = DataFiles()
    files.read_input(filename_config)
    coord_filename = files.data + '\\coord.txt'
    dm_xy_filename = files.data + '\\dm_xy.txt'

    #read fit parameters config
    input_fit_parameters = FitParameters()
    input_fit_parameters.read_input(fit_parameters_config)
        
    #read samples
    sample = ResultSample(input_fit_parameters.flag)
    sample.read_from(files.data)

    #calc final values and errors
    result = FinalFitParameters(input_fit_parameters.flag)
    result.dm21 = np.median(sample.dm21)
    result.dm21_er = np.std(sample.dm21)
    result.x2 = np.median(sample.x2)
    result.x2_er = np.std(sample.x2)
    result.y2 = np.median(sample.y2)
    result.y2_er = np.std(sample.y2)
    if (input_fit_parameters.flag == 'triple'):
        result.dm31 = np.median(sample.dm31)
        result.dm31_er = np.std(sample.dm31)
        result.x3 = np.median(sample.x3)
        result.x3_er = np.std(sample.x3)
        result.y3 = np.median(sample.y3)
        result.y3_er = np.std(sample.y3)
    result.print_values()
    print('psi2:',np.arctan2(result.y2,result.x2)*180/np.pi)
    print('psi3:',np.arctan2(result.y3,result.x3)*180/np.pi)
    result.save_to(dm_xy_filename)
    
    #convert coordinates in other system
    coord2 = Coordinate(x=result.x2,y=result.y2,x_er=result.x2_er,y_er=result.y2_er)
    coord2.calc_paralactic_angle(angle_config)
    coord2.calc_equtorial()
    coord2.calc_polar()
    if (input_fit_parameters.flag == 'triple'):
        coord3 = Coordinate(x=result.x3,y=result.y3,x_er=result.x3_er,y_er=result.y3_er)
        coord3.calc_paralactic_angle(angle_config)
        coord3.calc_equtorial()
        coord3.calc_polar()

    #save to file
    with open(coord_filename,'w') as output:
        output.write('alpha2:'+ str(coord2.alpha_in_px) + '+-' + str(coord2.alpha_in_px_er) + '[px]' + '\n')
        output.write('delta2:'+ str(coord2.delta_in_px) + '+-' + str(coord2.delta_in_px_er) + '[px]' + '\n')
        output.write('alpha2:'+ str(coord2.alpha) + '+-' + str(coord2.alpha_er) + '[arcsec]' + '\n')
        output.write('delta2:'+ str(coord2.delta) + '+-' + str(coord2.delta_er) + '[arcsec]' + '\n')
        output.write('r2:'+ str(coord2.r) + '+-' + str(coord2.r_er) + '[arcsec]' + '\n')
        output.write('theta2:'+ str(coord2.theta) + ' or ' + str(coord2.theta+180.) + '+-' + str(coord2.theta_er) + '[arcsec]' + '\n')
        output.write('\n')
        if (input_fit_parameters.flag == 'triple'):
            output.write('alpha3:'+ str(coord3.alpha_in_px) + '+-' + str(coord3.alpha_in_px_er) + '[px]' + '\n')
            output.write('delta3:'+ str(coord3.delta_in_px) + '+-' + str(coord3.delta_in_px_er) + '[px]' + '\n')
            output.write('alpha3:'+ str(coord3.alpha) + '+-' + str(coord3.alpha_er) + '[arcsec]' + '\n')
            output.write('delta3:'+ str(coord3.delta) + '+-' + str(coord3.delta_er) + '[arcsec]' + '\n')
            output.write('r3:'+ str(coord3.r) + '+-' + str(coord3.r_er) + '[arcsec]' + '\n')
            output.write('theta3:'+ str(coord3.theta) + ' or ' + str(coord3.theta+180.) + '+-' + str(coord3.theta_er) + '[arcsec]' + '\n')
    

