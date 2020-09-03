import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from grid import Grid
from masks import GaussEllipse, ring_mask, elliptic_mask

def define_ylim(image):
    masked_image = ring_mask(image.values, image.b_bound, image.up_bound)
    ymin = np.min(masked_image)
    ymax = np.max(masked_image)
    return ymin,ymax


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

class FitParameters():
    def __init__(self):
        self.flag = None
        self.dm21 = None
        self.dm21_bottom = None
        self.dm21_upper = None
        self.x2 = None
        self.x2_bottom = None
        self.x2_upper = None
        self.y2 = None
        self.y2_bottom = None
        self.y2_upper = None
        # third star parameters
        self.dm31 = None
        self.dm31_bottom = None
        self.dm31_upper = None
        self.x3 = None
        self.x3_bottom = None
        self.x3_upper = None
        self.y3 = None
        self.y3_bottom = None
        self.y3_upper = None
        self.b_freq_border = None
        self.up_freq_border = None
        self.bandwidth = None

    def read_input(self,file):
        info = []
        with open(file, 'r') as input:
            for line in input:
                text = line.strip()
                if text.startswith('#'):
                    continue
                info.append(text)
        self.flag = info[0]
        self.dm21 = float(info[1])
        self.dm21_bottom = float(info[2])
        self.dm21_upper = float(info[3])
        self.x2 = float(info[4])
        self.x2_bottom = float(info[5])
        self.x2_upper = float(info[6])
        self.y2 = float(info[7])
        self.y2_bottom = float(info[8])
        self.y2_upper = float(info[9])

        if (self.flag == 'triple'):
            self.dm31 = float(info[10])
            self.dm31_bottom = float(info[11])
            self.dm31_upper = float(info[12])
            self.x3 = float(info[13])
            self.x3_bottom = float(info[14])
            self.x3_upper = float(info[15])
            self.y3 = float(info[16])
            self.y3_bottom = float(info[17])
            self.y3_upper = float(info[18])

        self.b_freq_border = int(info[19])
        self.up_freq_border = int(info[20])
        self.bandwidth = int(info[21])


class FitResult():
    def __init__(self,flag):
        self.flag = flag
        self.f_ar = None
        self.residuals = None
        self.I1_ar = None
        self.dm21_ar = None
        self.x2_ar = None
        self.y2_ar = None
        self.r12_ar = None
        self.psi2_ar = None
        # third star parameters
        self.dm31_ar = None
        self.x3_ar = None
        self.y3_ar = None
        self.r13_ar = None
        self.psi3_ar = None

    def read_i_xy_dm_freq_from(self,result_folder_path):
        path = result_folder_path
        self.I1_ar = np.load(path + '\\I1_ar.npy')
        self.dm21_ar = np.load(path + '\\dm21_ar.npy')
        self.x2_ar = np.load(path + '\\x2_ar.npy')
        self.y2_ar = np.load(path + '\\y2_ar.npy')
        self.f_ar = np.load(path + '\\f_ar.npy')
        self.residuals = np.load(path + '\\residuals.npy')
        if(self.flag=='triple'):
            self.dm31_ar = np.load(path + '\\dm31_ar.npy')
            self.x3_ar = np.load(path + '\\x3_ar.npy')
            self.y3_ar = np.load(path + '\\y3_ar.npy')



class Fit:
    def __init__(self,ps,model,initial_parameters,uv_grid,bottom_freq_border,upper_freq_border,bandwidth,flag,zone_flag=None,ellipse_params=None):
        self.bandwidth = bandwidth
        self.bottom_freq_border = bottom_freq_border
        self.upper_freq_border = upper_freq_border
        self.ps = ps #ObjSpectrum()
        self.init_guess = initial_parameters
        self.model = model
        self.uv_grid = uv_grid
        self.flag = flag
        self.zone_flag = zone_flag
        if (self.zone_flag == 'ellipse'):
            self.ellipse_params = ellipse_params #GaussEllipse()
        self.result = FitResult(self.flag)

    def ring_zones(self,zones):
        f_ar_lenght = len(self.result.f_ar)
        for i in range(f_ar_lenght):
            zones[i] = ring_mask(self.ps.values,self.result.f_ar[i],self.result.f_ar[i]+self.bandwidth)

    def elliptic_zones(self,zones):
        f_ar_lenght = len(self.result.f_ar)
        for i in range(f_ar_lenght):
            zones[i] = elliptic_mask(self.ps.values,self.result.f_ar[i],self.result.f_ar[i]+self.bandwidth,self.ellipse_params)

 
    def plot_zone(self,zone):
        plt.figure()
        plt.plot(zone[256,:])
        plt.title('x_zone projection')
        plt.show()

    def plot_fit_izone(self,i,zone_values):
        u,v = self.uv_grid
        freq_axis = np.arange(-256.0,256.0)
        if(self.flag == 'triple'):
            plt.figure()
            plt.plot(freq_axis, self.ps.values[256,:],label='all data')
            plt.plot(freq_axis, zone_values[256,:],label='data')
            plt.plot(freq_axis, self.model(u,v,*self.init_guess.array())[256,:], label='init guess')
            plt.plot(freq_axis, self.model(u,v,self.result.I1_ar[i],self.result.dm21_ar[i],self.result.x2_ar[i],self.result.y2_ar[i],\
                                                                    self.result.dm31_ar[i],self.result.x3_ar[i],self.result.y3_ar[i])[256,:],label='model')
            ymin,ymax = define_ylim(self.ps)
            plt.ylim(ymin,ymax)
            plt.title('x projection')
            plt.legend()

            plt.figure()
            plt.plot(freq_axis, self.ps.values[:,256],label='all data')
            plt.plot(freq_axis, zone_values[:,256],label='data')
            plt.plot(freq_axis, self.model(u,v,*self.init_guess.array())[:,256], label='init guess')
            plt.plot(freq_axis, self.model(u,v,self.result.I1_ar[i],self.result.dm21_ar[i],self.result.x2_ar[i],self.result.y2_ar[i],\
                                                                    self.result.dm31_ar[i],self.result.x3_ar[i],self.result.y3_ar[i])[:,256],label='model')
            ymin,ymax = define_ylim(self.ps)
            plt.ylim(ymin,ymax)
            plt.title('y projection')
            plt.legend()

        else:
            plt.figure()
            plt.plot(freq_axis, self.ps.values[256,:],label='all data')
            plt.plot(freq_axis, zone_values[256,:],label='data')
            plt.plot(freq_axis, self.model(u,v,*self.init_guess.array())[256,:], label='init guess')
            plt.plot(freq_axis, self.model(u,v,self.result.I1_ar[i],self.result.dm21_ar[i],self.result.x2_ar[i],self.result.y2_ar[i])[256,:],label='model')
            ymin,ymax = define_ylim(self.ps)
            plt.ylim(ymin,ymax)
            plt.title('x projection')
            plt.legend()

            plt.figure()
            plt.plot(freq_axis, self.ps.values[:,256],label='all data')
            plt.plot(freq_axis, zone_values[:,256],label='data')
            plt.plot(freq_axis, self.model(u,v,*self.init_guess.array())[:,256], label='init guess')
            plt.plot(freq_axis, self.model(u,v,self.result.I1_ar[i],self.result.dm21_ar[i],self.result.x2_ar[i],self.result.y2_ar[i])[:,256],label='model')
            ymin,ymax = define_ylim(self.ps)
            plt.ylim(ymin,ymax)
            plt.title('y projection')
            plt.legend()
        plt.show()

    def fit_i_xy_dm(self):

        def residual_function(init_guess):
        #This function must be defined here
        #because she needs to know the model as the atribute of Fit class,
        # therefore, (self) should be determined above,
        #  and at the same time, the self can not be set as a function argument,
        #  because the residual function should has only one argument,
        #   the vector initial_guess.
            return np.sum((self.model(u,v,*init_guess) - zone_values)**2)

        #init data
        u,v = self.uv_grid
        self.result.f_ar = np.arange(self.bottom_freq_border,self.upper_freq_border,self.bandwidth)
        f_ar_lenght = len(self.result.f_ar)
        self.result.I1_ar = np.zeros(f_ar_lenght)
        self.result.dm21_ar = np.zeros(f_ar_lenght)
        self.result.x2_ar = np.zeros(f_ar_lenght)
        self.result.y2_ar = np.zeros(f_ar_lenght)
        self.result.residuals = np.zeros(f_ar_lenght)

        if(self.flag == 'triple'):
            self.result.dm31_ar = np.zeros(f_ar_lenght)
            self.result.x3_ar = np.zeros(f_ar_lenght)
            self.result.y3_ar = np.zeros(f_ar_lenght)
        
        size = 512
        zones = np.ma.array(np.zeros((f_ar_lenght,size,size)))
        if (self.zone_flag == 'ellipse'):
            self.elliptic_zones(zones)
        else:
            self.ring_zones(zones)

        #fitting
        print('start fitting dm and xy')
        print('iteration: .. from ',len(zones))
        for i in range(len(zones)):
            print(i)
            zone_values = zones[i]
            scale = np.sqrt(np.nanmean(zone_values))
            self.init_guess.I1 = scale
            fit_result = minimize(residual_function, self.init_guess.array(), method='L-BFGS-B', tol=1e-8)
            if(self.flag=='triple'):
                self.result.I1_ar[i] = fit_result.x[0]
                self.result.dm21_ar[i] = fit_result.x[1]
                self.result.x2_ar[i] = fit_result.x[2]
                self.result.y2_ar[i] = fit_result.x[3]
                self.result.dm31_ar[i] = fit_result.x[4]
                self.result.x3_ar[i] = fit_result.x[5]
                self.result.y3_ar[i] = fit_result.x[6]
                self.result.residuals[i] = np.sum((self.model(u,v,\
                                                   self.result.I1_ar[i],self.result.dm21_ar[i],self.result.x2_ar[i],self.result.y2_ar[i],\
                                                   self.result.dm31_ar[i],self.result.x3_ar[i],self.result.y3_ar[i])-zone_values)**2)
            else:
                self.result.I1_ar[i] = fit_result.x[0]
                self.result.dm21_ar[i] = fit_result.x[1]
                self.result.x2_ar[i] = fit_result.x[2]
                self.result.y2_ar[i] = fit_result.x[3]
                self.result.residuals[i] = np.sum((self.model(u,v,self.result.I1_ar[i],self.result.dm21_ar[i],self.result.x2_ar[i],self.result.y2_ar[i])- zone_values)**2)

            #self.plot_fit_izone(i,zone_values)

    def save_i_xy_dm_freq(self,result_folder_path):
        path = result_folder_path
        np.save(path + '\\I1_ar.npy',self.result.I1_ar)
        np.save(path + '\\dm21_ar.npy',self.result.dm21_ar)
        np.save(path + '\\x2_ar.npy',self.result.x2_ar)
        np.save(path + '\\y2_ar.npy',self.result.y2_ar)
        np.save(path + '\\f_ar.npy',self.result.f_ar)
        np.save(path + '\\residuals.npy',self.result.residuals)
        if(self.flag=='triple'):
            np.save(path + '\\dm31_ar.npy',self.result.dm31_ar)
            np.save(path + '\\x3_ar.npy',self.result.x3_ar)
            np.save(path + '\\y3_ar.npy',self.result.y3_ar)

    def read_i_xy_dm_freq_from(self,result_folder_path):
        path = result_folder_path
        self.result.I1_ar = np.load(path + '\\I1_ar.npy')
        self.result.dm21_ar = np.load(path + '\\dm21_ar.npy')
        self.result.x2_ar = np.load(path + '\\x2_ar.npy')
        self.result.y2_ar = np.load(path + '\\y2_ar.npy')
        self.result.f_ar = np.load(path + '\\f_ar.npy')
        if(self.flag=='triple'):
            self.result.dm31_ar = np.load(path + '\\dm31_ar.npy')
            self.result.x3_ar = np.load(path + '\\x3_ar.npy')
            self.result.y3_ar = np.load(path + '\\y3_ar.npy')

    def xy_to_r_psi(self):
        #x1 = 0; y1 = 0
        if(self.flag=='triple'):
            self.result.r13_ar = np.sqrt((self.result.x3_ar)**2 + (self.result.y3_ar)**2)
            self.result.psi3_ar = np.arctan2(self.result.y3_ar,self.result.x3_ar)*180.0/np.pi
        self.result.r12_ar = np.sqrt((self.result.x2_ar)**2 + (self.result.y2_ar)**2)
        self.result.psi2_ar = np.arctan2(self.result.y2_ar,self.result.x2_ar)*180.0/np.pi

 

  





 






