import numpy as np
import matplotlib.pyplot as plt
from masks import ring_mask


def middle_fft(imagename,imageframes):
    images = np.memmap(imagename,mode='r', dtype='uint16', shape=(imageframes,512,512))
    middle_fft = np.zeros((512,512))
    for i in range(imageframes):
        middle_fft = middle_fft + np.fft.fft(images[i])
    middle_fft /= imageframes
    images = None
    return middle_fft


def middle_dark(darkname,darkframes):
    print('-----------------DARK-----------------')
    if (darkname == None):
        print("'-' in input file")
        print('dark calculation will be ignored')
    else:
        print('-------Frames ignored in dark calculation--------')
        dark=np.memmap(darkname,mode='r', dtype='uint16', shape=(darkframes,512,512))
        middle_dark=np.zeros((512,512))
        for i in range(darkframes):
            if np.amax(dark[i]) > 10000: # mask frames with particles
                print(i) # print masked frames
                continue # mask frames with particles
            middle_dark+=dark[i]
        middle_dark/=darkframes
        dark=None
        return middle_dark

def median_dark(darkname,darkframes):
        print('-----------------MEDIAN DARK-----------------')
        if (darkname is None):
            print("'-' in input file")
            print('median dark calculation will be ignored')
            return None
        else:
            dark=np.memmap(darkname, dtype='uint16', shape=(darkframes,512,512))
            print('calculation...')
            median_dark = np.median(dark, axis=0)
            dark=None
            return median_dark
 
def middle_flat(flatname,flatframes):
    print('-----------------FLAT-----------------')
    if (flatname is None):
        print("'-' in input file")
        print('flat calculation will be ignored')
        return None
    else:
        print('-------Frames ignored in flat calculation--------')
        flat=np.memmap(flatname, mode='r', dtype='uint16', shape=(flatframes,512,512))
        maxintflat=np.zeros(flatframes)
        middle_flat=np.zeros((512,512))
        for i in range(flatframes):
            if np.amax(flat[i]) > 40000: # mask frames with particles
                print(i) # print masked frames
                continue # mask frames with particles
            middle_flat+=flat[i]
        middle_flat/=flatframes
        flat=None
        return middle_flat

def obj_ps(starname,starframes, middle_dark, middle_flat):
    print('-----------------POWER SPECTRUM-----------------')
    if (starname is None):
        print("'-' in input file")
        print('obj(ref) power spectrum calculation will be ignored')
        return None
    else:
        if (middle_dark is None):
            middle_dark = 0.
        if (middle_flat is None):
            middle_flat = 1.
        star=np.memmap(starname,mode='r', dtype='uint16', shape=(starframes,512,512))
        middle_star=np.zeros((512,512))
        print('-------Frames ignored in flat calculation--------')
        for i in range(starframes):
            if np.amax(star[i]) > 50000: # mask frames with particles 50000 -55000
                print(i) # print masked frames
                continue # mask frames with particles
            image=(star[i]-middle_dark)/(middle_flat-middle_dark)
            image=np.abs(np.fft.fft2(image))**2
            middle_star+=image
        middle_star/=starframes
        middle_star=np.fft.fftshift(middle_star)
        image=None
        return middle_star

    def dark_power_spectrum(darkname,darkframes):
        dark=np.memmap(darkname,mode='r', dtype='uint16', shape=(darkframes,512,512))
        dark_ps=zeros((512,512))
        for i in range(darkframes):
            if np.amax(dark[i]) > 5000: # mask frames with particles
                continue # mask frames with particles
            imagedark=(dark[i]-middle_dark)/(middle_flat-middle_dark)
            imagedark=np.abs(np.fft.fft2(imagedark))**2
            dark_ps+=imagedark
            if i%250==0:
                print('Frames: %i'%i)
        dark_ps/=darkframes
        dark_ps=np.fft.fftshift(dark_ps)
        imagedark=None
        return dark_ps

def remove_background(image,freq_border):
    if (freq_border==512*np.sqrt(2)):
        return image
    else:
        frame_edge = 512*np.sqrt(2)
        background = ring_mask(image,freq_border,frame_edge)
        slice_out = np.mean(background)
        clean_image = image - slice_out
        return clean_image



class ObjSpectrum():
    def __init__(self):
        self.values = None
        self.b_bound = None
        self.up_bound = None
        self.clean_ps = None

    def define_bounds(self):
        freq_axis = np.arange(256.0)
        print('define frequence bound of spectrum')
        #plot star power spectrum profile
        plt.figure(figsize=(8,8))
        plt.subplot(2,1,1)
        plt.plot(freq_axis,self.values[256,256:])
        plt.yscale('log')
        plt.xlim(0,256)
        plt.title('x projection of spectrum')
        plt.subplot(2,1,2)
        plt.plot(freq_axis,self.values[256:,256])
        plt.yscale('log')
        plt.xlim(0,256)
        plt.title('y projection of spectrum')
        plt.show(block=False)

        #seting frequencies from console
        x_bottom_freq = int(input('enter BOTTOM frequency (integer format) for X projection:'))
        x_upper_freq = int(input('enter UPPER frequency (integer format) for X projection:'))
        y_bottom_freq = int(input('enter BOTTOM frequency (integer format) for Y projection:'))        
        y_upper_freq = int(input('enter UPPER frequency (integer format) for Y projection:'))

        #compute frequence bounds
        self.b_bound = np.max([x_bottom_freq,y_bottom_freq])
        self.up_bound = np.max([x_upper_freq,y_upper_freq])

    def rmbg(self):
        self.clean_ps = remove_background(self.values, self.up_bound)



class Data():

    def __init__(self):
        self.star_ps = ObjSpectrum()
        self.dark = None
        self.ref_dark = None
        self.flat = None
        self.ref_ps = ObjSpectrum()
        self.final_ps = ObjSpectrum()
        self.rmbg_final_ps = ObjSpectrum()

    def save_to(self,result_folder_path):
        path = result_folder_path
        np.save(path + '\\mean_dark.npy',self.dark)
        np.save(path + '\\mean_flat.npy',self.flat)
        np.save(path + '\\mean_star_ps.npy',self.star_ps.values)
        np.save(path + '\\mean_ref_ps.npy',self.ref_ps.values)
        np.save(path + '\\final_ps.npy',self.final_ps.values)
        np.save(path + '\\final_rmbg_ps.npy',self.rmbg_final_ps.values)
        np.save(path + '\\freq_bound.npy',np.array([self.star_ps.b_bound,self.star_ps.up_bound,\
                                                    self.ref_ps.b_bound,self.ref_ps.up_bound,\
                                                    self.final_ps.b_bound,self.final_ps.up_bound\
            ]))

    def read_raw_data_from(self,result_folder_path):
        path = result_folder_path
        self.dark = np.load(path + '\\mean_dark.npy')
        self.flat = np.load(path + '\\mean_flat.npy')
        self.star_ps.values = np.load(path + '\\mean_star_ps.npy')
        self.ref_ps.values = np.load(path + '\\mean_ref_ps.npy')

    def read_from(self,result_folder_path):
        path = result_folder_path
        self.dark = np.load(path + '\\mean_dark.npy')
        self.flat = np.load(path + '\\mean_flat.npy')
        self.star_ps.values = np.load(path + '\\mean_star_ps.npy')
        self.ref_ps.values = np.load(path + '\\mean_ref_ps.npy')
        self.final_ps.values = np.load(path + '\\final_ps.npy')
        self.rmbg_final_ps.values = np.load(path + '\\final_rmbg_ps.npy')
        freq_bounds = np.load(path + '\\freq_bound.npy')
        self.star_ps.b_bound = freq_bounds[0]
        self.star_ps.up_bound = freq_bounds[1]
        self.ref_ps.b_bound = freq_bounds[2]
        self.ref_ps.up_bound = freq_bounds[3]
        self.final_ps.b_bound = freq_bounds[4]
        self.final_ps.up_bound = freq_bounds[5]
        self.rmbg_final_ps.b_bound = self.final_ps.b_bound
        self.rmbg_final_ps.up_bound = self.final_ps.up_bound

    def define_freq_bounds(self):
        self.star_ps.define_bounds()
        self.ref_ps.define_bounds()

    def rmbg(self):
        self.star_ps.rmbg()
        self.ref_ps.rmbg()

    def find_final_ps(self):
        self.final_ps.values = self.star_ps.values/self.ref_ps.values
        self.rmbg_final_ps.values = self.star_ps.clean_ps/self.ref_ps.clean_ps

        self.final_ps.b_bound = np.max([self.star_ps.b_bound,self.ref_ps.b_bound])
        self.final_ps.up_bound = np.min([self.star_ps.up_bound,self.ref_ps.up_bound])
        self.rmbg_final_ps.b_bound = self.final_ps.b_bound
        self.rmbg_final_ps.up_bound = self.final_ps.up_bound

