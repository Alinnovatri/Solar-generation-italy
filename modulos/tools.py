
#Import the necessary libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plt.style.use('seaborn')

class EnergyDataItaly:
    """Muestra un análisis detallado de la generación de energía solar y del consumo total en Italia en  
       periodos de tiempo (diario, mensual, por estación)


        Contiene una serie de métodos que permiten analizar los periodos en los que hay generación y 
        consumo, así como la comparación entre estos:

             -createColums(namecoldate): 
                    Devuelve un dataframe con la serie de tiempo dividida en mes, día y tiempo.
             -showSolarGen(typeG,rangeG,title,labelx,labely,year):
                    Muestra la gráfica de generación de energía solar diaria o mensual.
             -showSGenTime():
                    Muestra la gráfica de generación de energía solar diaria y por tiempo.
             -showSGenSta():
                    Muestra el histograma de generacón de energía solar por estación del año.
             -showSolarComG(typeG,rangeG,title,labelx,labely,year)
                    Muestra la gráfica de la relación entre la generación y el consumo de forma
                    diaria o mensual. 
             -showSolarComBar():
                    Muestra un histograma de la diferencia de generación y consumo de forma diaria o 
                    mensual.
            -showSolarComBarSt()
                    Muestra un histograma de la diferencia de generación y consumo por cada estación del 
                    año.
            
        Parámetros:
        url -- ruta donde se encuentra el archivo csv con la información de la fecha de generación y 
               consumo, el consumo [MW] y la generaión de energía solar [MW]
        namecol -- Nombre de las tres columnas del archivo csv, por defecto son ['date_time', 'load', 
               'solar_gen']

     
        
        
    
    """

    #El constructor nos permite inicializar al objeto de la clase EnergyDataItaly así como establecer la   
    #ruta del archivo que va a ser analizado y renombrar las columnas
    def __init__(self, url, namecol=['date_time', 'load', 'solar_gen']):
        self.data = pd.read_csv(url)
        self.namecol = namecol
        self.data.columns = self.namecol
        self.data[namecol[0]] = pd.to_datetime(self.data[namecol[0]])
        self.data.set_index('date_time', inplace=True)
        self.spring = self.data.loc['2016-3-21 00:00:00':'2016-6-20 23:00:00'].sum()
        self.summer = self.data.loc['2016-6-21 00:00:00':'2016-9-22 23:00:00'].sum()
        self.autum = self.data.loc['2016-9-23 00:00:00':'2016-12-20 23:00:00'].sum()
        self.winter = self.data.loc['2016-1-1 00:00:00':'2016-3-20 23:00:00'].sum()+ self.data.loc['2016-12-21 00:00:00':'2016-12-31 23:00:00'].sum()
        self.data = self.data.reset_index()

    def createColums(self,namecoldate=['month','date','time']):
        self.namecoldate = namecoldate
        self.data[namecoldate[0]] = self.data[self.namecol[0]].dt.month
        self.data[namecoldate[1]] = self.data[self.namecol[0]].dt.date
        self.data[namecoldate[2]] = self.data[self.namecol[0]].dt.time
        self.data = self.data.drop([self.namecol[0]],axis=1)
        
    def showSolarGen(self,typeG=0,rangeG=13,title = 'Solar Power Generation (Monthly)',labelx='Month', 
                     labely="Total solar power generation", year="2015"):
        
        total_generation = self.data.groupby([self.namecoldate[typeG]])[self.namecol[2]].sum()
        values = total_generation.values
        values = values.reshape(-1,1)
        months = np.arange(1,rangeG).reshape(-1,1)
        plt.plot(months,values,label=year,linewidth='3',color='#2cb17e')
        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.title(title)
        plt.legend(loc='best')
        plt.show();
        
        
        
    def showSGenTime(self):
        data = self.data
        #data.drop(['month'], axis = 1, inplace = True)
        data = data.pivot(index = 'time', columns = 'date')      
        plt.figure()
        plt.imshow(data['solar_gen'], aspect = 'auto', interpolation = 'gaussian')
        plt.yticks(np.arange(23, -1, -1))
        plt.colorbar()
        plt.xlabel('Day of year')
        plt.ylabel('Time of day')
        plt.title('Solar Generation [MW]')
        plt.show()
        
    def showSGenSta(self):
        
        fig, ax = plt.subplots(nrows=1, ncols=1)
        data = [('spring', self.spring[self.namecol[2]]), ('summer', self.summer[self.namecol[2]]),
                ('autum', self.autum[self.namecol[2]]),('winter', self.winter[self.namecol[2]])]
        stations, value = zip(*data)

        x = np.arange(len(stations))
        ax.bar(x, value, align="center", color='#2cb17e')
        ax.set(xticks=x, xticklabels=stations,title='Solar Power Generation (Stations of the Year)', ylabel='Total solar power generation [MW]', xlabel='Stations of the Year')
        plt.show()

        
        
    def showSolarComG(self,typeG=0,rangeG=13,title = 'Solar Power Generation (Monthly)',labelx='Month', 
                     labely="Total solar power generation [MW]", year="2015"):
        
        total_generation = self.data.groupby([self.namecoldate[typeG]])[self.namecol[2]].sum()
        valuesG = total_generation.values
        valuesG = valuesG.reshape(-1,1)
        
        total_load = self.data.groupby([self.namecoldate[typeG]])[self.namecol[1]].sum()
        valuesL = total_load.values
        valuesL = valuesL.reshape(-1,1)

        months = np.arange(1,rangeG).reshape(-1,1)
        
        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel(labelx)
        ax1.set_ylabel(labely, color='#2cb17e')
        ax1.plot(months,valuesG,label=year,linewidth='3',color='#2cb17e')
        ax1.tick_params(axis='y', labelcolor='#2cb17e')

        ax2 = ax1.twinx()  

        color = 'tab:blue'
        ax2.set_ylabel('Load [MW]', color=color)  
        ax2.plot(months,valuesL,label=year,linewidth='3',color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout() 
        plt.show()
        
    def showSolarComBar(self,typeG=0,rangeG=12,title = 'Solar Power Generation (Monthly)',labelx='Month', 
                     labely="Power [MW]", year="2015"):
       
        total_generation = self.data.groupby([self.namecoldate[typeG]])[self.namecol[2]].sum()
        valuesG = total_generation.values
        
        total_load = self.data.groupby([self.namecoldate[typeG]])[self.namecol[1]].sum()
        valuesL = total_load.values

        months = ('Jan','Feb','Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec')
        
        n_groups = rangeG
        means_frank = valuesG
        means_guido = valuesL
        
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.45
        opacity = 0.8
        
        if(rangeG>12):
            months = np.arange(1,rangeG)
            bar_width =  0.25

        rects1 = plt.bar(index, means_frank, bar_width,
        alpha=opacity,
        color='b',
        label='Generation')

        rects2 = plt.bar(index + bar_width, means_guido, bar_width,
        alpha=opacity,
        color='g',
        label='Load [MW]')

        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.title(title)
        plt.xticks(index + bar_width, months)
        plt.legend()

        plt.tight_layout()
        plt.show()
        
        
    def showSolarComBarSt(self,title = 'Solar Power Generation (Monthly)',labelx='Month', 
                     labely="Power [MW]", year="2015"):
        

        months = ('spring','summer','autum', 'winter')
        n_groups = 4
        means_frank = (self.spring[self.namecol[2]],self.summer[self.namecol[2]],self.autum[self.namecol[2]],self.winter[self.namecol[2]])
        means_guido = (self.spring[self.namecol[1]],self.summer[self.namecol[1]],self.autum[self.namecol[1]],self.winter[self.namecol[1]])
        
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.45
        opacity = 0.8
        rects1 = plt.bar(index, means_frank, bar_width,
        alpha=opacity,
        color='b',
        label='Generation')

        rects2 = plt.bar(index + bar_width, means_guido, bar_width,
        alpha=opacity,
        color='g',
        label='Load')

        plt.xlabel(labelx)
        plt.ylabel(labely)
        plt.title(title)
        plt.xticks(index + bar_width, months)
        plt.legend()

        plt.tight_layout()
        plt.show()