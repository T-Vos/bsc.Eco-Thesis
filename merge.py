import os
import pandas as pd
import sqlite3
import statistics
import numpy as np
import functools

# load moralis chunk csv files and merge into 1 dataset
moralis = pd.DataFrame({}, dtype=str)
filePath = "../data/Moralis/"
for filename in os.listdir(filePath):
    if not filename.endswith('csv'): continue # don't read non .csv files
    filePath_combined = filePath+filename
    newCsv = pd.read_csv(filePath_combined)
    moralis  = moralis.append(newCsv, ignore_index=True)


# Load data from Moonstream team
con = sqlite3.connect("../DataOtherSources/EthereumNFTs/nfts.sqlite") # find at https://doi.org/10.34740/KAGGLE/DSV/2698517
cur = con.cursor()
ethereum = pd.read_sql_query("SELECT * from transfers", con)
# print(df.head(10))
# Be sure to close the connection
con.close()

# Get some funky statistics
groupedByBlock = ethereum.groupby(["block_number"])
len(groupedByBlock) # 747033
print(statistics.mean(groupedByBlock.size().values)) # 6
print(statistics.variance(groupedByBlock.size().values)) # 63

# Clean Moralis data
moralis["Crypto"] = "ETH"
moralis["Price_USD"] = 0
moralis["Source"] = "Mo"

moralis = moralis[ moralis["contract_type"] == "ERC721"]

def disjunction(*conditions):
    return functools.reduce(np.logical_or, conditions)

block_max = ethereum["block_number"].max()
block_min = ethereum["block_number"].min()

c_1 = moralis["block_number"] > block_max
c_2 = moralis["block_number"] < block_min

moralis = moralis[disjunction(c_1,c_2)]

moralis = moralis.drop([  "block_hash",
                "block_number",
                "operator",
                "verified",
                "transaction_type",
                "transaction_index",
                "log_index",
                "contract_type",
                "from_address",
                "to_address",
                "amount"
                ], axis=1)
moralis.columns = ['block_number','timestamp', 'transaction_hash', 'transaction_value', 'nft_address',"token_id","Crypto","Price_USD","Source"]

moralis['timestamp'] = pd.to_datetime(moralis['timestamp'])
moralis['timestamp_day'] = moralis['timestamp'].dt.floor('d')

# clean Moonstream data
ethereum = ethereum.drop([ 
                # "block_number",
                "event_id", 
                "from_address",
                "to_address",
                ], axis=1)
ethereum["Crypto"] = "ETH"
ethereum["Price_USD"] = 0
ethereum["Source"] = "MS"
ethereum['timestamp'] = pd.to_datetime(ethereum['timestamp'],unit='s')
ethereum['timestamp_day'] = ethereum['timestamp'].dt.floor('d')

# merge datasets
merge = pd.concat([ethereum,moralis]).reset_index(drop=True)

# export to csv
import datetime
x = datetime.datetime.now()
merge.to_csv('../data/merged/'+str(x.strftime("%Y%m%d"))+'merge.csv')