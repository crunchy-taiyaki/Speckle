class  DataFiles():
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


    def read_input(self,file):
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

    def info(self):
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
