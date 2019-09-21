# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 21:10:34 2018

@author: Adi
"""


## Pakiety

import os
import urllib
from urllib import request
import zipfile


#os.mkdir(sciezka+"synoptyczne")
sciezka = "D://meteo//meteo_synop"   # miejsce, do którego pobrane zostaną dane pogodowe dla całego kraju
os.chdir(sciezka)
os.getcwd()
#os.mkdir("Poznan") # stworzenie katalogu, który będzie przechowywał dane pogodowe tylko dla Poznania




########### I - Pobieranie plików ##############



## 1. Lista adresow do poszczegolnych lat (duża pętla w następnych punktach)
## 2. Wyszukanie nazw archiwów .zip poszczególnych miesięcy dla każdego roku
## 3. Pobranie danych z każdego miesiąca


##1

adr_glowny = 'https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/synop/'
lista_adresow = [adr_glowny+str(i) for i in range(2010,2018)] # Rok bieżący, w dalszej częsci kodu, wymaga odmiennego sposobu sczytywania ze strony nazw plików



##2 i 3

for d in range(len(lista_adresow)):
    strona = request.urlopen(lista_adresow[d]).read()#.spliteline()
    plik_str=str(strona).splitlines()
    
    l=0
    lista = []
    
    for i in range(len(plik_str[0][:])):
        if plik_str[0][i] == 'e' and plik_str[0][i+1] == 'f' and plik_str[0][i+2]== '=' and plik_str[0][i+4]=='2':
            #j=[]
            j=i+4
            listka=[]
            [listka.append(plik_str[0][k]) for k in range(j,j+14)]
            lista.append(''.join(listka))

    for z in range(len(lista)):
        zipek = request.urlopen(lista_adresow[d]+"/"+lista[z])
        zipek_zawartosc = zipek.read()
        with open(lista[z], 'wb')as f:
            f.write(zipek_zawartosc)



############# II - Rozpakowywanie plików ##############
            
pliki=os.listdir(".")

poznanie =[]

## Petla wyszukujaca wsrod plikow z katalogu, tylko te odnoszace sie do Poznania (kod 330)

for i in range(len(pliki)):
    if pliki[i].find("330") > 0:
        poznanie.append(pliki[i])
    
zrodlo= []

#Przeniesienie archiwow .zip do innego katalogu

for i in range(len(poznanie)):
    zrodlo= sciezka + "//" + poznanie[i]
    cel = sciezka + "//Poznan" + "//" +poznanie[i]
    os.rename(zrodlo,cel)


sciezka_2 = "D://meteo//meteo_synop//Poznan"
os.chdir(sciezka_2)

#Wypakowywanie plikow z archiwow

for i in range(len(poznanie)):
    with zipfile.ZipFile(poznanie[i],"r") as zip_ref:
        zip_ref.extractall(sciezka_2)