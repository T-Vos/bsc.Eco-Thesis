import os
from downloadFunctions.cryptokitties import API_request_Cryptokitties
import pandas as pd
from dateutil.rrule import rrule, MONTHLY
from dateutil.relativedelta import relativedelta

def downloadData(dates=pd.to_datetime({'year': [2021, 2021],'month': [1,1],'day': [1,15]}), download_function=API_request_Cryptokitties):
    print('From: ', dates[0])
    print('To: ', dates[1])

    lines_to_save_data = 50000
    limit = 100

    data_folder = './'+ download_function.__name__
    if not os.path.exists(data_folder) : os.mkdir(data_folder)

    for curr_month in rrule(freq=MONTHLY, dtstart=dates[0], until=dates[1]):
        nextMonth = curr_month + relativedelta(months=1)
        date_folder = data_folder+'/'+str(curr_month.month)+'_'+str(curr_month.year)+'/'
        if not os.path.exists(date_folder) : os.mkdir(date_folder)
        download_function(limit,nextMonth,curr_month, lines_to_save_data,date_folder)
    return

# downloadData(dates=pd.to_datetime({'year': [2021, 2021],'month': [1,6],'day': [1,1]}),download_function=API_request_Cryptokitties)