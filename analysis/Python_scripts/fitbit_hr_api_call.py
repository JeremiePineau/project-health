######### IMPORT LIBRARIES AND RESSOURCES #########
import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
import psycopg2
from google.cloud import bigquery
from google.oauth2 import service_account

########## AUTHENTICATION ##########
CLIENT_ID = "23B4M8"
CLIENT_SECRET = "c9cb64cda63ff148724c21cedad9dfdc"

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()

ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

########## DEFINE VARIABLES ##########

yesterday = str((dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y%m%d"))
yesterday2 = str((dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d"))
today = str(dt.datetime.now().strftime("%Y%m%d"))
today2 = str(dt.datetime.now().strftime("%Y-%m-%d"))
backload_date = str((dt.datetime.now() - dt.timedelta(days=180)).strftime("%Y%m%d"))
backload_date2 = str((dt.datetime.now() - dt.timedelta(days=180)).strftime("%Y-%m-%d"))

sdate = dt.date(2021,7,8)   # start date
edate = dt.date(2021,7,19)   # end date
date_modified=sdate
date_list = [str(sdate.strftime("%Y-%m-%d"))]

while date_modified < edate:
    date_modified += dt.timedelta(days=1)
    date_list.append(str(date_modified.strftime("%Y-%m-%d")))

########## EXECUTION ##########
# Heart Rate data

a = date_list[0]

for a in date_list:
    fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=a, detail_level='1sec')

    days_list = []
    time_list = []
    val_list = []

    for i in fit_statsHR['activities-heart-intraday']['dataset']:
        val_list.append(i['value'])
        time_list.append(i['time'])
        days_list.append(a)
    heartdf = pd.DataFrame({'date_ts':days_list, 'hours':time_list, 'heart_rate':val_list})

########## SAVE DATA LOCALLY ##########
heartdf.to_csv('S:\9_Projects\Project_Health\data\heart_rate\HR_'+ \
               a+'.csv', \
               columns=['date_ts','hours','heart_rate'], header=True, \
               index = False)
