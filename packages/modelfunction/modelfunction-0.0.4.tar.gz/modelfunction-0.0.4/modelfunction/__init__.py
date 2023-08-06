
# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
import unicodecsv as csv
import csv
class ModelFunction(object):
    """
        Parameters
        ----------
        file_path : str
            File path of data in .csv format.
        input_col1 : int
            starting column of input data.
        input_col2 : int
            ending column of input data.
        output_col: int
            output column of data.
        degree : int
            degree of polynomial.
        saving_path : str
            the path to the file to save the model as .csv.
        -------
        
        """
    def __init__(self,file_path,input_col1,input_col2,output_col,degree,saving_path):
        
        self.file_path=file_path
        self.saving_path=saving_path
        self.input_col1=input_col1
        self.input_col2=input_col2
        self.output_col=output_col
        self.degree=degree
        self.y_preds=[]
        self.coef=None
        self.names=None
        self.X=None
        self.Y=None
        self.denklem=None
    def read_data(self):
        """
        Reads your data set in .csv format.

        """
        self.veriler=pd.read_csv(self.file_path)
        self.x = self.veriler.iloc[:,self.input_col1-1:self.input_col2]
        self.y = self.veriler.iloc[:,self.output_col-1:self.output_col]
  
        self.X = self.x.values
        self.Y = self.y.values
    def polynomial_reg(self):
        """
        It trains and tests your data according to leave one out cross validation 
        by applying the polynomial regression method.

        """
        poly_reg = PolynomialFeatures(self.degree)
        for i in range(len(self.X)):
            data = pd.read_csv(self.file_path)   
            x_test,y_test=data.iloc[i,self.input_col1-1:self.input_col2],data.iloc[i,self.output_col-1:self.output_col]
            data=data.drop(i)
            x_train,y_train=data.iloc[:,self.input_col1-1:self.input_col2],data.iloc[:,self.output_col-1:self.output_col]
            x_poly = poly_reg.fit_transform(x_train)
            lin_reg = LinearRegression(fit_intercept=False)
            lin_reg.fit(x_poly,y_train.values.ravel())   
            self.coef = lin_reg.coef_
            self.names=poly_reg.get_feature_names()    
            sample = x_test.values.reshape(1,-1)
            sample = poly_reg.fit_transform(sample)
            ress = lin_reg.predict(sample) 
            self.y_preds.append(ress)
            
    def generate_formula(self):  
        """
        The formula used by the polynomial regression method is generated.

        """
        i = 1
        list1=[]
        for (self.name,c) in zip(self.names,np.nditer(self.coef)):
            self.name +=" "+ "("+str(c)+")"
            new_name = self.name.replace("x0","B"+str(i)).replace("x1","C"+str(i)).replace("x2","D"+str(i)).replace("x3","E"+str(i)).replace("x4","F"+str(i)).replace(" ","*")
            new_name+="+"   
            list1.append(new_name)
        
        list2=[]
        list2.append(list1[-1][: -1])
        list3 = list1[:-1]
        list4 =list3+list2
        self.denklem="'="+str(list4)
        self.denklem=self.denklem.replace("'","").replace(",","").replace(".",",").replace("[","(").replace("]",")").replace(" ","")
        print(self.denklem)
        return self.denklem
    def export_model(self):
        """
        The formula is exported in .csv format.

        """
            
        with open(self.saving_path,'w',newline='',encoding='utf-8-sig') as f:
            w = csv.writer(f, delimiter=',')  
            w.writerow([self.denklem])
        
    
 