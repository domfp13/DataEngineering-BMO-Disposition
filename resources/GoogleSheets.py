# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

import gspread
from dataclasses import dataclass
from oauth2client.service_account import ServiceAccountCredentials
class Row():
    """This class creates a dynamic object even one of the attributes is empty
    
    Arguments:
        None
    Returns: 
        bmoDataClass obj
    """
    def __init__(self, **kwargs):
        self.caseId = kwargs.get('Case #')
        self.recv_date = kwargs.get('Recv Date (mm/dd/yyyy)')
        self.store_address = kwargs.get('Store Address #') 
        self.floor_id = kwargs.get('Floor #')
        self.city1 = kwargs.get('City')
        self.postal_code = kwargs.get('Postal Code')
        self.asset_tag = kwargs.get('Asset tag #')
        self.serial = kwargs.get('Serial #')
        self.brand = kwargs.get('Brand')
        self.model = kwargs.get('Model #')
        self.type_desc = kwargs.get('Type')
        self.skid = kwargs.get('Skid #')
        self.text = kwargs.get('Text')
        self.redeploy = kwargs.get('Redeploy')
        self.donate = kwargs.get('Re-Sell')
        self.recycle = kwargs.get('Recycle')
        self.bmo_comments = kwargs.get('BMO Comments')

    @staticmethod
    def keys():
        """
        Register names of common fields in this method.
        :return: List of field names
        """
        return ['caseId', 'recv_date', 'store_address', 'floor_id', 'city1', 'postal_code', 'asset_tag', 'serial', 'brand', 'model', 'type_desc', 'skid', 'text', 'redeploy', 'donate', 'recycle', 'bmo_comments']

    def values(self) -> dict:
        """Returns all attributes for this object in a Dict format
        
        Arguments:
            None
        Returns: 
            (dict): Dictionary with all the attributes and values for this object
        """
        return self.__dict__
    
    def __del__(self):
        '''
        This (Magic/Dunder) method deletes the object from memory
        '''
        pass

class Sheet():
    """This class creates a dynamic object even one of the attributes is empty

    Arguments:
        None
    Returns: 
        bmoDataClass obj
    """
    def __init__(self, sheet_name, raw_data):
        self.sheet_name = sheet_name
        self.rows = self.addRows(raw_data=raw_data)

    def addRows(self, raw_data:list):
        """Returns all attributes for this object in a Dict format
        
        Arguments:
            None
        Returns: 
            (dict): Dictionary with all the attributes and values for this object
        """
        data_transformed = []
        for element in raw_data:
            data_transformed.append(Row(**element).values())
        
        return data_transformed

    def __del__(self):
        '''
        This (Magic/Dunder) method deletes the object from memory
        '''
        pass

class SpreadSheet():
    """This class creates an object using the gspread API that connects to the GoogleSheets
    """
    def __init__(self, google_sheet_workbook:str):
        self.__scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        self.__creds = ServiceAccountCredentials.from_json_keyfile_name("Keys/creds.json", self.__scope)
        self.__client = gspread.authorize(self.__creds)
        self.__workbook = self.__client.open(google_sheet_workbook)
        self.spreadSheet_name = google_sheet_workbook
        self.sheets = []

    def getAllSheets(self) -> list:
        """Returns a list of all sheets in workbook
        
        Arguments:
            None
        Returns: 
            (list):  ['Jan 2020', 'Feb 2020', 'March 2020', 'April']
        """
        worksheet_list = self.__workbook.worksheets()
        worksheet_list_names = []
        for obj in worksheet_list:
            worksheet_list_names.append(obj.title)
        return worksheet_list_names
    
    def addSheet(self, sheet_name:str):
        """Returns a list of all sheets in workbook
        
        Arguments:
            sheet_name (str): Sheet's name 
        Returns: 
            (list):  [{'Recv Date (mm/dd/yyyy)': '1/31/2020', 'Store Address #': 'H5044'}, etc]
        """
        self.sheets.append(Sheet(sheet_name=sheet_name, raw_data=self.__workbook.worksheet(sheet_name).get_all_records()))
        
    def __del__(self):
        '''
        This (Magic/Dunder) method deletes the object from memory
        '''
        pass

