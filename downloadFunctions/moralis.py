import pandas as pd
import requests
from config import MORALISAPIKEY


def Moralis(limit=10, block_start=13296011, blocks=1, lines_to_save_data_per_block=500000, data_folder='', chain='eth'):
    my_headers = {'X-API-Key' : MORALISAPIKEY}

    for block in range(blocks):
        df = pd.DataFrame({}, dtype=str)
        limit=10000
        offset = 0
        block_on_chain=block_start + block
        url = 'https://deep-index.moralis.io/api/v2/block/'+str(block_on_chain)+'/nft/transfers'
        counter = 0

        while lines_to_save_data_per_block > offset:
            counter += 1
            query= {'chain':chain, 'limit':limit, 'offset': offset}
            try:
                print('trying to get block '+ str(counter) + 'from blockchain ' + str(block_on_chain))
                response = requests.get(url=url, headers=my_headers, params=query)

            except requests.exceptions.HTTPError as error:
                print(error)
                break

            response = response.json()

            df_supp = pd.DataFrame(response['result'], dtype=str)
            if len(df_supp)==0: break
            df = df.append(df_supp, ignore_index=True)

            if response['page_size'] == limit : offset += limit
            else : break
        df.to_csv(data_folder+'moralis_block'+str(block_on_chain)+'.csv', index=False)