import pandas as pd
import requests
import datetime
import time
import os
import sys


def Atomic(limit, time_data, time_start, lines_to_save_data, data_folder):
    print('SET:', time_start)
    counter = 0
    df = pd.DataFrame({}, dtype=str)
    url = "https://wax.api.atomicassets.io/atomicmarket/v1/sales/"
    
    state = {'sold':'3'}
    page=1
    
    time_start = int(time_start.timestamp()*10**3)
    time_data = int(time_data.timestamp()*10**3)
    while(time_data>time_start):

        print('START REQUEST')
        # unixTimeStamp = datetime.datetime(time_start).timestamp()
        print(time_start)

        querystring = {"state":state["sold"],
              "after":time_start,
              "page":str(page),
              "limit":str(limit)}
        
        response = requests.request("GET", url, params=querystring)

        if response.status_code==200:
            print('FOUND ',len(response.json()['data']),' ITEMS')

            df_supp = pd.DataFrame(response.json()['data'], dtype=str)
            if len(df_supp)==0: break
            df = df.append(df_supp, ignore_index=True)
            
            time_data_supp = int(df_supp.created_at_time.min())
            print()
            if page >1:
                if (pd.to_datetime(time_data, unit='ms') -  pd.to_datetime(time_data_supp, unit='ms'))>pd.Timedelta('3 hours'): 
                    page=1
                    time_data=time_data_supp
                else: page+=1
            else:
                if time_data == time_data_supp: page+=1
                else: time_data = time_data_supp
            
            # print(len(df_supp), len(df), pd.to_datetime(time_data), pd.to_datetime(time_data_supp), page)

            counter +=limit
            if counter%lines_to_save_data==0:
                print(len(df_supp), len(df), pd.to_datetime(time_data, unit='ms'), pd.to_datetime(time_data_supp, unit='ms'), page)
                supp = pd.to_datetime(time_start, unit='ms')  
                df.to_csv(data_folder+'NFT_Atomic_'+str(supp.month)+'_'+str(supp.year)+'.csv', index=False)
            
        else: 
            print('Could not retrieve data')
            return
        
        time.sleep(1)
    supp = pd.to_datetime(time_start, unit='ms')
    if len(df)>0:
        df.to_csv(data_folder+'NFT_Atomic_'+str(supp.month)+'_'+str(supp.year)+'.csv', index=False)
    else:
        print('No data in this month')