import numpy as np
import pandas as pd
class Reserving:
    def __init__(self):
        """
        Manage the data used to compute the reserving methods.
        """
        self.data=None
        self.triangle=None
        self.triangleComplete=None
        self.facteur=[]
        self.reserve=None
        
    def ImportData(self,filepath,sep=','):
        """
        Function to read data from a text or csv file. The file must contain four columns :
        - claim ID
        - claim occurence year
        - claim adjustment year
        - claim charge
        Args:
        filepath (string):the path of the file to import;
        delim (characters): the delimiter of the file. Default is ','
        """
        self.data=pd.read_csv(filepath,sep=sep)
        self.data.columns=["claimID","claimOccurence","claimAdjustment","claimCharge"]
        
        
    def ComputeTriangle(self,startDate,endDate,cumul=True):
        """
        Create the triangle table by using the data table
        Args:
        startDate:date to start the triangle
        endDate:date of end of the triangle
        cumul: decide if the triangle will be cumulated or not
        """
        dataToUse=self.data[self.data['claimOccurence']<=endDate]
        dataToUse=dataToUse[dataToUse['claimOccurence']>=startDate]
        dataToUse=dataToUse[dataToUse['claimAdjustment']>=startDate]
        dataToUse=dataToUse[dataToUse['claimAdjustment']<=endDate]
        if cumul:
            dataToUse=dataToUse.groupby(['claimOccurence','claimAdjustment']).sum()['claimCharge'].groupby(['claimOccurence']).cumsum()
        else:
            dataToUse=dataToUse.groupby(['claimOccurence','claimAdjustment']).sum()['claimCharge']
        
        yearMin=startDate
        yearMax=endDate
        period=yearMax-yearMin+1
        triangle=pd.DataFrame(data=np.zeros((period,period)),index=range(yearMin,yearMax+1),columns=range(0,period))
        for idx in dataToUse.index:
            triangle.loc[idx[0],0 if idx[1]<=idx[0] else idx[1]-idx[0]]+=dataToUse.loc[idx]
        
        self.triangle=triangle
        return triangle

    
    def chainLadderClassic(self):
        triangle=self.triangle
        facteur=[]
        yearStart=triangle.index.min()
        yearEnd=triangle.index.max()-1
        sizeToConsider=len(triangle.index)-1
        for i in range(sizeToConsider):
            rate=triangle.loc[yearStart:yearEnd-i][i+1].sum()/triangle.loc[yearStart:yearEnd-i][i].sum()
            facteur.append(rate)
        self.facteur=facteur
        return facteur
    
    def completeTriangle(self):
        triangle=self.triangle
        facteur=self.facteur
        yearEnd=triangle.index.max()
        for i in range(len(facteur)):
            for j in range(i+1):
                triangle.loc[yearEnd-j][i+1]=facteur[i]*triangle.loc[yearEnd-j][i]
                
        self.triangleComplete=triangle
        return triangle
    
    def calculateReserve(self):
        triangle=self.triangleComplete
        yearStart=triangle.index.min()
        yearEnd=triangle.index.max()
        period=yearEnd-yearStart+1
        reserve=pd.DataFrame(data=np.zeros(period),index=range(yearStart,yearEnd+1),columns=["Reserve"])
        for i in range(period):
            reserve.loc[yearStart+i]=triangle.loc[yearStart+i][period-1]-triangle.loc[yearStart+i][period-1-i]
            
        reserve.loc['Total']=reserve['Reserve'].sum()
        self.reserve=reserve
        return reserve