import pandas as pd
import requests
import datetime
import time
import os
import sys


def Opensea(limit, time_data, time_start, lines_to_save_data, data_folder):
    print('OPENSEA', time_start)
    offset = 0
    counter = 0
    df = pd.DataFrame({}, dtype=str)
    url = "https://api.opensea.io/api/v1/events"
    while(time_data>time_start):
        querystring = {"only_opensea":"false","offset":str(offset),"limit":str(limit), 
                       "event_type":"successful", 'occurred_before':time_data}
        response = requests.request("GET", url, params=querystring)

        print(response.status_code)
        if response.status_code==200:
            print('FOUND', response.json()['asset_events'], 'ITEMS')
            df_supp = pd.DataFrame({}, dtype=str)
            for key in response.json()['asset_events']:
                df_supp = df_supp.append(key, ignore_index=True)
            
            df = df.append(df_supp, ignore_index=True)
            
            time_data_supp = pd.to_datetime(df_supp.created_date.unique()).min()
            
            if offset>0:
                if (time_data -  time_data_supp)>pd.Timedelta('5 hours'): 
                    offset=0
                    time_data=time_data_supp
                else: offset+=limit
            else:
                if time_data == time_data_supp: offset+=limit
                else: time_data = time_data_supp
            
            
            counter +=limit
            if counter%lines_to_save_data==0:
                print(len(df_supp), len(df), pd.to_datetime(time_data), time_data_supp, offset)
                df.to_csv(data_folder+'NFT_OpenSea_'+str(time_start.month)+'_'+str(time_start.year)+'.csv',
                            index=False)
                            
            time.sleep(1)
        else: return
        

    
    if len(df)>0:
        df.to_csv(data_folder+'NFT_OpenSea_'+str(time_start.month)+'_'+str(time_start.year)+'.csv', index=False)
    else:
        print('No data in this month')