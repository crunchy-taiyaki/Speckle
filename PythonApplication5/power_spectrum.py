import numpy as np

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
        if (darkname == None):
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
    if (flatname == None):
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
    if (starname == None):
        print("'-' in input file")
        print('obj(ref) power spectrum calculation will be ignored')
        return None
    else:
        if (middle_dark == None):
            middle_dark = 0.
        if (middle_flat == None):
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

def remove_background(image, xlim):
    outbound = image[xlim:512,0:512]
    slice_out = np.mean(image, axis=0)
    clean_image = image - slice_out
    return clean_image


class Data():

    def __init__(self):
        self.star_ps = None
        self.dark = None
        self.ref_dark = None
        self.flat = None
        self.ref_ps = None
        self.final_ps = None

    def save_to(self,result_folder_path):
        path = result_folder_path
        np.save(path + '\\mean_dark.npy',self.dark)
        np.save(path + '\\mean_flat.npy',self.flat)
        np.save(path + '\\mean_star_ps.npy',self.star_ps)
        np.save(path + '\\mean_ref_ps.npy',self.ref_ps)
        np.save(path + '\\final_ps.npy',self.final_ps)

    def read_from(self,result_folder_path):
        path = result_folder_path
        self.dark = np.load(path + '\\mean_dark.npy')
        self.flat = np.load(path + '\\mean_flat.npy')
        self.star_ps = np.load(path + '\\mean_star_ps.npy')
        self.ref_ps = np.load(path + '\\mean_ref_ps.npy')
        self.final_ps = np.load(path + '\\final_ps.npy')

    def final_power_spectrum(self):
        self.final_ps = self.star_ps/self.ref_ps

