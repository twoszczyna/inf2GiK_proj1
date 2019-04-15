# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:19:27 2019

@author: pc
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QColorDialog
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title='Wyznaczanie przecięcia dwóch punktów'
        self.initInterface()
        self.initWidgets()
        self.setWindowIcon(QIcon('calculator.png'))
        
    def initInterface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100,100,600,500)
        self.show()
        
    def initWidgets(self):
        btn=QPushButton('rysuj',self)
        btncol=QPushButton('zmień kolor',self)
        btnsave=QPushButton('zapisz wynik',self)
        xAlabel=QLabel('x A',self) 
        yAlabel=QLabel('y A',self)  #definiowanie labeli i line editow
        xBlabel=QLabel('x B',self)
        yBlabel=QLabel('y B',self)
        xClabel=QLabel('x C',self)
        yClabel=QLabel('y x',self)
        xDlabel=QLabel('x D',self)
        yDlabel=QLabel('y D',self)
        polozenielabel=QLabel('polozenie prostych',self)
        
        btncol.setToolTip('wybierz kolor wykresu')
        btnsave.setToolTip('zapisz współrzędne pnnktu P do pliku')
        btn.setToolTip('nacinij aby narysowac wykres')
    
        self.xAEdit=QLineEdit()
        self.yAEdit=QLineEdit()
        self.xBEdit=QLineEdit()
        self.yBEdit=QLineEdit()
        self.xCEdit=QLineEdit()
        self.yCEdit=QLineEdit()
        self.xDEdit=QLineEdit()
        self.yDEdit=QLineEdit()
        self.polozenielabel=QLineEdit()
        
        self.xAEdit.setToolTip('wpisz wsp X punktu A')
        self.yAEdit.setToolTip('wpisz wsp y punktu A')#podpowiedzi do okien edycji 
        
        self.xBEdit.setToolTip('wpisz wsp X punktu B')
        self.yBEdit.setToolTip('wpisz wsp y punktu B')
        
        self.xCEdit.setToolTip('wpisz wsp X punktu C')
        self.yCEdit.setToolTip('wpisz wsp y punktu C')
        
        self.xDEdit.setToolTip('wpisz wsp X punktu D')
        self.yDEdit.setToolTip('wpisz wsp y punktu D')
        
        
        self.resultLabel = QLabel('',self)
        
        #wykres
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        #rozlokowanie przycisków i okien edycji w main window aplikacji
        grid = QGridLayout()
        grid.addWidget(xAlabel, 2, 0)
        grid.addWidget(self.xAEdit, 2, 1)  #wsp A
        grid.addWidget(yAlabel, 2, 3)
        grid.addWidget(self.yAEdit, 2, 4)
        
        grid.addWidget(xBlabel, 3, 0)
        grid.addWidget(self.xBEdit, 3, 1)    #Wsp B
        grid.addWidget(yBlabel, 3, 3)
        grid.addWidget(self.yBEdit, 3, 4)
        
        grid.addWidget(xClabel, 4, 0)
        grid.addWidget(self.xCEdit, 4, 1)    #wsp C
        grid.addWidget(yClabel, 4, 3)
        grid.addWidget(self.yCEdit, 4, 4)
        
        grid.addWidget(xDlabel, 5, 0)
        grid.addWidget(self.xDEdit, 5, 1)    #wsp D
        grid.addWidget(yDlabel, 5, 3)
        grid.addWidget(self.yDEdit, 5, 4)
        
        
        grid.addWidget(btn, 7, 0 ,1, 2)   #przycisk przelicz
        grid.addWidget(btncol, 7, 0,3,4) #przycisk zmiana koloru
        grid.addWidget(self.resultLabel,9,0)
        grid.addWidget(self.canvas, 1 ,7, -1, -1) #wykres
        
        grid.addWidget(polozenielabel,9,0) #label polozenia
        grid.addWidget(self.polozenielabel,9,1,1,4)
        
        grid.addWidget(btnsave,10,0,1,2) #przycisk zapisz
        
        self.setLayout(grid)
        
        
        
        btn.clicked.connect(self.oblicz)
        btncol.clicked.connect(self.zmienkolor)
        btn.clicked.connect(self.zapisz)
    
        
    def zmienkolor(self):
        color=QColorDialog.getColor()
        if color.isValid():
            print(color.name())
            self.SprawdzWartosc(col=color.name())
        
    def oblicz(self):
        self.SprawdzWartosc()
        
        
    #sprawdzenie czy wprowadzane przez użytkownika wartosci sa wartosciami liczbowymi oraz przeliczenie 
    def SprawdzWartosc(self,col='red'):
        xA=self.sprawdzwartosc(self.xAEdit)
        yA=self.sprawdzwartosc(self.yAEdit)
        xB=self.sprawdzwartosc(self.xBEdit)
        yB=self.sprawdzwartosc(self.yBEdit)
        xC=self.sprawdzwartosc(self.xCEdit)
        yC=self.sprawdzwartosc(self.yCEdit)
        xD=self.sprawdzwartosc(self.xDEdit)
        yD=self.sprawdzwartosc(self.yDEdit)
        
        if xA is not None and (yA is not None) and (xB is not None) and (yB is not None) and (xC is not None) and (yC is not None) and (xD is not None) and (yD is not None):
               
            if (((xB-xA)*(yD-yC))-((yB-yA)*(xD-xC)))==0:
                self.polozenielabel.setText('proste są równoległe')
            else:
                t1=(((xC-xA)*(yD-yC))-((yC-yA)*(xD-xC)))/(((xB-xA)*(yD-yC))-((yB-yA)*(xD-xC)))
                t2=(((xC-xA)*(yB-yA))-((yC-yA)*(xB-xA)))/(((xB-xA)*(yD-yC))-((yB-yA)*(xD-xC)))    
                self.xP=round(xA+t1*(xB-xA),3)
                self.yP=round(yA+t1*(yB-yA),3)
   
                if 0<=t1<=1 and 0<=t2<=1:
                    self.polozenielabel.setText("Punkt przecięcia leży wewnątrz obu odcinków")
                elif 0<=t1<=1 and t2<0 or t2>1:
                    self.polozenielabel.setText("punkt leży wewnątrz odcinka AB i na przedłużeniu odcinka CD")
                elif 0<=t2<=1 and t1<0 or t1>1:
                    self.polozenielabel.setText("punkt przecięcia leży wewnątrz odcinka CD i na przedłużeniu odcinka AB")
              #odwieżenie wykresu 
            x1=['A', 'B', 'C', 'D', 'P']
            X2=[xA, xB, xC, xD, self.xP]
            Y2=[yA, yB, yC, yD, self.yP]
                      
            self.figure.clear()
            ax=self.figure.add_subplot(111)  
            ax.scatter(X2,Y2)
            ax.plot([xA,xB],[yA,yB] ,color=col,marker='o')
            ax.plot([xC,xD],[yC,yD] ,color=col,marker='o')  #rysowanie wykresu
            ax.plot([xA,self.xP],[yA,self.yP] ,linestyle='--', color='red')
            ax.plot([xD,self.xP],[yD,self.yP] ,linestyle='--', color='blue')
            for (x,y,l) in zip(X2,Y2,enumerate(x1)):
                ax.annotate("{}({};{})".format(l[1],x,y), xy=(x,y)) #etykiety do punktów
           
            self.canvas.draw()
            
             
    def sprawdzwartosc(self,element):
        if element.text().lstrip('-').replace('.','',1).isdigit():
            return float(element.text())
        else:
            element.setFocus()
            return None 
        #zapis wyniku do pliku txt
    def zapisz(self):
        plik1=open('proj_1_wsp_pkt_P.txt','w+')#stworzenie pliku tekstowego
        plik1.write(80*'-')
        plik1.write('\n|{:^10}|\n'.format('współrzędne'))#okrelenie formatu zapisu danych
        plik1.write('\n|{:^10}|{:^10}|\n'.format('xP', 'yP'))
        plik1.write('\n|{:^10}|{:^10}|\n'.format(self.xP,self.yP))

        plik1.close()
            

def main():
    app = QApplication(sys.argv)
    window = AppWindow()
    app.exec_()
    
if __name__ == '__main__':
    main()