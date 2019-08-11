#%%
import os
import os.path
import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
CLIENT_ID = '22B794'
CLIENT_SECRET = '2f31a717c743e5def8bc64381595fe4a'

#%%
# server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
# server.browser_authorize()
# ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
# REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
# print(ACCESS_TOKEN)
# print(REFRESH_TOKEN)


ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMkI3OTQiLCJzdWIiOiI2UTg2NTgiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJhY3QgcnNldCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNTY1MzkyOTgyLCJpYXQiOjE1NjUzNjQxODJ9.zlHyu8LH8OyrwEHa5ASXRKvIY0Esm-F54euBHfP09ts'
REFRESH_TOKEN = 'a881036b4ae57b016a9676530b3dc87626216e3bca5ce3a3d07c0bc76858c724'

auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)


yesterday = str((datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime("%Y%m%d"))


#%% Get HR data and save to *.csv =====================================================
date_hr= str((datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d"))
url_hr =  "https://api.fitbit.com/1.2/user/-/activities/heart/date"+"/"+ date_hr+"/" +date_hr+ "/1sec/time/00:00/23:59.json"
a_hr= auth2_client.make_request(url_hr)

data_hr = a_hr['activities-heart-intraday']['dataset']
index_list = []
time_list =[]
value_list=[]
for i in range(len(data_hr)):
    index_list.append(i)
    time_list.append(data_hr[i].get("time"))
    value_list.append(data_hr[i].get("value"))

hrdf = pd.DataFrame({
                     'index':index_list,
                     'time':time_list,
                     'value':value_list                 
                     })                     

path_save = os.path.join (os.getcwd(),"out_data", today + "_HR_data.csv") 
hrdf.to_csv(path_save,   header=True,  index = None)
# ======================================================================================

#%% Get sleep data 4 stage and save to file ============================================
# get data at "2019-08-09"
# a_sleep = auth2_client.make_request("https://api.fitbit.com/1.2/user/-/sleep/date/2019-08-09.json")

# get data with specific date
date_sleep = str((datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d"))
url_sleep =  "https://api.fitbit.com/1.2/user/-/sleep/date/"+ date_sleep + ".json"
a_sleep = auth2_client.make_request(url_sleep)

data_sleep = a_sleep['sleep'][0]['levels']['data']
index_list = []
dateTime_list =[]
level_list=[]
second_list=[]

for i in range(len(data_sleep)):
    index_list.append(i)
    dateTime_list.append(data_sleep[i].get("dateTime"))
    level_list.append(data_sleep[i].get("level"))
    second_list.append(data_sleep[i].get("seconds"))

sleepdf = pd.DataFrame({
                     'index':index_list,
                     'dateTime':dateTime_list,
                     'level':level_list,
                     'seconds':second_list
                     })                     
sleepdf['value'] = sleepdf['level'].map({'wake':'0','light':'1','rem':'2','deep':'3'})
path_save = os.path.join (os.getcwd(),"out_data", today + "_Sleep_data_4stage.csv") 
sleepdf.to_csv(path_save,   header=True,  index = None)
#=====================================================================================

#%%
a = a_sleep['sleep'][0]['levels']['data']
c = (data_sleep[1])
print(data_sleep[1].get("index"))
print(len(data_sleep))

#%% Get sleep data and save to file ================================================
fit_statsSl = auth2_client.sleep(date='today')
stime_list = []
sval_list = []

# print(fit_statsSl)

for i in fit_statsSl['sleep'][0]['minuteData']:
    stime_list.append(i['dateTime'])
    sval_list.append(i['value'])

sleepdf = pd.DataFrame({'State':sval_list,
                     'Time':stime_list})
sleepdf['Interpreted'] = sleepdf['State'].map({'2':'Awake','3':'Really Awake','1':'Asleep'})


path_save = os.path.join (os.getcwd(),"out_data", today + "_Sleep_data_out.csv") 
sleepdf.to_csv(path_save,   header=True,  index = None)
#=====================================================================================

#%%
