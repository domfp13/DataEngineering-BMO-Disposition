# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

import pandas as pd
from resources.GoogleSheets import Sheet
from resources.GenericClasses import Time
from resources.GenericFunctions import getPath

class DataFrame():
    
    def __init__(self, sheet, sheet_name:str, year:int, month:int):
        self.df = self.cleanData(sheet=sheet, sheet_name=sheet_name, year=year, month=month)
    
    def cleanData(self, sheet, sheet_name, year, month):
        """Cleans data attribute form a sheet object
        
        Arguments:
            sheet (Sheet): This is the an instance of the class Sheet
            sheet_name (str): This is a string containing the name of the sheet
            year (int): Month as an int formant
            month (int): Year as an int formant
        Returns: 
            None
        """
        import re

        df = pd.DataFrame(data=sheet.rows)

        # Dropping records that are all NaN
        df.dropna(how='all', inplace=True)

        # Transforming columns
        for column in list(df.columns):
            df[column].fillna("", inplace=True)
            df[column] = df[column].astype(str).str.upper()
            df[column] = df[column].astype(str).str.strip()
        
        # "recv_data" cannot be empty string
        df.drop(df[df['recv_date'] == ''].index, axis=0, inplace=True)
        # This is how to use IN operator in pandas
        # df.drop(df[~df[df.columns[0]].apply(lambda x: len(str(x))).isin([14, 15, 16])].index,axis=0,inplace=True)
        
        # "recv_date": replace any character other than a digit or forwardslash
        df['recv_date'] = df['recv_date'].apply(lambda x: re.sub('[^\d\/]','',x))

        # Deleting floating point if any
        for element in ['store_address', 'floor_id', 'asset_tag']:
            df[element] = df[element].apply(lambda x : x.split('.')[0] if ('.' in x) else x)
        
        # Remove duplicates
        #df.sort_values(list_of_columns, inplace=True)
        #df.drop_duplicates(keep='first', inplace=True)

        df['sheet_name'] = sheet_name
        df['year_str'] = year
        df['month_str'] = month        

        return df
    
    def __del__(self):
        """
        This (Magic/Dunder) method deletes the object from memory
        """
        pass
    
class DataFrames():
    
    def __init__(self):
        self.data_frames = []
        self.merged_data_frame = pd.DataFrame()
    
    def addDataFrame(self, sheet, sheet_name, year, month):
        """Adds DataFrame instance to the list object
        
        Arguments:
            sheet (Sheet): This is the an instance of the class Sheet
            sheet_name (str): This is a string containing the name of the sheet
            year (int): Month as an int formant
            month (int): Year as an int formant
        Returns: 
            None
        """      
        self.data_frames.append(DataFrame(sheet, sheet_name, year, month))
    
    def mergeDataFrames(self):
        """Cleans data attribute form a sheet object
        
        Arguments:
            sheet (Sheet): This is the an instance of the class Sheet
            sheet_name (str): This is a string containing the name of the sheet
            year (int): Month as an int formant
            month (int): Year as an int formant
        Returns: 
            None
        """
        counter = 0
        while counter <= len(self.data_frames)-1:
            self.merged_data_frame = pd.concat([self.merged_data_frame, self.data_frames[counter].df], ignore_index=True, sort=False)
            counter += 1

    def convertToCSV(self)->str:
        """Convers a pandas DataFrame to a CSV
        
        Arguments:
            df (DataFrame): Pandas Dataframe
        Returns: 
            Path
        """
        from csv import QUOTE_ALL

        time = Time()
        file_name = 'BMO_Disposition_{year}_{month}_{day}.csv'.format(year=time.getCurrentYear(), month=time.getCurrentMonth(), day=time.getCurrentDay())
        file_full_path = getPath(file_name)

        self.merged_data_frame.to_csv(file_full_path, header=True, index=False, sep=',', quoting=QUOTE_ALL, escapechar = ' ')

        return file_full_path

    def __del__(self):
        """
        This (Magic/Dunder) method deletes the object from memory
        """
        pass
    

        