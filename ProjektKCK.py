import cv2
from skimage import feature, data, color, measure
from skimage.filters.edges import convolve
from pylab import *
import skimage as ski
from skimage import data, io, filters, exposure
import numpy as np

def policzSumeKonturu(image,obrazek_kontur,nrObrazu):  # zwraca wspolczynnik dla kazdego z konturow na obrazku
    tablica_y = []
    tablica_x=[]
    for i in obrazek_kontur:
        tablica_y.append(i[1])
        tablica_x.append(i[0])

    min_y = min(tablica_y)
    max_y = max(tablica_y)
    min_x = min(tablica_x)
    max_x = max(tablica_x)

    #sumaKonturuKolor=0.0
    sumaKonturuCanny = 0.0
    #sumaKonturuBialych=0.0
    licznikpikseli=0

    image_background = color.rgb2hsv(image)

    for i in range(len(image_background)):
        for j in range(len(image_background[i])):
            image_background[i][j] = [0, 0, 0]

    image_pom = data.imread('./Pomocnicze/4_FiltrCanny' + str(nrObrazu) + '.jpg')

    cv2.drawContours(image_background, [obrazek_kontur], 0, (255, 255, 255), 1)

    for i in range (min_y+1,max_y-1):

            liczbaBialych=0
            flaga=False

            for j in range (min_x,max_x):
                if (image_background[i,j,2]==255.0 and flaga==False):
                    liczbaBialych=liczbaBialych+1
                    continue

                if (liczbaBialych != 0 and image_background[i,j,2]!=255.0):
                    #sumaKonturuKolor = sumaKonturuKolor + float(fabs(image[i, j , 2] - image[i, j-1, 2]))
                    #sumaKonturuCanny = sumaKonturuCanny + float(fabs(image_pom[i, j] - image_pom[i, j - 1]))
                    if(image_pom[i,j]==255.0):
                        sumaKonturuCanny=sumaKonturuCanny+1.0
                    #if(image[i, j , 2]>150.0): #<40
                        #sumaKonturuBialych=sumaKonturuBialych+1

                    licznikpikseli=licznikpikseli+1
                    flaga=True

                if (image_background[i,j,2]==255.0 and flaga==True):
                    break

    '''
    #if ((sumaKonturuBialych/licznikpikseli) > 0.70 and sumaKonturuBialych/licznikpikseli < 0.85):
    #    print("AAAAA")
    #    wagaKolorBialy=1.0
    #else:
    #   wagaKolorBialy=0.0


    #if ((sumaKonturuCanny/licznikpikseli) > 0.05 and sumaKonturuCanny/licznikpikseli < 0.2):
     #   print("BBBBBB")
    #    wagaKolorCanny=1.0
    #else:
    #    wagaKolorCanny=0.0
    #wagaKolor=2.0
    #wagaCanny=5.0
    #wspolczynnik=(wagaKolor*sumaKonturuKolor)+(wagaCanny*sumaKonturuCanny)+(sumaKonturuCzarnych*wagaKolorCzarny) / licznikpikseli

    #wspolczynnik=wagaKolorCanny*sumaKonturuCanny/licznikpikseli + wagaKolorBialy*sumaKonturuBialych/licznikpikseli
    #print("licznikPikseli", licznikpikseli, " Wspolczynnik ", wspolczynnik)'''

    wspolczynnik=sumaKonturuCanny/licznikpikseli
    return wspolczynnik

def stworzWartWspolczynnikowObrazka(image, tablica_konturow,nrObrazu): #zwraca tablice wartosci wspolczynnikow konturow dla obrazka
    tab_najlepszych=[]

    for kon in tablica_konturow:
        tab_najlepszych.append( policzSumeKonturu(image,kon,nrObrazu))

    return tab_najlepszych

def wyrownajHistogram(filename): #wyrowunuje histogram dla obrazka kolorowego

    src2 = cv2.cvtColor(filename, cv2.COLOR_BGR2YCrCb)
    b, g, r = cv2.split(src2)

    img = cv2.merge((b, g, r))
    img_final = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)

    return img_final

def dlugosc_i_wysokosc(tablica_tablic): # sprawdza rozmiar przypuszczanej tablicy
    a = tablica_tablic[0]
    b = tablica_tablic[1]
    c = tablica_tablic[2]
    d = tablica_tablic[3]
    x = 0
    y = 1
    odleglosc1 = sqrt((a[x] - b[x]) * (a[x] - b[x]) + (a[y] - b[y]) * (a[y] - b[y]))
    odleglosc2 = sqrt((a[x] - d[x]) * (a[x] - d[x]) + (a[y] - d[y]) * (a[y] - d[y]))
    if (odleglosc1==0):
        odleglosc1=0.1
    if (odleglosc2==0):
        odleglosc2=0.1
    if odleglosc1 > odleglosc2:
        return odleglosc1, odleglosc2
    else:
        return odleglosc2, odleglosc1


def czy_pozioma(tablica): # sprawdza czy przypuszczalna tablica nie jest pionowa
    tablica_x = []
    tablica_y = []
    for i in tablica:
        tablica_x.append(i[0])
        tablica_y.append(i[1])

    min_x = min(tablica_x)
    max_x = max(tablica_x)
    min_y = min(tablica_y)
    max_y = max(tablica_y)

    odl_x = max_x - min_x
    odl_y = max_y - min_y

    if odl_x > odl_y:
        return 1
    else:
        return 0


def pictureToData(pictureName, nrObrazu): #przetwarzanie obrazu
    image_hist = data.imread(pictureName)
    wynikowy_hist = wyrownajHistogram(image_hist)
    cv2.imwrite('./Pomocnicze/1_WyrownanyHistKolor' + str(nrObrazu) + '.jpg', wynikowy_hist)

    image = data.imread('./Pomocnicze/1_WyrownanyHistKolor' + str(nrObrazu) + '.jpg')

    image2 = cv2.medianBlur(image, 5)  # z 9 tez jest spoko
    cv2.imwrite('./Pomocnicze/2_FiltrMedianowy' + str(nrObrazu) + '.jpg', image2)

    image = data.imread('./Pomocnicze/2_FiltrMedianowy' + str(nrObrazu) + '.jpg', flatten=True)

    image = ski.filters.gaussian(image, sigma=1.5)  # bylo 2 sigma

    #dla rysowania tablic ( wszystkie - zostawione - najlepsza )
    image_background1 = data.imread(pictureName)
    image_background2 = data.imread(pictureName)
    image_background_wyn = data.imread(pictureName)

    io.imsave('./Pomocnicze/3_FiltrGauss' + str(nrObrazu) + '.jpg', image)
    image_pom = data.imread("./Pomocnicze/3_FiltrGauss" + str(nrObrazu) + '.jpg', 0)

    image_pom = cv2.Canny(image_pom, 100, 150)

    io.imsave('./Pomocnicze/4_FiltrCanny' + str(nrObrazu) + '.jpg', image_pom)

    im, contours, a = cv2.findContours(image_pom, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, offset=(0, 0))
    prostokaty = []
    for i in contours:
        rect = cv2.minAreaRect(i)
        box = cv2.boxPoints(rect)
        prostokaty.append(np.int0(box))

    #zapis wszystkich prostokatow
    for i in range (0,len(prostokaty)):
        cv2.drawContours(image_background1 , [prostokaty[i]], 0, (255, 255, 0), 5)
    io.imsave('./Pomocnicze/5_WszystkieProstokaty' + str(nrObrazu) + '.jpg', image_background1)

    od = 3.0
    do1 = 6.5
    zostawione=[]

    for contour in prostokaty:
        d, h = dlugosc_i_wysokosc(contour)

        if czy_pozioma(contour) == 1 and (d / h) >= od and (d / h) <= do1 and d>75 and h>25:
            zostawione.append(contour)


    #zapis zostawionych prostokatow

    for i in range (0,len(zostawione)):
        cv2.drawContours(image_background2 , [zostawione[i]], 0, (255, 255, 0), 5)

    io.imsave('./Pomocnicze/6_PrzypuszczalneTablice' + str(nrObrazu) + '.jpg', image_background2)


    tablicaWspolObrazka = stworzWartWspolczynnikowObrazka(image_background2, zostawione,nrObrazu)

    maxwart=max(tablicaWspolObrazka)
    indeks=0
    for i in range(0,len(tablicaWspolObrazka)):
        if(tablicaWspolObrazka[i]==maxwart):
            indeks=i
            break
    #print(indeks)
    cv2.drawContours(image_background_wyn, [zostawione[indeks]], 0, (255, 255, 0), 5)

    io.imsave('./Wyniki/Obraz' + str(nrObrazu) + '.jpg', image_background_wyn)
    print("Przetworzylem obrazek nr ", nrObrazu)

def LoopLoadFiles():  #laduje pliki obrazow z katalogu
    fileList = "./BazaAut/auto"
    for nrObrazu in range(1,2):

        pictureName = fileList + str(nrObrazu) + '.jpg'

        pictureToData(pictureName, nrObrazu)



def main():
    LoopLoadFiles()


if __name__ == '__main__':
    main()
