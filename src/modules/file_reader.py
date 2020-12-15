"""Модуль содержит классы, реализующие чтение данных из текстовых (конфигурационных) файлов."""

class  FileInfoReader:
    """ Класс содержит информацию о файлах спекл-интерферометрических серий:
    их абсолютные пути, колличество кадров в серии, а также абсолютные пути
    к директориям с результатами работы программы."""
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
        print('--------------------------------------------')

    def info(self,filename_config):
        self.read(filename_config)
        self.write_info()

class FitParametersReader:
    def __init__(self):
        self.star_type = None
        self.rmbg_flag = None
        self.zone_type = None
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
        self.star_type = info[0]
        self.rmbg_flag = info[1]
        self.zone_type = info[2]
        self.method = info[3]
        self.dm21 = float(info[4])
        self.dm21_bottom = float(info[5])
        self.dm21_upper = float(info[6])
        self.x2 = float(info[7])
        self.x2_bottom = float(info[8])
        self.x2_upper = float(info[9])
        self.y2 = float(info[10])
        self.y2_bottom = float(info[11])
        self.y2_upper = float(info[12])

        if self.star_type == 'triple':
            self.dm31 = float(info[13])
            self.dm31_bottom = float(info[14])
            self.dm31_upper = float(info[15])
            self.x3 = float(info[16])
            self.x3_bottom = float(info[17])
            self.x3_upper = float(info[18])
            self.y3 = float(info[19])
            self.y3_bottom = float(info[20])
            self.y3_upper = float(info[21])

        self.b_freq_border = int(info[22])
        self.up_freq_border = int(info[23])
        self.bandwidth = int(info[24])
        self.mask_b_freq_border = int(info[25])
        self.mask_up_freq_border = int(info[26])
