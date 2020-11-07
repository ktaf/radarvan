#! /usr/bin/env python3

from typing import Dict, Tuple
import requests
import json
import os
from sty import Style, RgbFg ,fg

class ArvanCloud:
    def __init__(self):
        self.__ispData = self.__getIspData()
        self.__origin = "https://radar.arvancloud.com"
        self.__apiPath = "/api/v1/internet-monitoring?isp="
        self.__radarApps = self.__getApps()

    def __getIspData(self) -> dict:
        with open('arvan.json','r') as apiFile:
            data = json.load(apiFile)
        
        return dict(data)
    
    def __getApps(self) -> dict:

        fg.Instagram = Style(RgbFg(234,37,185))
        fg.Github = Style(RgbFg(207,17,0))
        fg.Google = Style(RgbFg(236,104,101))
        fg.Twitch = Style(RgbFg(246,204,3))
        fg.Wikipedia = Style(RgbFg(171,0,255))
        fg.Digikala = Style(RgbFg(94,207,39))
        fg.Aparat = Style(RgbFg(118,253,238))
        fg.Varzesh3 = Style(RgbFg(62,133,255))
        fg.End = '\033[0m'

        appList = {
            'instagram':fg.Instagram,
            'github':fg.Github,
            'google':fg.Google,
            'twitch':fg.Twitch,
            'wikipedia':fg.Wikipedia,
            'digikala':fg.Digikala,
            'aparat':fg.Aparat,
            'varzesh3':fg.Varzesh3,  
        }
        
        return appList
    
    def getIspApps(self)->list:
        return self.__radarApps

    def getIspData(self)->dict:
        return self.__ispData

    def getApi(self)->dict:
        return {
            'origin':self.__origin,
            'apiPath':self.__apiPath
        }
    
    def makeURL(self,ispAPI:str) -> str:
        return self.__origin + self.__apiPath + ispAPI

    
    def hasNull(self,appRate:list)->bool:
        for el in appRate:
            if el == None:
                return True
        return False
    
    def avaibleISP(self,ispData=dict)->bool:
        for app in ispData:
            if ispData[app]==None:
                return False
        return True

def main():

    
    arvan = ArvanCloud()
    
    for city in arvan.getIspData():
        # print(city,"***************")
        for isp  in arvan.getIspData()[city]:
            # if isp['api'] != 'afranet':
            #     continue
            
            apiURL = arvan.makeURL(isp['api'])
            # print(apiURL)
            
            res = requests.get(apiURL)
            res = dict(json.loads(res.content))

            
            if not arvan.avaibleISP(res):
                continue
            
            print(city ,isp['name'])
            matrix_col_len = 360
            
            matrix = matrix_generator(arvan=arvan,column=matrix_col_len,resp=res)

            responsive = len(matrix)-int(terminal_columns)
            
            # print(matrix)
            for row in range(len(matrix[0])-1,-1,-1):
                for col in range(responsive,len(matrix)):
                    print(matrix[col][row],end='')
                print("")
            
            for line in range(int(terminal_columns)):
                print('‾',end="")

def matrix_generator(arvan:ArvanCloud,column:int,resp:dict):
    matrix=[]
    max_col=0
    global terminal_columns

    for col in range(column):
        col_list = []
        for app in resp:
            rateList = resp[app]
            if  rateList[col] != None and rateList[col] > 0:
                col_list.append(arvan.getIspApps()[app]+'▐'+fg.End)

        if len(col_list) == 0:
            col_list.append(' ')
        
        if len(col_list) >max_col:
            max_col = len(col_list) 
        # print(col_list)
        matrix.append(col_list)

    # print(matrix)
    
    for col in range(len(matrix)):
        if len(matrix[col])<max_col:
            while len(matrix[col])!=max_col:
                matrix[col].append(' ')
    
    return matrix
    

def printMatrix(matrix):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            print(matrix[row][col],end='')
        print()


if __name__ == "__main__":
    terminal_rows, terminal_columns = os.popen('stty size', 'r').read().split()
    main() 
