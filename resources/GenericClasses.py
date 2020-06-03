# -*- coding: utf-8 -*-
# Luis Enrique Fuentes Plata

import datetime
from datetime import date
class Time():
    """This class has several methods for timing
    
    Arguments:
        None
    Returns: 
        None
    """

    def __init__(self):
        self.__date = date   # private attribute

    def getCurrentDay(self) -> int:
        """Returns today's day

        Argumentes:
            None
        Returns:
            (int): 15, 16, 17,etc
        
        """
        return self.__date.today().day

    def getCurrentMonth(self) -> int:
        """Returns today's month

        Argumentes:
            None
        Returns:
            (int): 3,4,5,etc
        
        """
        return self.__date.today().month

    def getCurrentYear(self) -> int:
        """Returns today's year

        Argumentes:
            None
        Returns:
            (int): 2019,2020,etc
        
        """
        return self.__date.today().year

    def getLastdayLastmonth(self) -> datetime.date:
        """Returns the last day for last month as a datetime.date object format

        Argumentes:
            None
        Returns:
            (datetime.date): 2020-02-29
        
        """
        return self.__date.today().replace(day=1) - datetime.timedelta(days=1)

    def getCurrentMonthStr(self) -> str:
        """Returns today's month as a string format

        Argumentes:
            None
        Returns:
            (str): March, June, etc
        
        """
        return self.__date.today().strftime('%B')

    def getLastMonthStr(self) -> str:
        """Returns lasts month as a string format

        Argumentes:
            None
        Returns:
            (str): March, June, etc
        """
        return self.getLastdayLastmonth().strftime('%B')

    @staticmethod
    def getMonthByString(month:str)->int:
        """Returns the month as and int format

        Argumentes:
            month (str): This has to be firt 3 letters and lower case
        Returns:
            (int): 1,2,3,etc
        """
        months = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}
        return months[month]
