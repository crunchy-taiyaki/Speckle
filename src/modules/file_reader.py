"""Модуль содержит классы, реализующие чтение данных из текстовых (конфигурационных) файлов."""

class  FileInfoReader:
    """ Класс содержит информацию о файлах спекл-интерферометрических серий:
    их абсолютные пути, колличество кадров в серии, а также абсолютные пути
    к директориям с результатами работы программы.
    
    Конструктор __init__: содержит информацию о файлах и абсолютных путях,
    заполняется с помощью метода read.

    Методы:    
    read: принимает аргументом абсолютный путь читаемого файла, заполняет поля экземпляра класса.    
    write: выводит данные на экран
    info: комбинация read и write - считывает данные и выводит информацию на экран

    Пример:
    filename_config = 'C:\\Users\\input.txt'
    file_reader = FileInfoReader()
    file_reader.info(filename_config)
    """

    def __init__(self):
        # абсолютные пути к спекл-интерфереметрическим файлам
        self.star = None # серия объекта/звезды 
        self.dark = None # серия темновых кадров      
        self.flat = None # серия кадров плоского поля       
        self.ref = None  # серия опорного (точечного) объекта      
        self.ref_dark = None # серия темновых кадров для опорного объекта
        
        # колличество кадров в сериях
        self.star_frames = None
        self.dark_frames = None
        self.flat_frames = None
        self.ref_frames = None
        self.ref_dark_frames = None

        # абсолютные пути к результатам работы программы
        self.images = None # директория для всех изображений
        self.data = None # директория с прочими данными: бинарные (.npy) и текстовые (.txt) файлы


    def read(self,file):
        info = []
        with open(file, 'r') as input:
            for line in input:
                text = line.strip()
                if text.startswith('#'):
                    continue
                info.append(text)
        info = [x if x!='-' else None for x in info] # заменяем '-' на None
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

    def write(self):
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
        self.write()

class FitParametersReader:
    """ Класс содержит параметры фитирования спектров мощности.
    
    Конструктор __init__: содержит параметры фитирования спектров мощности,
    заполняется с помощью метода read.

    Методы:    
    read: принимает аргументом абсолютный путь читаемого файла, заполняет поля экземпляра класса.
    
    Пример:
    fit_parameters_config = 'C:\\Users\\fit_parameters.txt'
    input_fit_parameters = FitParametersReader()
    input_fit_parameters.read(fit_parameters_config) #чтение файла
    input_fit_parameters.star_type # возвращает тип звезды, указанный в файле
    """

    def __init__(self):
        self.star_type = None # тип исследуемой звезды: binary или triple, например
        self.rmbg_flag = None # переключатель процедуры удаления шумовой подложки
                              # у спектров мощности объекта и опоры
        self.zone_type = None # форма областей подбора параметров модели: ring или elliptical
        self.dm21 = None # разность блеска m2 - m1, где m1 - звездная величина самой яркой звезды
        self.dm21_bottom = None # нижняя граница поиска dm21
        self.dm21_upper = None # верхняя граница поиска dm21
        self.x2 = None # x координата второй звезды
        self.x2_bottom = None # нижняя граница поиска x2
        self.x2_upper = None # верхняя граница поиска x2
        self.y2 = None # y координата второй звезды
        self.y2_bottom = None # нижняя граница поиска y2
        self.y2_upper = None # верхняя граница поиска y2
        self.dm31 = None # разность блеска m3 - m1, где m1 - звездная величина самой яркой звезды
        self.dm31_bottom = None # нижняя граница поиска dm31
        self.dm31_upper = None # верхняя граница поиска dm31
        self.x3 = None # x координата третьей звезды
        self.x3_bottom = None # нижняя граница поиска x3
        self.x3_upper = None # верхняя граница поиска x3
        self.y3 = None # y координата третьей звезды
        self.y3_bottom = None # нижняя граница поиска y3
        self.y3_upper = None # верхняя граница поиска y3
        # нижняя и верхняя границы области поиска параметров модели
        # по пространственной частоте 
        self.b_freq_border = None
        self.up_freq_border = None
        self.bandwidth = None # ширина шага по частоте

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
