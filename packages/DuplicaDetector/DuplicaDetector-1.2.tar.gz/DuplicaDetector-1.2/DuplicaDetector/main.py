from PIL import Image
import pandas as pd
from datetime import datetime
from random import randint

class ImageChecker:
    def __init__(self):
        self.__pixels = []
        self.__image = None
        self.__imagename = ""
        self.__r_mean = 0
        self.__g_mean = 0
        self.__b_mean = 0
        try:
            self.__db = pd.read_pickle("db.pkl")
        except:
            self.__db = pd.DataFrame(columns=['PATH','LENGHT','WIDTH'])
            df.to_pickle("db.pkl")

    def __SaveImage(self, size):
        name = "pictures/" + str(datetime.now()) + self.__imagename[len(self.__imagename) - 4:]
        self.__image.save(name)
        df_tmp = [name, str(size[1]), str(size[0])]
        self.__db = self.__db.append(pd.DataFrame([df_tmp], columns=self.__db.columns), ignore_index=True)
        return (name)

    def Exit(self):
        self.__db.to_pickle("db.pkl")

    def DoesExist(self, image):
        def ImageData():
            pass
        try:
            self.__image = Image.open(image)
        except FileNotFoundError:
            return(1)
        self.__imagename = image
        size = self.__image.size
        samesize = self.__db[self.__db['LENGHT'] == str(size[1])][self.__db['WIDTH'] == str(size[0])]
        if samesize.empty:
            setattr(ImageData, 'path', self.__SaveImage(size))
            setattr(ImageData, 'exists', False)
            return (ImageData)
        else:
            res = self.__Credits(samesize, size)
            if (res[1] == False):
                setattr(ImageData, 'exists', False)
            else:
                setattr(ImageData, 'exists', True)
            setattr(ImageData, 'path', res[0])
            return (ImageData)

    def __get_colors_means(self, image, size):
        r, g, b = 0, 0, 0
        pixels = image.getdata()
        for element in pixels:
            r += element[0]
            g += element[1]
            b += element[2]
        return(r/(size[0] * size[1]), g/(size[0] * size[1]), b/(size[0] * size[1]))

    def __check_random_value(self, samesize, size, im):
        i = 0
        pixels = im.getdata()
        maxi = int(int(size[0] * size[1]) / 1000)
        while (i != maxi):
            y = randint(0, maxi*1000)
            if (pixels[y][0:3] != self.__pixels[y][0:3]):
                return(1)
            i += 1
        return (0)

    def __Credits(self, samesize, size):
        r, g, b = 0, 0, 0
        self.__pixels = self.__image.getdata()
        for element in self.__pixels:
            r += element[0]
            g += element[1]
            b += element[2]
        self.__r_mean, self.__g_mean, self.__b_mean = r/(size[0] * size[1]), g/(size[0] * size[1]), b/(size[0] * size[1])
        for _, element in samesize.iterrows():
            im = Image.open(str(element['PATH']))
            if (self.__get_colors_means(im, im.size) == (self.__r_mean, self.__g_mean, self.__b_mean)):
                if (self.__check_random_value(samesize, size, im) == 0):
                    return(str(element['PATH']), True)
        return (self.__SaveImage(size), False)