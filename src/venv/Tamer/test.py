# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 15:39:32 2023

@author: yzt
"""

import pymysql
import pandas as pd
import pandas_market_calendars as mcal
import matplotlib.pyplot as plt


def get_df_from_db(sql):
    db = pymysql.connect(
            host='', 
            port=3306,              
            user='',            
            passwd='',        
            db='rzrq',              
            charset='utf8'          
            )
    cursor = db.cursor()
    cursor.execute(sql)
    """
   
    """
    data = cursor.fetchall()

  
    columnDes = cursor.description 
    columnNames = [columnDes[i][0] for i in range(len(columnDes))] 
    df = pd.DataFrame([list(i) for i in data],columns=columnNames)
    
    """
   
    """
    cursor.close()
    db.close()

    #print("cursor.description中的内容：",columnDes)
    return df

if __name__ == "__main__":
    sql1 = "SELECT * FROM borrowdeclaration21 limit 10"
    df = get_df_from_db(sql1)
    print(df)
