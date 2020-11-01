class  InputReader():
    def __init__(self):
        self.star = None
        self.dark = None        
        self.flat = None        
        self.ref = None        
        self.ref_dark = None
        
        self.star_frames = None
        self.dark_frames = None
        self.flat_frames = None
        self.ref_frames = None
        self.ref_dark_frames = None

        self.images = None
        self.data = None
        self.work_dir = None


    def read(self,file):
        info = []
        with open(file, 'r') as input:
            for line in input:
                text = line.strip()
                if text.startswith('#'):
                    continue
                info.append(text)
        info = [x if x!='-' else None for x in info] #exchange '-' to None
        self.star = info[0]
        self.star_frames = int(info[1])
        self.dark = info[2]
        self.dark_frames = int(info[3])
        self.flat = info[4]
        self.flat_frames = int(info[5])

        self.ref = info[6]
        self.ref_frames = int(info[7])
        self.ref_dark = info[8]
        self.ref_dark_frames = int(info[9])

        self.images = info[10]
        self.data = info[11]
        self.work_dir = info[12]

    def write_info(self):
        print('--------------------------------------------')
        print('----------------INPUT INFO------------------')
        print('--------------------------------------------')
        print('star',self.star)
        print('star frames',self.star_frames)
        print('dark',self.dark)
        print('dark frames',self.dark_frames)
        print('flat',self.flat)
        print('flat frames',self.flat_frames)

        print('reference star',self.ref)
        print('reference star frames',self.ref_frames)
        print('reference star dark',self.ref_dark)
        print('referemce star dark frames',self.ref_dark_frames)

        print('images folder',self.images)
        print('data folder',self.data)
        print('working directory',self.work_dir)
        print('--------------------------------------------')

    def info(self,filename_config):
        self.read(filename_config)
        self.write_info()

class FitParametersReader():
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

    def read(self,file):
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
        self.mask_b_freq_border = int(info[22])
        self.mask_up_freq_border = int(info[23])
