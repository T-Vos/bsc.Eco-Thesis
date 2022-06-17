import pandas as pd
import requests
from config import MORALISAPIKEY
import time

maxTries = 10
downloadTime = 1/24

def Moralis(limit=500, block_start=13296011, blocks=1, lines_to_save_data_per_block=50000, data_folder='', chain='eth'):
    my_headers = {'X-API-Key' : MORALISAPIKEY}
    df = pd.DataFrame({}, dtype=str)

    for block in range(blocks):
        offset = 0
        block_on_chain=block_start + block
        url = 'https://deep-index.moralis.io/api/v2/block/'+str(block_on_chain)+'/nft/transfers'
        counter = 0

        for i in range(maxTries):
            try:
                time.sleep(downloadTime)
                while lines_to_save_data_per_block > offset:
                    counter += 1
                    # print('trying to get block '+ str(counter) + 'from blockchain ' + str(block_on_chain))
                    query= {'chain':chain, 'limit':limit, 'offset': offset}
                    response = requests.get(url=url, headers=my_headers, params=query)
                    response = response.json()
                    df_supp = pd.DataFrame(response['result'], dtype=str)
                    
                    if len(df_supp)==0: break
                    df = df.append(df_supp, ignore_index=True)

                    if len(response['result']) == limit : offset += limit
                    else : break
                    df.append(df_supp, ignore_index=True)
                break
            except Exception:
                time.sleep(10)
                if i == maxTries - 1 :
                    print("Failed at block ", str(block_on_chain))
                    df.to_csv(data_folder+'moralis_blocks'+str(block_start)+'-'+str(block_on_chain)+'.csv', index=False)
                    print(Exception)
                    return
                continue

    return df.to_csv(data_folder+'moralis_blocks'+str(block_start)+'-'+str(block_on_chain)+'.csv', index=False)